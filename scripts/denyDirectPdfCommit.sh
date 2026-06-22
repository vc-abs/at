#!/usr/bin/env bash
set -euo pipefail

staged_pdf_files="$(
	git diff --cached --name-only --diff-filter=ACMR \
	| awk 'tolower($0) ~ /\.pdf$/ {print $0}'
)"

if [[ -z "$staged_pdf_files" ]]; then
	exit 0
fi

echo "ERROR: Direct PDF commit is blocked by repository policy."
echo
echo "Staged PDF files:"
echo "$staged_pdf_files" | sed 's/^/  - /'
echo
echo "Use DVC instead:"
echo "  ./scripts/addPdfToDvc.sh <path-to-pdf>"
echo "  git add <path-to-pdf>.dvc <pdf-dir>/.gitignore"
echo "  dvc push"
echo
echo "If this is intentional and temporary, use --no-verify (not recommended)."
exit 1
