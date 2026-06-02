# Developer Sandbox Mode

Dev-sandbox mode is an implementation test, not an APP publication.

Show a summary:

```text
DEV-SANDBOX RESULT SUMMARY

  Candidate tree:          publication-staging/
  Validation status:       <release-ready | release-blocked | sandbox-pass | sandbox-pass-with-release-blockers | sandbox-fail>
  Paper-agent test status: <passed | failed | not performed>
  Public-release blockers: <none | list>
  Sandbox-only deferrals:  <none | list>
  Tree hash/checksum:      <hash if available>

  No public repo will be created.
  No APP_PUBLICATION.json manifest will be created.
  No APP compliance record will be written.
```

Record the implementation test result in the requested sandbox log. Include date, protocol/skill version or commit, source fixture/example, validation result, paper-agent test result, public-release blockers, sandbox-only deferrals, and failures/fixes needed.

Never write `.publications.md` or `APP_PUBLICATION.json` in dev-sandbox mode.

