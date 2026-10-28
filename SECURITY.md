# Security

AILab is a local learning app. It is not an internet service.

## Run it on localhost

- Roadmap UI: `127.0.0.1:8765` (`LAB_UI_HOST` / `LAB_UI_PORT`)
- Ollama: `127.0.0.1:11434`

Do not publish those ports. The UI can read repository files so you can open guides beside the steps. It refuses `.git`, `.env`, and `.llama`, and that is not a substitute for keeping the process on your machine.

## Do not commit secrets

Never add API keys, `.env`, private documents, or model weights. `.env.example` lists variable names only.

## Reporting a problem

Open a GitHub issue on [farnodes/AILab](https://github.com/farnodes/AILab) if a change would expose local files, credentials, or the model port. Please do not include your `.env` or `learner/progress.json` in the report.
