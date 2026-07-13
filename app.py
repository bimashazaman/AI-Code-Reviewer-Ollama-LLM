import argparse
import sys
from pathlib import Path
from typing import Optional

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

IGNORED_DIRS = {
    ".git",
    ".svn",
    ".hg",
    "node_modules",
    "vendor",
    "venv",
    ".venv",
    "env",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".idea",
    ".vscode",
    ".next",
    ".nuxt",
    ".cache",
    "coverage",
    "build",
    "dist",
    "out",
    "tmp",
}

IGNORED_EXTS = {
    ".pyc",
    ".pyo",
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".svg",
    ".pdf",
    ".mp3",
    ".mp4",
    ".zip",
    ".tar",
    ".gz",
    ".tgz",
    ".rar",
    ".pack",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".csv",
    ".ttf",
    ".woff",
    ".woff2",
    ".eot",
    ".old",
    ".log",
}

MAX_FILE_SIZE_BYTES = 500 * 1024  # 500 KB limit for code files

def is_ignored(path: Path) -> bool:
    """Check if a file or directory should be ignored."""
    if path.name.startswith(".") and path.name not in {".env", ".gitignore"}:
        return True
    if path.name.endswith(".lock") or "lock.json" in path.name:
        return True
    if path.is_dir() and path.name in IGNORED_DIRS:
        return True
    if path.is_file() and path.suffix.lower() in IGNORED_EXTS:
        return True
    return False


def read_codebase(path_str: Optional[str]) -> str:
    """Reads code from a file, directory, URL, or standard input."""
    if path_str:
        if path_str.startswith("http://") or path_str.startswith("https://"):
            import urllib.request
            url = path_str
            # Automatically append .diff to GitHub PR URLs if not present
            if "github.com" in url and "/pull/" in url and not (url.endswith(".diff") or url.endswith(".patch")):
                url += ".diff"
            
            try:
                # Add a User-Agent header as GitHub sometimes blocks default urllib agents
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as response:
                    return response.read().decode("utf-8")
            except Exception as e:
                raise ReviewError(f"Failed to fetch URL {url}: {e}")

        path = Path(path_str)
        if not path.exists():
            raise ReviewError(f"Path not found: {path_str}")

        if path.is_file():
            try:
                return f"--- File: {path.name} ---\n{path.read_text(encoding='utf-8')}"
            except Exception as e:
                raise ReviewError(f"Failed to read file {path}: {e}")

        if path.is_dir():
            lines = []
            for file_path in path.rglob("*"):
                if file_path.is_file():
                    # Check if any parent directory is ignored or file is ignored
                    if any(is_ignored(p) for p in file_path.parents) or is_ignored(file_path):
                        continue
                    
                    # Skip excessively large files
                    try:
                        if file_path.stat().st_size > MAX_FILE_SIZE_BYTES:
                            continue
                    except OSError:
                        continue

                    try:
                        content = file_path.read_text(encoding="utf-8")
                        rel_path = file_path.relative_to(path)
                        lines.append(f"--- File: {rel_path} ---\n{content}\n")
                    except UnicodeDecodeError:
                        # Skip binary files that don't match IGNORED_EXTS
                        continue

            if not lines:
                raise ReviewError(f"No code files found in directory: {path_str}")
            return "\n".join(lines)

    # Read from standard input if no path is provided
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


def detect_language(path_str: Optional[str]) -> Optional[str]:
    """Detect primary language if a single file is provided."""
    if not path_str:
        return None
    path = Path(path_str)
    if path.is_file():
        return LANGUAGE_BY_EXTENSION.get(path.suffix.lower())
    return "multiple"


def main() -> int:
    parser = argparse.ArgumentParser(description="Review code locally with Ollama.")
    parser.add_argument(
        "path",
        nargs="?",
        help="File or directory to review. If omitted, reads from stdin.",
    )
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help="Ollama model")
    parser.add_argument("-l", "--language", help="Language hint, e.g. python")
    parser.add_argument("-c", "--context", help="Short note about what the code does")
    parser.add_argument("-o", "--output", help="Save review to a file")
    args = parser.parse_args()

    print("=== AI Code Reviewer ===\n")

    try:
        code = read_codebase(args.path)
        language = args.language or detect_language(args.path)
        
        # Auto-detect if the input is a git diff (check first few hundred chars to bypass potential file headers)
        is_diff = "diff --git" in code[:500] or "Index: " in code[:500]

        print("Reviewing...\n")
        if is_diff:
            print("Detected Git Diff / Pull Request. Running PR review mode...\n")
        
        result = review(
            code,
            model=args.model,
            language=language,
            context=args.context,
            is_diff=is_diff,
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
    sys.exit(main())
