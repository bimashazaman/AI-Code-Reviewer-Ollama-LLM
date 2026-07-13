# AI Code Reviewer

Review code locally with [Ollama](https://ollama.com). No API keys, no cloud — your code stays on your machine.

## Setup

1. Install [Ollama](https://ollama.com) and pull a model:

```bash
ollama pull qwen2.5-coder
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

**Interactive** — paste code, then type `END`:

```bash
python app.py
```

**Review a file:**

```bash
python app.py -f app.py
```

**Pipe code in:**

```bash
cat app.py | python app.py
```

**Save the review:**

```bash
python app.py -f app.py -o review.md
```

## Options

| Flag | What it does |
|------|--------------|
| `-f` | Path to a file |
| `-m` | Ollama model (default: `qwen2.5-coder`) |
| `-l` | Language hint |
| `-c` | Short context about the code |
| `-o` | Save output to a file |

## Project files

```
app.py        → CLI and input handling
reviewer.py   → talks to Ollama
prompts.py    → review instructions for the model
```

## Troubleshooting

**`No module named 'ollama'`** — run `pip install -r requirements.txt`

**`Could not reach Ollama`** — open the Ollama app, then run `ollama pull qwen2.5-coder`
