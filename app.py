import argparse
import sys
from pathlib import Path

from reviewer import DEFAULT_MODEL, ReviewError, review

# Guess language from common file extensions.
LANGUAGE_BY_EXTENSION = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".go": "go",
    ".java": "java",
    ".rb": "ruby",
    ".rs": "rust",
    ".php": "php",
    ".c": "c",
    ".cpp": "cpp",
}


def read_code(file_path=None):
    if file_path:
        path = Path(file_path)
        if not path.is_file():
            raise ReviewError(f"File not found: {file_path}")
        return path.read_text(encoding="utf-8")

    if not sys.stdin.isatty():
        return sys.stdin.read()

    print("Paste your code below. Type END on its own line when done.\n")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def detect_language(file_path):
    if not file_path:
        return None
    return LANGUAGE_BY_EXTENSION.get(Path(file_path).suffix.lower())


def main():
    parser = argparse.ArgumentParser(description="Review code locally with Ollama.")
    parser.add_argument("-f", "--file", help="File to review")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help="Ollama model")
    parser.add_argument("-l", "--language", help="Language hint, e.g. python")
    parser.add_argument("-c", "--context", help="Short note about what the code does")
    parser.add_argument("-o", "--output", help="Save review to a file")
    args = parser.parse_args()

    print("=== AI Code Reviewer ===\n")

    try:
        code = read_code(args.file)
        language = args.language or detect_language(args.file)

        print("Reviewing...\n")
        result = review(
            code,
            model=args.model,
            language=language,
            context=args.context,
        )

        print(result)

        if args.output:
            Path(args.output).write_text(result, encoding="utf-8")
            print(f"\nSaved to {args.output}")

    except ReviewError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
