## Hosting

This bot is hosted on a Google Cloud Compute Engine VM.

It runs as a `systemd` service:

- Service name: `spellcrest-bot`

The bot source is deployed to:

- `/home/thomashillebrink/spellcrest-bot`

Live character data is stored outside the repository at:

- `/home/thomashillebrink/spellcrest-bot-data/characters.json`

---

## Environment Variables

The bot uses a local `.env` file on the VM.

Example:

```env
DISCORD_BOT_TOKEN=your_bot_token_here
CHAR_FILE=/home/thomashillebrink/spellcrest-bot-data/characters.json
REFERENCE_FILE=/home/thomashillebrink/spellcrest-bot/reference.json
```
