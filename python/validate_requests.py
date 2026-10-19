import csv
import json
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = [
    "request_id",
    "submitted_at",
    "requester_token",
    "request_type",
    "business_unit",
    "priority_source",
    "request_details",
    "supporting_reference",
    "authorization_status",
]

ALLOWED_REQUEST_TYPES = {
    "data_correction",
    "access_request",
    "fulfillment_exception",
    "vendor_issue",
    "process_blocker",
    "quality_issue",
    "general_request",
}

HIGH_IMPACT_TERMS = re.compile(
    r"fraud|legal action|lawsuit|threat|harassment|discrimination",
    re.IGNORECASE,
)

ROUTE_MAP = {
    "data_correction": "data_quality_queue",
    "access_request": "access_management_queue",
    "fulfillment_exception": "fulfillment_queue",
    "vendor_issue": "vendor_operations_queue",
    "process_blocker": "process_improvement_queue",
    "quality_issue": "quality_assurance_queue",
    "general_request": "general_operations_queue",
}

def normalize(value):
    return (value or "").strip().lower()

def validate_row(row, seen_keys):
    errors = []

    for field in REQUIRED_FIELDS:
        if not normalize(row.get(field)):
            errors.append(f"missing:{field}")

    if normalize(row.get("authorization_status")) != "confirmed":
        errors.append("review:authorization_not_confirmed")

    request_type = normalize(row.get("request_type"))
    if request_type and request_type not in ALLOWED_REQUEST_TYPES:
        errors.append("invalid:request_type")

    duplicate_key = "|".join(
        [
            normalize(row.get("requester_token")),
            normalize(row.get("business_unit")),
            request_type,
        ]
    )

    duplicate = duplicate_key in seen_keys and duplicate_key != "||"
    if duplicate:
        errors.append("duplicate:possible_duplicate")

    seen_keys.add(duplicate_key)

    text = normalize(row.get("request_details")) + " " + normalize(row.get("notes"))
    high_impact = sorted(set(HIGH_IMPACT_TERMS.findall(text)))

    if high_impact:
        errors.append("review:high_impact_language")

    if duplicate:
        status = "duplicate"
        route = "duplicate_queue"
    elif errors:
        status = "needs_review"
        route = "review_queue"
    else:
        status = "ready"
        route = ROUTE_MAP.get(request_type, "review_queue")

    return {
        "request_id": row.get("request_id"),
        "status": status,
        "route": route,
        "errors": errors,
        "high_impact_terms": high_impact,
    }

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python validate_requests.py data/operations_requests_test_cases.csv")

    path = Path(sys.argv[1])
    seen_keys = set()
    results = []

    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            results.append(validate_row(row, seen_keys))

    output = json.dumps(results, indent=2)
    Path("python/validation_results.json").write_text(output)
    print(output)

if __name__ == "__main__":
    main()
