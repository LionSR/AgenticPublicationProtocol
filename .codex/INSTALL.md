# Installing for Codex

## Clone and link

```bash
git clone https://github.com/LionSR/AgenticPublicationProtocol.git ~/.codex/paper-protocol
mkdir -p ~/.codex/skills
ln -sfn ~/.codex/paper-protocol/skills ~/.codex/skills/paper-protocol
```

Restart Codex to pick up the skills. This links the entire `skills/` directory, so every skill shipped with the protocol is available, and new ones appear automatically after `git pull`.

## Updating

```bash
cd ~/.codex/paper-protocol && git pull
```

## Uninstalling

```bash
rm ~/.codex/skills/paper-protocol
rm -rf ~/.codex/paper-protocol
```
