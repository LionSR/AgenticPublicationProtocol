# Installing for Codex

## Option A: Use the skill installer

```
$skill-installer install --repo LionSR/AgenticPublicationProtocol --path skills/publish-paper skills/load-paper-agent
```

Restart Codex to pick up new skills.

## Option B: Manual clone + symlink

```bash
git clone https://github.com/LionSR/AgenticPublicationProtocol.git ~/.codex/paper-protocol
mkdir -p ~/.codex/skills
ln -s ~/.codex/paper-protocol/skills/publish-paper ~/.codex/skills/publish-paper
ln -s ~/.codex/paper-protocol/skills/load-paper-agent ~/.codex/skills/load-paper-agent
```

Restart Codex to pick up new skills.

## Updating

```bash
cd ~/.codex/paper-protocol && git pull
```

## Uninstalling

```bash
rm -rf ~/.codex/skills/publish-paper ~/.codex/skills/load-paper-agent
rm -rf ~/.codex/paper-protocol
```
