# Phase 6B — Developer Sandbox Mode

Dev-sandbox mode is an implementation-testing workflow, not a publication workflow. It uses the same prepare and validate standards up through phase 5, then substitutes a sandbox outcome for public release.

Before finalizing the sandbox run, show:

```text
DEV-SANDBOX RESULT SUMMARY:

  Sandbox target:          <path>
  Candidate tree:          publication-staging/
  Test case:               <new publication example | revision example | fixture name>
  Validation status:       <release-ready | release-blocked | sandbox-pass | sandbox-pass-with-release-blockers | sandbox-fail>
  Paper-agent test status: <passed | failed | not performed>
  Public-release blockers: <none | missing LICENSE | other blockers>
  Sandbox-only deferrals:  <none | list explicitly deferred items>
  Tree hash/checksum:      <hash if available>

  Outcome:
    <record success | preserve failing state for debugging | reset sandbox>

  Important:
    No public repo will be created.
    No APP_PUBLICATION.json manifest will be created.
    No APP compliance record will be written.
```

Record the implementation test result in the agreed sandbox log or test notes for the protocol implementation. Include:

- date;
- protocol/skill version or commit;
- sandbox target;
- source fixture/example;
- validation result;
- paper-agent test result;
- public-release blockers;
- sandbox-only deferrals;
- failures and fixes needed, if any.

If the run passed and the sandbox policy says to reset, reset the reusable sandbox to baseline. If the run failed or the researcher wants to inspect it, preserve `publication-staging/` and relevant logs temporarily.

Never write `.publications.md` as a compliance record in dev-sandbox mode. If a sandbox log is needed, use an implementation-test location whose name makes clear it is not an APP publication record.
