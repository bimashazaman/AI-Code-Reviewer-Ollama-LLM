# AI Code Reviewer

A lightweight CLI tool that reviews code locally using [Ollama](https://ollama.com) and a coding-focused language model. Paste code, point at a file, or pipe input from another command — no API keys or cloud services required.

## Features

- Local, private code review powered by Ollama
- Structured feedback: bugs, security, performance, readability, best practices, and an improved version
- Multiple input modes: interactive paste, file path, or stdin pipe
- Configurable model and optional language hint
- Clear error messages when Ollama is not running or the model is missing

## Prerequisites

- **Python 3.9+**
- **[Ollama](https://ollama.com)** installed and running
- A coding model pulled locally (default: `qwen2.5-coder`)

```bash
# Install Ollama from https://ollama.com, then pull the model:
ollama pull qwen2.5-coder
```

Other models that work well for code review:

```bash
ollama pull codellama
ollama pull deepseek-coder-v2
```

## Installation

```bash
git clone https://github.com/bimashazaman/AI-Code-Reviewer-Ollama-LLM
cd ai-code-reviewer

pip install -r requirements.txt
```

## Usage

### Interactive mode

Run the app and paste your code. Press **Ctrl+D** (Mac/Linux) or **Ctrl+Z** then **Enter** (Windows) when finished:

```bash
python app.py
```

### Review a file

```bash
python app.py --file path/to/script.py
```

Short form:

```bash
python app.py -f reviewer.py
```

### Pipe code from stdin

```bash
cat app.py | python app.py
```

```bash
echo "def add(a,b): return a+b" | python app.py
```

### Specify language and model

```bash
python app.py -f app.py -l python -m qwen2.5-coder
```

### CLI options

| Flag | Description |
|------|-------------|
| `-f`, `--file` | Path to a source file to review |
| `-m`, `--model` | Ollama model name (default: `qwen2.5-coder`) |
| `-l`, `--language` | Language hint, e.g. `python`, `javascript`, `go` |
| `-h`, `--help` | Show help message |

## Example output

The reviewer returns markdown with sections like:

- **Overall Score** — rating out of 10
- **Bugs** — concrete issues or runtime risks
- **Security Issues** — unsafe patterns or vulnerabilities
- **Performance** — inefficiencies and scaling concerns
- **Readability** — naming, structure, maintainability
- **Best Practices** — idiomatic patterns for the language
- **Improved Version** — suggested rewrite when useful
- **Explanation** — summary of what to fix first
- **Score Breakdown** — per-dimension scores

## Project structure

```
ai-code-reviewer/
├── app.py           # CLI entry point
├── reviewer.py      # Ollama integration and review logic
├── prompts.py       # System prompt for the reviewer
├── requirements.txt # Python dependencies
└── README.md
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'ollama'`

Install dependencies:

```bash
pip install -r requirements.txt
```

### `Failed to reach Ollama`

1. Make sure the Ollama app is running.
2. Confirm the model is installed:

```bash
ollama list
ollama pull qwen2.5-coder
```

3. Test Ollama directly:

```bash
ollama run qwen2.5-coder "Hello"
```

### Slow responses

Larger models produce better reviews but take longer. Try a smaller model if speed matters:

```bash
python app.py -f app.py -m codellama
```

## License

MIT
