#!/usr/bin/env bash
# run_tests.sh - CI-ready test runner (cross-platform)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$SCRIPT_DIR"

# Find venv Python (Windows Git Bash vs Linux/Mac)
if [ -f ".venv/Scripts/python.exe" ]; then
    VENV_PYTHON=".venv/Scripts/python.exe"
elif [ -f ".venv/bin/python" ]; then
    VENV_PYTHON=".venv/bin/python"
else
    echo "❌ Virtual environment not found. Create with: python -m venv .venv"
    exit 1
fi

echo "🔹 Running pytest via virtual environment..."
"$VENV_PYTHON" -m pytest --tb=short -v
TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Tests failed or encountered an error!"
    exit 1
fi