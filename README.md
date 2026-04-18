# LawxBot

A powerful Discord moderation bot built for **Lawxed** — the official server of **Lawx**, a Pakistani streamer with 100+ members. LawxBot gives moderators full control over server management with commands for banning, kicking, muting, warning, and automatic message filtering.

## Features

- Ban one or multiple members with an optional message deletion window and reason
- Kick one or multiple members with a reason
- Timeout members for a specified duration
- Remove timeouts from members
- Warn members — auto-timeout triggers after 3 warnings
- Purge an entire channel (delete and recreate it cleanly)
- Clear a specific number of recent messages
- Assign roles to members
- Mute / unmute members in voice channels
- Deafen / undeafen members in voice channels
- Automatic offensive word detection with auto-deletion and auto-warning
- All moderation commands are restricted to authorized roles only
- Logs all bot activity to `Discord.log`
- 24/7 uptime via Railway

## How the Program Works

Run the bot and it connects to Discord using your token stored as an environment variable.

- The bot listens for commands prefixed with `!`
- Only members with the **🩸 Crib Mod** or **Hoodie** role can use moderation commands
- When a message containing an offensive word (from `offensivewords.txt`) is detected, the message is deleted, the user is DM'd, and a warning is issued
- Warnings are tracked in `warning.json` — after **3 warnings**, the member is automatically timed out for 5 minutes and their warning count resets
- If a member has DMs disabled, the bot sends a fallback message in the channel

## Commands

All commands use the `!` prefix. All commands require the **🩸 Crib Mod** or **Hoodie** role.

---

### Ban
```
!ban <member(s)> [delete_days] <reason>
```
| Parameter | Type | Required | Description |
|---|---|---|---|
| `member(s)` | Mention / ID | Yes | One or more members to ban |
| `delete_days` | Integer | No | Number of days of messages to delete (default: 0) |
| `reason` | String | Yes | Reason for the ban |

**Example:**
```
!ban @user1 @user2 3 Spamming in chat
```

---

### Kick
```
!kick <member(s)> <reason>
```
| Parameter | Type | Required | Description |
|---|---|---|---|
| `member(s)` | Mention / ID | Yes | One or more members to kick |
| `reason` | String | Yes | Reason for the kick |

**Example:**
```
!kick @user Being disrespectful
```

---

### Timeout
```
!timeout <member> <minutes> [reason]
```
| Parameter | Type | Required | Description |
|---|---|---|---|
| `member` | Mention / ID | Yes | Member to timeout |
| `minutes` | Integer | Yes | Duration of timeout in minutes |
| `reason` | String | No | Reason for the timeout (default: "No reason provided") |

**Example:**
```
!timeout @user 10 Repeated warnings
```

---

### Remove Timeout
```
!untimeout <member>
```
| Parameter | Type | Required | Description |
|---|---|---|---|
| `member` | Mention / ID | Yes | Member whose timeout to remove |

**Example:**
```
!untimeout @user
```

---

### Warn
```
!warn <member(s)>
```
| Parameter | Type | Required | Description |
|---|---|---|---|
| `member(s)` | Mention / ID | Yes | One or more members to warn |

- Warning count is saved in `warning.json`
- At **3 warnings**, member is auto-timed out for **5 minutes** and count resets

**Example:**
```
!warn @user1 @user2
```

---

### Purge Channel
```
!purge
```

No parameters. Deletes the entire channel and recreates it in the same position.

**Example:**
```
!purge
```

---

### Clear Messages
```
!clear_messages [num]
```
| Parameter | Type | Required | Description |
|---|---|---|---|
| `num` | Integer | No | Number of messages to delete (default: 5) |

**Example:**
```
!clear_messages 20
```

---

### Assign Role
```
!assign <member> <role>
```
| Parameter | Type | Required | Description |
|---|---|---|---|
| `member` | Mention / ID | Yes | Member to assign the role to |
| `role` | Role Mention / Name | Yes | Role to assign |

**Example:**
```
!assign @user @SomeRole
```

---

### Mute (Voice)
```
!mute <member>
```
| Parameter | Type | Required | Description |
|---|---|---|---|
| `member` | Mention / ID | Yes | Member to server-mute in voice |

Member must be in a voice channel.

**Example:**
```
!mute @user
```

---

### Unmute (Voice)
```
!unmute <member>
```
| Parameter | Type | Required | Description |
|---|---|---|---|
| `member` | Mention / ID | Yes | Member to unmute in voice |

**Example:**
```
!unmute @user
```

---

### Deafen (Voice)
```
!deafen <member>
```
| Parameter | Type | Required | Description |
|---|---|---|---|
| `member` | Mention / ID | Yes | Member to server-deafen in voice |

**Example:**
```
!deafen @user
```

---

### Undeafen (Voice)
```
!undeafen <member>
```
| Parameter | Type | Required | Description |
|---|---|---|---|
| `member` | Mention / ID | Yes | Member to undeafen in voice |

**Example:**
```
!undeafen @user
```

---

## Automatic Word Filter

The bot reads from `offensivewords.txt` (one word per line, already included in the repository) on every message.

- If a banned word is found, the message is **deleted**
- The user receives a **DM warning**
- A **warning** is logged to `warning.json`
- After **3 warnings**, automatic **5-minute timeout** is applied and the count resets

---

## Hosting — Keeping LawxBot Alive 24/7

LawxBot is hosted on **Railway** and includes a Flask web server (`webserver.py`) that runs on a background thread alongside the bot, exposing an HTTP endpoint at port `8080`.

### How to host on Railway

1. Push your code to a GitHub repository.
2. Go to [railway.app](https://railway.app) and create a new project.
3. Select **Deploy from GitHub repo** and connect your repository.
4. Once the project is created, go to the **Variables** tab and add:
   ```
   DISCORD_TOKEN=your_token_here
   ```
5. Go to the **Settings** tab and set the **Start Command** to:
   ```bash
   python main.py
   ```
6. Deploy the service. Railway will build and run the bot automatically.

Railway redeploys automatically whenever you push new commits to your connected GitHub repository.

---

## How to Run the Program

### Prerequisites

- Python 3.10+
- A Discord Bot Token ([Discord Developer Portal](https://discord.com/developers/applications))
- Bot must have the following permissions: `Ban Members`, `Kick Members`, `Manage Roles`, `Manage Channels`, `Moderate Members`, `Mute Members`, `Deafen Members`, `Manage Messages`
- The following Gateway Intents must be enabled in the Developer Portal: `Message Content Intent`, `Server Members Intent`, `Presence Intent`

### Setup

1. Clone the repository and navigate to the project folder.

2. Create a `.env` file in the root directory:
   ```
   DISCORD_TOKEN=your_token_here
   ```

---

### Option 1: Using Python (Simple Way)

1. Make sure **Python** is installed.

2. Install dependencies:
   ```bash
   pip install discord.py python-dotenv flask
   ```

3. Run the bot:
   ```bash
   python main.py
   ```

---

### Option 2: Using uv (Optional)

1. Install **uv** (if not already installed):
   ```bash
   pip install uv
   ```

2. Sync the project environment:
   ```bash
   uv sync
   ```

3. Run the bot:
   ```bash
   uv run main.py
   ```

---

## File Structure

```bash
project/
│── main.py               # Main bot file with all commands
│── webserver.py          # Flask web server for 24/7 hosting
│── offensivewords.txt    # List of banned words (one per line)
│── warning.json          # Auto-generated warning tracker (created at runtime)
│── Discord.log           # Auto-generated bot activity log (created at runtime)
│── .env                  # Your Discord token (do NOT commit this)
│── README.md
│── .python-version
│── pyproject.toml
│── uv.lock
```

## Technologies Used

- Python
- [discord.py](https://discordpy.readthedocs.io/) — Discord API wrapper
- python-dotenv — Environment variable management
- Flask — Lightweight web server running on a background thread
- json module — Warning persistence
- datetime module — Timeout duration handling
- logging module — Activity logging

## Notes

- The bot only responds to commands from members with the **🩸 Crib Mod** or **Hoodie** role.
- Never commit your `.env` file or expose your bot token publicly.
- `warning.json` is auto-created when the first warning is issued — no manual setup needed.
- Voice commands (`!mute`, `!unmute`, `!deafen`, `!undeafen`) only work if the target member is currently in a voice channel.
- The bot must be higher in the role hierarchy than the member being moderated, otherwise actions will fail.
- `!purge` completely recreates the channel — all message history will be permanently lost.

## Author

Built for the **Lawxed** Discord server — official community of **Lawx**, Pakistani content creator.

---

If you like this project, consider giving it a star on GitHub!