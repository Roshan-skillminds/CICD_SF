#!/usr/bin/env python3
"""
Reads the PR description and decides which Apex tests the pipeline should run.

Looked-for convention in the PR body:

    ## Apex Tests
    ClassA, ClassB

or:

    ## Apex Tests
    RunRelevantTests

If no "## Apex Tests" section is found (or it's empty), falls back to
"No Apex classes found", which tells the pipeline to use the default test level.

Sets the result into GITHUB_ENV as `apex_test_classes` so later workflow
steps can read it as ${{ env.apex_test_classes }}.
"""
import os
import re
import sys

DEFAULT_RESULT = "No Apex classes found"


def parse_apex_test_classes(pr_body: str) -> str:
    match = re.search(r"##\s*Apex Tests\s*\n(.+?)(\n##|\Z)", pr_body, re.IGNORECASE | re.DOTALL)
    if not match:
        return DEFAULT_RESULT

    section = match.group(1).strip()
    if not section:
        return DEFAULT_RESULT

    first_line = section.splitlines()[0].strip()
    if not first_line:
        return DEFAULT_RESULT

    if first_line.lower() == "runrelevanttests":
        return "RunRelevantTests"

    classes = [c.strip() for c in first_line.split(",") if c.strip()]
    return ",".join(classes) if classes else DEFAULT_RESULT


def main() -> None:
    pr_body = os.environ.get("PR_BODY", "") or ""
    result = parse_apex_test_classes(pr_body)

    print(f"apex_test_classes = {result}")

    github_env = os.environ.get("GITHUB_ENV")
    if github_env:
        with open(github_env, "a", encoding="utf-8") as f:
            f.write(f"apex_test_classes={result}\n")
    else:
        print("::warning::GITHUB_ENV not set - not running inside GitHub Actions?", file=sys.stderr)


if __name__ == "__main__":
    main()
