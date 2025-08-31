# Telegram Gifts Buyer Bot, UserBot

[![Tests](https://github.com/bavanDA/gifts-buyer-bot/actions/workflows/tests.yml/badge.svg)](https://github.com/bavanDA/gifts-buyer-bot/actions/workflows/tests.yml)


This bot allows users to **automatically purchase Telegram gifts** based on **price** and **supply**.  
It supports sending gifts to both **individual users** and **channels**, and can optionally connect to a **user account** to purchase **premium gifts**.

## Features:

- ⭐ **Charge & Refund Stars** – Manage star balances for each user.  
- 🧾 **Order Management** – Create and store orders based on **gift price** and **supply**.  
- 🔄 **Gift Retrieval** – Fetch gifts from the upstream Telegram userbot via API.  
- ⚙️ **Background Fulfillment** – Process and complete orders automatically.  
- 🎁 **Gift Delivery** – Send gifts to **individual users** or **channels**.  
- 🔔 **Gift Notifications** – Get notified instantly when new gifts are available.  
- ⚡ **Rapid Purchase Mode** – Buy new gifts in large amounts before they run out.  
- 👥 **Relay Mode** – Act as a relayer and buy gifts on behalf of your friends.  
- 👥 **Multi-User Support** – Multiple users can use the system concurrently.  
- 🔑 **Userbot Fallback** – Connect your own Telegram account to purchase  premium gifts 
- 📊 **Star Balances** – View and manage balances for all users.  
- 🛡 **Role System** – Assign roles with different permissions (see table).  

| Role     | Permissions |
|----------|-------------|
| Receiver | Can only receive gifts |
| Buyer    | Can create orders and charge stars |
| Admin    | All buyer permissions, plus can add/remove users and change roles |



## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/bavanDA/gifts-buyer-bot.git
cd gifts-buyer-bot
```
### 2. Change `.env.example` file to `.env`
Update the environment variables as needed. At minimum, set your `BOT_TOKEN` and `ADMIN_ID`. Other variables are optional.


### 3. Start the bot:

#### Linux / macOS
```bash
./scripts/setup.sh
./scripts/start-bot.sh
```

#### Windows (CMD)


```CMD
scripts\setup.bat
scripts\start-bot.bat
```


## Docker Setup

You can also run the bot using Docker. Follow these steps:


1. Rename `.env.example` to `.env` and update the environment variables as needed

2. Build the Docker image:
```bash
docker compose build
```
3. (Optional) Connect the bot to your Telegram account.

  ###### Run this command if you want to link a user account; otherwise, skip this step:

```bash
docker compose run login_once
```
4.  Run the bot container:
```bash
docker compose up -d gifts-buyer-bot

```

## Notes

- To add a **channel** as a receiver: add the bot to the channel and send `/start` command from that channel.  
- Orders and star balances are persisted in `data/app.db`.  
- When the Telegram bot fails to buy a gift, it will attempt to purchase it using the connected userbot. This feature is only accessible to the bot owner.
- ⚠️ This project is under **development** — **Use at your own risk**.

## License

This project is licensed under the [MIT License](LICENSE).