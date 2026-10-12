# Mobile Backend API Test Plan

Use only a test backend and accounts approved for the assessment. Avoid destructive actions and never test another person's account.

| Area | Safe validation idea | Evidence to record |
|---|---|---|
| Authentication | Verify unauthenticated requests are rejected | Request/response with tokens redacted |
| Object-level authorisation | With two test accounts, verify each can access only its own records | Account role, object ID, response status |
| Token lifecycle | Review expiry, logout, refresh and revocation behaviour | Redacted token claims and observed result |
| Rate limiting | Use a documented low request rate in a test environment | Request count, response codes, retry headers |
| Error disclosure | Submit invalid but non-destructive input | Error response with secrets removed |
| Data minimisation | Review response fields returned to each role | Field list and business justification |

Do not label a weakness as confirmed until it is reproducible and its context is understood.
