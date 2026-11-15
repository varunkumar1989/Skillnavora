# Week 1, Subject 4 and 21: dictionaries, lists, JSON
import json

message = {
    "role": "user",
    "content": "Summarise this policy in 3 bullets",
}
conversation = [
    {"role": "system", "content": "You are a helpful assistant."},
    message,
]
text = json.dumps(conversation, indent=2)
print(text)

# A very rough token estimate: about 4 characters per token in English
estimate = len(text) // 4
print("Rough token estimate:", estimate)
