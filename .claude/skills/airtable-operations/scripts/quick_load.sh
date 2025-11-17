#!/bin/bash
# Quick loader wrapper for demo usage
# Usage: ./quick_load.sh <csv_path> [--dry-run]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOADER="$SCRIPT_DIR/load_candidates.py"

if [ $# -eq 0 ]; then
    echo "Usage: ./quick_load.sh <csv_path> [--dry-run] [--verbose]"
    echo ""
    echo "Examples:"
    echo "  ./quick_load.sh reference/guildmember_scrape.csv"
    echo "  ./quick_load.sh data/executives.csv --dry-run"
    echo "  ./quick_load.sh ../Exec_Network.csv --verbose"
    exit 1
fi

python3 "$LOADER" "$@"
