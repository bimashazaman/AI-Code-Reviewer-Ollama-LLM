import argparse
import sys
from pathlib import Path

from reviewer import DEFAULT_MODEL, ReviewError, review


def read_code_from_file(path: str) -> str:
    file_path = Path(path)
    if not file_path.is_file():
        raise ReviewError(f"File not found: {path}")
    return file_path.read_text(encoding="utf-8")


def read_code_interactive() -> str:
    print("Paste your code below.")
    print("Press Ctrl+D (Mac/Linux) or Ctrl+Z then Enter (Windows) when done:\n")
    return sys.stdin.read()


def read_code(args: argparse.Namespace) -> str:
    if args.file:
        return read_code_from_file(args.file)
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return read_code_interactive()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Review code locally with Ollama and a coding-focused LLM.",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Path to a source file to review",
    )
    parser.add_argument(
        "-m",
        "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "-l",
        "--language",
        help="Programming language hint, e.g. python, javascript, go",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    print("=== AI Code Reviewer ===\n")

    try:
        code = read_code(args)
        if not code.strip():
            raise ReviewError("No code provided.")

        print("Reviewing... (this may take a moment)\n")
        result = review(code, model=args.model, language=args.language)
        print(result)
        return 0
    except ReviewError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
