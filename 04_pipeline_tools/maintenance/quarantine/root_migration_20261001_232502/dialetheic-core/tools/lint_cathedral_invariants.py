#!/usr/bin/env python3
"""
tools/lint_cathedral_invariants.py

Zero-dependency standard library implementation:
- REC-01: Three-Layer Causal Integrity (Semantic ≠ Computational ≠ Physical)
- REC-03: Landauer Conservation Lint (Limitation 34.4 enforcement)
"""

import sys
import re
from pathlib import Path
from html.parser import HTMLParser

VALID_LAYERS = {"semantic", "computational", "physical"}

class ApparatusCausalAuditor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.active_apparatus_stack = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        is_apparatus = (
            "data-apparatus" in attr_dict
            or tag == "figure"
            or "data-layer" in attr_dict
        )

        if is_apparatus:
            app_id = attr_dict.get("id", f"unnamed-{tag}-{self.getpos()[0]}:{self.getpos()[1]}")
            layer = attr_dict.get("data-layer")

            if not layer:
                self.errors.append(f"[REC-01] Missing data-layer declaration on apparatus: {app_id}")
                apparatus_info = {
                    "id": app_id,
                    "declared": set(),
                    "has_transducer": False
                }
            else:
                declared = {l.strip() for l in layer.split("|")}
                invalid = declared - VALID_LAYERS
                if invalid:
                    self.errors.append(f"[REC-01] Invalid causal layer(s) {invalid} on: {app_id}")

                has_transducer = (
                    "computational" in declared
                    or "data-transducer" in attr_dict
                )
                apparatus_info = {
                    "id": app_id,
                    "declared": declared,
                    "has_transducer": has_transducer
                }

            self.active_apparatus_stack.append(apparatus_info)
        else:
            if "data-transducer" in attr_dict and self.active_apparatus_stack:
                self.active_apparatus_stack[-1]["has_transducer"] = True

    def handle_endtag(self, tag):
        if self.active_apparatus_stack:
            app = self.active_apparatus_stack.pop()
            declared = app["declared"]
            if "semantic" in declared and "physical" in declared and not app["has_transducer"]:
                self.errors.append(
                    f"[REC-01 VIOLATION] L1 (Semantic) bridges directly to L3 (Physical) "
                    f"on '{app['id']}' without declaring L2 (Computational) or data-transducer."
                )

def audit_rec03_landauer_lint(text_content: str) -> list[str]:
    errors = []
    banned_tokens = ["bypass", "recycle", "refund", "recover"]
    pattern = re.compile(
        r"([^.\n]*?Landauer[^.\n]*?(" + "|".join(banned_tokens) + r")[^.\n]*?\.)",
        re.IGNORECASE
    )

    for match in pattern.finditer(text_content):
        sentence = match.group(1)
        if "Limitation 34.4" not in sentence:
            errors.append(
                f"[REC-03 VIOLATION] Landauer erasure recovery claimed without Limitation 34.4 citation:\n"
                f"  -> \"{sentence.strip()}\""
            )
    return errors

def run_checks(html_path: str):
    path = Path(html_path)
    if not path.is_file():
        print(f"ERROR: Target file not found: {html_path}")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")

    parser = ApparatusCausalAuditor()
    parser.feed(content)
    rec01_errs = parser.errors

    rec03_errs = audit_rec03_landauer_lint(content)

    total_errors = rec01_errs + rec03_errs
    if total_errors:
        print(f"FAILED: {len(total_errors)} architectural invariants broken in {html_path}")
        for err in total_errors:
            print(f"  • {err}")
        sys.exit(1)

    print(f"PASSED: Tier 0 invariants verified for {html_path}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "dist/master_report.html"
    run_checks(target)
