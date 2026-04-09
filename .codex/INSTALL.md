# Installing for Codex

## Option A: Use the skill installer

```
$skill-installer install --repo LionSR/AgenticPublicationProtocol --path skills/publish-paper skills/load-paper-agent skills/prepublish-organize skills/extract-context skills/create-paper-page
```

Restart Codex to pick up new skills.

## Option B: Manual clone + symlink

```bash
git clone https://github.com/LionSR/AgenticPublicationProtocol.git ~/.codex/paper-protocol
mkdir -p ~/.codex/skills
ln -s ~/.codex/paper-protocol/skills/publish-paper ~/.codex/skills/publish-paper
ln -s ~/.codex/paper-protocol/skills/load-paper-agent ~/.codex/skills/load-paper-agent
ln -s ~/.codex/paper-protocol/skills/prepublish-organize ~/.codex/skills/prepublish-organize
ln -s ~/.codex/paper-protocol/skills/extract-context ~/.codex/skills/extract-context
ln -s ~/.codex/paper-protocol/skills/create-paper-page ~/.codex/skills/create-paper-page
```

Restart Codex to pick up new skills.

## Updating

```bash
cd ~/.codex/paper-protocol && git pull
```

## Uninstalling

```bash
rm -rf ~/.codex/skills/publish-paper ~/.codex/skills/load-paper-agent ~/.codex/skills/prepublish-organize ~/.codex/skills/extract-context ~/.codex/skills/create-paper-page
rm -rf ~/.codex/paper-protocol
```
