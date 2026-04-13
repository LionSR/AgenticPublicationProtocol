# Publication Checklist

## Which sections apply?

Not every section applies to every paper. Use this guide to skip irrelevant sections:

- **Theory paper** (no code): Paper, Supplementary Materials, AGENTS.md, Validation, Final
- **Computational paper**: All sections
- **Experimental paper** (wet lab + analysis scripts): Paper, Data, Supplementary Materials, AGENTS.md, Validation, Final
- **Notebook paper**: Paper, Code (focus on notebooks), Data, Supplementary Materials, AGENTS.md, Validation, Final

---

## Paper
- [ ] Paper source is included and designated as ground truth
- [ ] Paper compiles / renders without errors (if applicable)
- [ ] All figures match the published/submitted version
- [ ] BibTeX entry is complete and correct
- [ ] License file is present

## Code
- [ ] All scripts run with the publication repo directory structure
- [ ] Import paths are updated for the publication repo layout
- [ ] No hardcoded absolute paths (e.g., `/Users/name/...`)
- [ ] Dependencies are pinned in `environment/requirements.txt` (or equivalent)
- [ ] Figure generation scripts produce output matching `paper/figures/`

## Data
- [ ] Local data files are included and correctly referenced
- [ ] External data links are verified and accessible
  - [ ] <!-- link 1 — replace with actual URL and verification status -->
  - [ ] <!-- link 2 -->
- [ ] Download instructions are documented and tested
- [ ] Data README explains what each file/dataset is

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

## Skills
- [ ] Each skill in `skills/` has a valid SKILL.md with name and description
- [ ] Skill instructions are accurate and tested
- [ ] Skills do not make claims that contradict the paper

## AGENTS.md
- [ ] All file paths in Repository Structure exist in the repo
- [ ] All commands in figure generation table have been tested
- [ ] Paper Summary captures what makes the work distinctive
- [ ] Ground truth hierarchy is clear (paper is authoritative)
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
- [ ] README is complete and accurate
- [ ] `.gitignore` covers build artifacts and sensitive files
- [ ] No sensitive information in any committed file
- [ ] Researcher has reviewed and approved everything
