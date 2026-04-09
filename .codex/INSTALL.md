# Installing Paper Protocol Skills for Codex

## Prerequisites

- Git

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/paper-protocol/skills.git ~/.codex/paper-protocol
   ```

2. **Create the skills symlinks:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/paper-protocol/skills/publish-paper ~/.agents/skills/publish-paper
   ln -s ~/.codex/paper-protocol/skills/load-paper-agent ~/.agents/skills/load-paper-agent
   ```

3. **Restart Codex** to discover the skills.

## Verify

```bash
ls -la ~/.agents/skills/publish-paper
ls -la ~/.agents/skills/load-paper-agent
```

## Updating

```bash
cd ~/.codex/paper-protocol && git pull
```

## Uninstalling

```bash
rm ~/.agents/skills/publish-paper
rm ~/.agents/skills/load-paper-agent
rm -rf ~/.codex/paper-protocol
```
