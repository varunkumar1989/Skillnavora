"""Settings, read from environment variables (or a .env file you load yourself).

OFFLINE mode (default when ANTHROPIC_API_KEY is not set) runs everything without a network
call, so every lesson works for free. Set ANTHROPIC_API_KEY to call Claude for real.
"""
import os
from dataclasses import dataclass


def _load_dotenv(path=".env"):
    """Tiny .env reader so beginners do not need an extra package. Existing variables win."""
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_key: str = os.environ.get("ANTHROPIC_API_KEY", "")
    model: str = os.environ.get("CLAUDE_MODEL", "claude-opus-5-5")
    effort: str = os.environ.get("CLAUDE_EFFORT", "medium")          # low | medium | high | xhigh | max
    max_tokens: int = int(os.environ.get("CLAUDE_MAX_TOKENS", "4000"))
    # Prices per 1M tokens used for cost reports. Defaults are the published list prices for the
    # default model at the time of writing; always check the provider's pricing page.
    price_in_per_m: float = float(os.environ.get("PRICE_INPUT_PER_M", "4.00"))
    price_out_per_m: float = float(os.environ.get("PRICE_OUTPUT_PER_M", "20.00"))
    log_path: str = os.environ.get("APP_LOG_PATH", "logs/requests.jsonl")
    min_retrieval_score: float = float(os.environ.get("MIN_RETRIEVAL_SCORE", "0.12"))

    @property
    def offline(self) -> bool:
        return not self.api_key


settings = Settings()
