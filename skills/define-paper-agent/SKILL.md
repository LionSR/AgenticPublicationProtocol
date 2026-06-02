---
name: define-paper-agent
description: Draft and iterate the APP paper-agent documentation in publication-staging, including AGENTS.md, CLAUDE.md, and README.md, using the author-approved staging tree and reproduction report.
---

# Define Paper Agent

Use this after `prepare-staging`. The output is author-reviewed paper-agent documentation inside `publication-staging/`.

Assume the author may not know APP. Explain that `AGENTS.md` tells future reader agents how to represent the paper and use the staged files.

## Process

1. Read:
   - `publication-staging/`;
   - `working/reproduction/reproduction-report.md`;
   - `PROTOCOL.md` `AGENTS.md` schema;
   - templates under `template/`.
2. Ask the author for the core message they want readers to take away before drafting summary/key-results text.
3. Draft `publication-staging/AGENTS.md` from `template/AGENTS.md`:
   - required frontmatter;
   - identity and ground-truth hierarchy;
   - paper summary and key results in author intent;
   - repository structure with staging-root paths;
   - concrete "What You Can Do" commands;
   - environment setup matching `environment/README.md`;
   - figure/table reproduction summary pointing to `code/figure-reproduction/README.md`;
   - computational requirements and heavy-command warnings;
   - citation;
   - supplementary materials and skills when present.
4. Create `publication-staging/CLAUDE.md` as `@AGENTS.md`.
5. Self-check:
   - every path exists from staging root;
   - setup commands and runner prefixes match `environment/README.md`;
   - figure/table statuses match `code/figure-reproduction/README.md`;
   - no stale "not validated" or overbroad "fully validated" claims;
   - licensing language matches `LICENSE` or sandbox deferral.
6. Invoke `/validate-publication --stage agents-md`.
7. Walk the author through `AGENTS.md` section by section. Revise until the author agrees it reflects their intent.
8. Draft `publication-staging/README.md` from `template/README.md`. Keep setup, citation, reproduction, and validation status compatible with `AGENTS.md`.
9. Show README to the author and revise.

Do not invent author voice. Do not imply that optional supplementary material is ground truth.

