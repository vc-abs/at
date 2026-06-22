#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
	echo "Usage: $0 <pdf-path> [<pdf-path> ...]"
	echo "Example: $0 references/texts/muhurta/newBook.pdf"
	exit 1
fi

for pdf in "$@"; do
	if [[ ! -f "$pdf" ]]; then
		echo "ERROR: File not found: $pdf"
		exit 1
	fi
	if [[ "${pdf##*.}" != "pdf" ]]; then
		echo "ERROR: Not a .pdf file: $pdf"
		exit 1
	fi
	echo "Adding to DVC: $pdf"
	dvc add "$pdf"
done

echo
echo "Now stage pointers (example):"
echo "  git add <file>.dvc <dir>/.gitignore"
echo "Optionally push DVC cache:"
echo "  dvc push"
