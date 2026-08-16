#!/usr/bin/env python3
"""
Reads a Salesforce deploy/validate result JSON file (produced via `sf ... --json`)
and enforces a minimum org-wide Apex code coverage percentage.

Usage:
    python3 code_coverage.py <path-to-deploy-result.json>

Env vars:
    MIN_COVERAGE - minimum required coverage percentage (default: 75)

Exits non-zero (fails the CI step) if coverage is below the threshold.
"""
import json
import os
import sys


def compute_coverage(data: dict) -> float | None:
    run_test_result = (
        data.get("result", {})
        .get("details", {})
        .get("runTestResult", {})
    )
    coverage_entries = run_test_result.get("codeCoverage", []) or []

    total_locations = 0
    total_covered = 0
    for entry in coverage_entries:
        num_locations = int(entry.get("numLocations", 0) or 0)
        num_not_covered = int(entry.get("numLocationsNotCovered", 0) or 0)
        total_locations += num_locations
        total_covered += num_locations - num_not_covered

    if total_locations == 0:
        return None

    return round((total_covered / total_locations) * 100, 2)


def main() -> None:
    if len(sys.argv) < 2:
        print("::error::Usage: code_coverage.py <deploy-result.json>")
        sys.exit(1)

    result_path = sys.argv[1]
    min_coverage = float(os.environ.get("MIN_COVERAGE", "75"))

    if not os.path.exists(result_path):
        print(f"::error::Deploy result file not found: {result_path}")
        sys.exit(1)

    with open(result_path, encoding="utf-8") as f:
        data = json.load(f)

    percent = compute_coverage(data)

    if percent is None:
        print("::warning::No coverage data found in deploy result - skipping coverage check")
        sys.exit(0)

    print(f"Overall Apex code coverage: {percent}% (minimum required: {min_coverage}%)")

    if percent < min_coverage:
        print(f"::error::Code coverage {percent}% is below the required {min_coverage}%")
        sys.exit(1)

    print("Coverage check passed.")


if __name__ == "__main__":
    main()
