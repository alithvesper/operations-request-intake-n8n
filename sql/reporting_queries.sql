-- Requests by processing status
SELECT
    processing_status,
    COUNT(*) AS request_count
FROM requests
GROUP BY processing_status
ORDER BY request_count DESC;

-- Requests by route
SELECT
    route,
    COUNT(*) AS route_count
FROM requests
GROUP BY route
ORDER BY route_count DESC;

-- Review reasons
SELECT
    review_reasons,
    COUNT(*) AS review_count
FROM requests
WHERE review_required = 1
GROUP BY review_reasons
ORDER BY review_count DESC;

-- Duplicate keys
SELECT
    duplicate_key,
    COUNT(*) AS matching_requests
FROM requests
GROUP BY duplicate_key
HAVING COUNT(*) > 1;

-- Workflow failures
SELECT
    error_code,
    COUNT(*) AS error_count
FROM workflow_runs
WHERE status = 'failed'
GROUP BY error_code
ORDER BY error_count DESC;

-- Exception types
SELECT
    exception_type,
    COUNT(*) AS exception_count
FROM exception_log
GROUP BY exception_type
ORDER BY exception_count DESC;

-- Average Workflow B processing duration in seconds
SELECT
    AVG(
        (julianday(completed_at) - julianday(started_at)) * 86400
    ) AS average_processing_seconds
FROM workflow_runs
WHERE workflow_name = 'Workflow B — AI Classification and Routing'
  AND started_at IS NOT NULL
  AND completed_at IS NOT NULL;
