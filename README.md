# Operational Request Intake and Exception Triage System

## Project status

Practice project / synthetic-data prototype.

## Problem

Operations teams may receive incomplete, duplicate, high-impact, or difficult-to-route
requests across fulfillment, vendor operations, quality assurance, access management,
and process improvement.

## Goal

Demonstrate a controlled workflow for operational request intake, validation,
classification, routing, exception handling, and human review.

## Safety boundary

This project does not approve refunds, modify financial records, delete business data,
send external communications automatically, make legal or compliance decisions, or
process real customer, employee, financial, or confidential business data.

## Synthetic-data statement

All records use fictional identifiers and synthetic values.
No real business data, credentials, or production systems were used.

## Workflow summary

1. Receive synthetic JSON request by webhook.
2. Return a controlled webhook response.
3. Normalize request fields.
4. Create a Google Sheets request record.
5. Check duplicates.
6. Validate required fields and authorization.
7. Detect high-impact language.
8. Send eligible requests to AI classification.
9. Validate structured AI output.
10. Route requests to operational queues.
11. Create Asana tasks for valid actionable requests.
12. Send Slack notifications for exceptions.
13. Create Gmail drafts for human review.
14. Record workflow outcomes and exceptions.

## Why n8n

n8n provides explicit control over webhook responses, JSON transformation,
conditional branching, Google Sheets operations, AI classification, error handling,
and external business-tool integrations.

## Workflow split

Workflow A performs webhook intake, normalization, validation, duplicate checks,
safety screening, and workflow logging.

Workflow B performs AI classification, AI-output validation, category-conflict
checking, final routing, Asana task creation, Slack notifications, and Gmail drafts.

## Deterministic logic

- Missing required fields route to review.
- Unconfirmed authorization routes to review.
- Duplicate keys route to the duplicate queue.
- High-impact language routes to review.
- Valid requests route by request category.
- Invalid, uncertain, conflicting, or unmatched AI results route to review.

## AI role

The AI classifies the request category, extracts the requested action, summarizes
the request, and identifies ambiguity or possible high impact.

The AI does not approve refunds, modify records, delete data, contact customers,
or make business decisions.

## Data model

- Requests
- Workflow Runs
- Review Queue
- Exception Log

## Error handling

The workflow handles missing fields, unconfirmed authorization, duplicates,
high-impact language, invalid JSON, invalid AI output, category conflicts,
unmatched routes, and integration failures.

## Testing

See `docs/testing-results.md`.

## Measured prototype results

Report only results actually observed from the test runs.

## Limitations

- Synthetic data only.
- No production deployment.
- No real business-system integration.
- No security or compliance certification.
- Webhook authentication is not implemented in the first prototype.
- Duplicate detection is limited to the documented key.
- AI classification requires human review when uncertain.
- Gmail creates drafts only; it does not send email automatically.

## Future improvements

- Webhook authentication.
- Formal schema validation.
- Idempotency and event deduplication.
- Role-based access controls.
- Secure credential management.
- Production monitoring and alerting.
- Integration testing with approved systems.
- Controlled retry policies.
