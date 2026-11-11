#!/usr/bin/env bash
# cURL examples. STATUS: UNTESTED against the live API. Confirm the URL and model ID on https://docs.x.ai.
# Usage: export XAI_API_KEY=...  (never paste the key into a file you share)
set -euo pipefail
BASE_URL="${XAI_BASE_URL:-https://api.x.ai/v1}"
MODEL="${GROK_MODEL:-grok-4.7}"   # placeholder model ID

# 1. A single chat request (POST with a JSON body)
curl -sS "$BASE_URL/chat/completions" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\": \"$MODEL\", \"max_tokens\": 150,
       \"messages\": [{\"role\": \"system\", \"content\": \"Answer in one sentence.\"},
                      {\"role\": \"user\", \"content\": \"What is an API key?\"}]}"
echo

# 2. Streaming: -N turns off buffering so you see each server-sent event as it arrives
curl -sS -N "$BASE_URL/chat/completions" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\": \"$MODEL\", \"stream\": true, \"max_tokens\": 100,
       \"messages\": [{\"role\": \"user\", \"content\": \"Count from 1 to 5.\"}]}"
echo

# 3. List models available to your key (GET request, no body). Endpoint assumed; check the docs.
curl -sS "$BASE_URL/models" -H "Authorization: Bearer $XAI_API_KEY"
echo
