# Installing for Codex

Just clone and symlink.

## Installation

1. **Clone:**
   ```bash
   git clone https://github.com/LionSR/AgenticPublicationProtocol.git ~/.codex/paper-protocol
   ```

2. **Symlink skills:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/paper-protocol/skills/publish-paper ~/.agents/skills/publish-paper
   ln -s ~/.codex/paper-protocol/skills/load-paper-agent ~/.agents/skills/load-paper-agent
   ```

3. **Restart Codex** to discover the skills.

## Updating

```bash
cd ~/.codex/paper-protocol && git pull
```

## Uninstalling

```bash
rm ~/.agents/skills/publish-paper ~/.agents/skills/load-paper-agent
rm -rf ~/.codex/paper-protocol
```
