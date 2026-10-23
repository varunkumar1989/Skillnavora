# tools/

`chat.src.js` is the source of the AI chat function. Cloudflare runs the bundled copy in
`functions/api/chat.js`, which includes the Anthropic SDK so no install step is needed.

To change the assistant's instructions, edit `chat.src.js`, then rebuild:

```bash
npm install --no-save @anthropic-ai/sdk@0.132.1 esbuild@0.24.0
npx esbuild tools/chat.src.js --bundle --format=esm --platform=neutral --target=es2022 \
  --main-fields=module,main --conditions=worker,browser --external:'node:*' \
  --outfile=functions/api/chat.js --legal-comments=eof
```

`wrangler.toml` turns on `nodejs_compat`, which the SDK needs on Cloudflare.
