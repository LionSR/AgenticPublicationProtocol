# Publication Checklist

Skill-internal QA tracker for `/publish-paper`. Walked with the researcher during phase 3 (after organizing files) and phase 5 (final review). **This file is not part of any publication** — it lives with the skill and tracks progress within a single publication run. Items that do not apply can be marked N/A.

---

## Paper
- [ ] Paper source is included and designated as ground truth
- [ ] Paper compiles / renders without errors (if applicable)
- [ ] All figures match the published/submitted version
- [ ] BibTeX entry is complete and correct

## Code
- [ ] All scripts run with the publication repo directory structure
- [ ] Import paths are updated for the publication repo layout
- [ ] No hardcoded absolute paths (e.g., `/Users/name/...`)
- [ ] Dependencies are pinned in `environment/requirements.txt` (or equivalent)
- [ ] Figure generation scripts produce output matching `paper/figures/`
- [ ] Each figure has its own reproduction script in `code/`; no script produces multiple figures (or the exception is documented)

## Data
- [ ] Local data files are included and correctly referenced
- [ ] `data/README.md` exists and describes every local and external dataset (URL, download command, local destination, whether required for the default workflow)
- [ ] External data links are verified and accessible
- [ ] Download instructions are documented and tested

## Environment
- [ ] Setup instructions work on a clean machine
- [ ] Platform and version requirements are documented
- [ ] Heavy computation requirements are flagged in AGENTS.md

## Supplementary Materials
- [ ] `know-how.md` captures key methodology decisions and tacit knowledge
- [ ] `authors-note.md` reflects what the authors want readers to know
- [ ] Conversation history included/excluded per researcher preference
- [ ] Additional materials (slides, posters, tutorials) have copyright clearance
- [ ] All supplementary files pass confidentiality screening
- [ ] No paper appendix necessary for understanding is in `supplementary/` (move to `paper/`)

## Skills
- [ ] Each skill in `skills/` has a valid SKILL.md with name and description
- [ ] Skill instructions are accurate and tested
- [ ] Skills do not make claims that contradict the paper

## License
- [ ] `LICENSE` file exists at repo root with no extension
- [ ] Single license covers the whole repo, OR the `LICENSE` file explicitly covers the different licenses of manuscript, code, and data
- [ ] Any third-party or proprietary restrictions are called out in `LICENSE`

## AGENTS.md
- [ ] All file paths in Repository Structure exist in the repo
- [ ] All commands in figure generation table have been tested
- [ ] Paper Summary captures what makes the work distinctive
- [ ] Identity section declares that paper, code, and data are ground truth
- [ ] Computational requirements are accurate
- [ ] Citation entry is correct
- [ ] Supplementary Materials section points to correct files
- [ ] Skills section lists all published skills

## Validation
- [ ] Structure validation passed (after file organization)
- [ ] AGENTS.md validation passed (after drafting)
- [ ] README validation passed (after drafting)
- [ ] Full validation passed (before release)

## Final
- [ ] README covers paper title, authors, link to paper PDF / arXiv / DOI, talk-to-agent instructions, and citation
- [ ] `.gitignore` covers build artifacts and sensitive files
- [ ] No sensitive information in any committed file
- [ ] GitHub Release notes drafted and reviewed with the researcher (captures what is new in this version)
- [ ] Researcher has reviewed and approved everything
