# Telegram Session String Generator Bot [V2]

A secure, feature-rich Telegram bot built using **Pyrogram**, **Telethon**, and **Pyromod** to generate session strings entirely in-memory.

---

## Features
* **Multi-Library Support:** Generate strings for both **Pyrogram V2** and **Telethon**.
* **User & Bot Token Support:** Supports generating sessions for user accounts as well as bot tokens (`@BotFather`).
* **Demo API Option:** Built-in default demo API credentials so users without their own API ID/Hash can test or generate seamlessly.
* **Full Security (In-Memory):** No local `.session` SQLite database files are ever saved on disk.
* **Saved Messages Routing:** Automatically forwards the generated session string directly to the user's Telegram Saved Messages.
* **Auto-Self-Destruct:** Temporary chat copies of the string and 2FA passwords automatically wipe themselves after 60 seconds.
* **Interactive Menus & Guides:** Aesthetic media layout on `/start` with built-in `/help` command and basic guides.
* **24/7 Uptime Ready:** Includes an integrated `aiohttp` health check server for cron job pinging.

---

## Deployment Guide (Render)

1. Fork or upload this repository to your GitHub account.
2. Create a new **Web Service** on [Render](https://render.com).
3. Connect your GitHub repository.
4. Set the following build and start configurations:
   * **Runtime:** `Python 3`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `python main.py`
5. Add the following **Environment Variables** in your Render dashboard:
   * `API_ID` - Your Telegram API ID (from my.telegram.org)
   * `API_HASH` - Your Telegram API Hash
   * `BOT_TOKEN` - Your Telegram Bot Token (from @BotFather)
6. Deploy! 

---

##  Keeping It Alive 24/7
Render free web services spin down after 15 minutes of inactivity. To prevent this:
1. Copy your live Render URL (e.g., `https://your-app-name.onrender.com/`).
2. Set up a free cron job on [cron-job.org](https://cron-job.org) or UptimeRobot to ping your URL every **10 minutes**.

---

## Commands
* `/start` - Launch the aesthetic interactive control panel.
* `/help` - Read detailed usage instructions and guides.
* `/cancel` - Terminate any ongoing session generation prompts.
