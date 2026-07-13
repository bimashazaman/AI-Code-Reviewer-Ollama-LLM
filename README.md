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

You can use the AI Code Reviewer to analyze an entire codebase, a single file, or a quick snippet.

### Review an Entire Codebase
Simply provide the path to your project folder. The tool will automatically gather your code while ignoring massive folders (like `node_modules`, `.git`, `vendor`) and large data files to keep the review efficient.

```bash
python3 app.py ./my-project/
```

### Review a Single File
Pass the exact file you want to review.

```bash
python3 app.py src/main.py
```

### Review a Snippet (Interactive)
Run the script without any arguments. You can paste your code directly into the terminal. Type `END` on a new line when you're finished.

```bash
python3 app.py
```

### Pipe Code In
You can also pipe the output of any command directly into the reviewer.

```bash
cat app.py | python3 app.py
```

### Save the Review
Save the generated review to a Markdown file using the `-o` flag.

```bash
python3 app.py ./my-project/ -o review.md
```

## Options

| Flag / Arg | What it does |
|------------|--------------|
| `path`     | (Optional) Directory or file to review. If omitted, reads from standard input. |
| `-m`       | Ollama model (default: `qwen2.5-coder`) |
| `-l`       | Language hint (useful for snippets) |
| `-c`       | Short context about what the code does |
| `-o`       | Save output to a specific file path |

## Project files

```
app.py        → CLI, input handling, and directory traversal
reviewer.py   → Talks to Ollama
prompts.py    → Review instructions for the model
```

## Troubleshooting

**`No module named 'ollama'`** — run `pip install -r requirements.txt`

**`Could not reach Ollama`** — open the Ollama app, then run `ollama pull qwen2.5-coder`

**`Error: Path not found`** — Ensure the file or directory you specified actually exists.
