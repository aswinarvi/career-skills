#!/usr/bin/env bash
# Smoke test: verify the three scripts work end-to-end against the bundled example.
# Usage: bash scripts/smoke_test.sh   (from anywhere; needs node + python3)
set -euo pipefail

SKILL="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
cd "$TMP"

fail() { echo "FAIL: $1" >&2; exit 1; }

# 0. the vendored single-file docx bundle must load and export the API
node -e "const d=require('$SKILL/scripts/vendor/docx.js'); if(!(d.Document&&d.Packer&&d.Paragraph)) process.exit(1)" \
  || fail "vendor/docx.js bundle is broken"

# 1. build the bundled example (navy/a4 defaults)
node "$SKILL/scripts/build_docx.js" "$SKILL/assets/resume.example.json" out.docx >/dev/null
[ -s out.docx ] || fail "build_docx produced no output"

# 2. classic theme / letter page
python3 - "$SKILL/assets/resume.example.json" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1]))
d["meta"].update(theme="classic", page="letter")
json.dump(d, open("classic.json", "w"))
EOF
node "$SKILL/scripts/build_docx.js" classic.json classic.docx >/dev/null
[ -s classic.docx ] || fail "classic/letter build failed"

# 3. the example resume must pass the ATS check (exit 0 at score >= 85)
python3 "$SKILL/scripts/ats_check.py" "$SKILL/assets/resume.example.json" >/dev/null \
  || fail "example resume no longer passes ats_check"

# 4. plain-text export
python3 "$SKILL/scripts/to_plaintext.py" "$SKILL/assets/resume.example.json" out.txt >/dev/null
[ -s out.txt ] || fail "to_plaintext produced no output"

# 5. bare-string bullets: must not crash the linter or get dropped from the docx
cat > str.json <<'EOF'
{"basics":{"name":"T"},"experience":[{"company":"A","title":"D","bullets":["Built X","Shipped Y"]}]}
EOF
out="$(python3 "$SKILL/scripts/ats_check.py" str.json || true)"
echo "$out" | grep -q "ATS score:" || fail "ats_check crashed on string bullets"
node "$SKILL/scripts/build_docx.js" str.json str.docx >/dev/null
python3 - <<'EOF'
import zipfile
xml = zipfile.ZipFile("str.docx").read("word/document.xml").decode()
assert "Built X" in xml and "Shipped Y" in xml, "string bullets were dropped from the docx"
EOF

echo "smoke test: OK"
