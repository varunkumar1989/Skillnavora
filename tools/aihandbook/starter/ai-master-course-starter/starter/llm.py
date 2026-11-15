"""One function to call a language model: chat(system, user) -> Reply.

- No ANTHROPIC_API_KEY: an offline stand-in answers from the context in the prompt, so every
  lesson runs for free and gives the same output each time.
- With ANTHROPIC_API_KEY: calls Claude through the official Anthropic SDK. Server-side
  fallbacks are switched on, so if the model declines a request the API retries it on a
  fallback model inside the same call. Set CLAUDE_MODEL to change the model.
"""
import re
import time
from dataclasses import dataclass, field

from .config import settings


@dataclass
class Reply:
    text: str
    input_tokens: int
    output_tokens: int
    model: str
    latency_s: float
    stop_reason: str = "end_turn"
    offline: bool = False
    extra: dict = field(default_factory=dict)


def estimate_tokens(text: str) -> int:
    """Rough estimate for offline mode: about 4 characters per token in English."""
    return max(1, len(text) // 4)


def _offline_answer(system: str, user: str) -> str:
    """A transparent stand-in for a model: picks the source sentence that shares the most
    (rarer) words with the question and quotes it with its source tag. Good enough to test
    the plumbing and the refusals; it is not a language model and cannot reason."""
    from .embeddings import STOP

    def words(text: str) -> set[str]:
        out = set()
        for w in re.findall(r"[a-z0-9]+", text.lower()):
            if w in STOP or len(w) < 3:
                continue
            w = w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w
            out.add(w[:6])  # crude stem: "approve" and "approval" both become "approv"
        return out

    body, _, question = user.rpartition("QUESTION:")
    filler = {"how", "many", "much", "what", "when", "who", "which", "can", "get", "doe", "day", "year", "compan", "policy", "employ"}
    all_q = words(question)
    q_words = all_q - filler          # the words that carry the meaning
    weak = all_q & filler             # small tie-breakers such as "day" or "year"
    sentences = []
    for tag, text in re.findall(r"\[(S\d+)\]\s*(.*?)(?=\n\[S\d+\]|\Z)", body, flags=re.S):
        for sentence in re.split(r"(?<=[.!?])\s+", " ".join(text.split())):
            # drop a heading glued to the front of the sentence, e.g. "Sick Leave Employees get ..."
            sentence = re.sub(r"^(?:[A-Z][a-z]+ ){1,3}(?=[A-Z][a-z]+ [a-z])", "", sentence.strip())
            if len(sentence.split()) >= 3 and sentence.endswith((".", "!", "?")):
                sentences.append((tag, sentence))
    if not sentences or not q_words:
        return "I don't know. The documents I was given do not answer this question."
    # words that appear in few sentences count for more (a tiny version of IDF)
    df = {}
    for _, sent in sentences:
        for w in words(sent):
            df[w] = df.get(w, 0) + 1
    best, best_score, best_hits = None, 0.0, 0
    for tag, sent in sentences:
        shared = q_words & words(sent)
        sw = words(sent)
        score = sum(1 + 1 / df[w] for w in shared) + 0.3 * len(weak & sw)
        if score > best_score:
            best, best_score, best_hits = (tag, sent), score, len(shared)
    # refuse unless enough of the question's key words are found in one sentence: half of them,
    # or 60% when a specific word (6+ letters, such as "parental") appears nowhere in the sources
    missing = any(len(w) == 6 and w not in df for w in q_words)
    need = 0.6 if missing else 0.5
    if not best or best_hits / len(q_words) < need:
        return "I don't know. The documents I was given do not answer this question."
    tag, sentence = best
    return f"{sentence} [{tag}]"


def chat(system: str, user: str, max_tokens: int | None = None) -> Reply:
    start = time.perf_counter()
    if settings.offline:
        text = _offline_answer(system, user)
        return Reply(text=text, input_tokens=estimate_tokens(system + user), output_tokens=estimate_tokens(text),
                     model="offline-stand-in", latency_s=time.perf_counter() - start, offline=True)

    import anthropic  # imported only when a key is set, so offline mode needs no SDK

    client = anthropic.Anthropic()
    try:
        response = client.beta.messages.create(
            model=settings.model,
            max_tokens=max_tokens or settings.max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
            output_config={"effort": settings.effort},
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
    except anthropic.AuthenticationError:
        raise RuntimeError("The API key was rejected. Check ANTHROPIC_API_KEY.")
    except anthropic.RateLimitError:
        raise RuntimeError("Rate limited by the API. Wait a minute and try again.")
    except anthropic.APIStatusError as e:
        raise RuntimeError(f"API error {e.status_code}: {e.message}")
    except anthropic.APIConnectionError:
        raise RuntimeError("Could not reach the API. Check your internet connection.")

    if response.stop_reason == "refusal":
        category = getattr(response.stop_details, "category", None) if response.stop_details else None
        text = "The model declined this request" + (f" (category: {category})." if category else ".")
    else:
        text = "".join(block.text for block in response.content if block.type == "text").strip()
    return Reply(text=text, input_tokens=response.usage.input_tokens, output_tokens=response.usage.output_tokens,
                 model=response.model, latency_s=time.perf_counter() - start, stop_reason=response.stop_reason,
                 extra={"request_id": getattr(response, "_request_id", None)})
