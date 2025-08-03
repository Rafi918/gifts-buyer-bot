# Gifts Buyer Bot For Telegram

This bot allows users to automatically purchase future gifts based on price and supply. It supports both individual users and public channels, retrieving gift data from an upstream Telegram user bot via API.

Features:

- ⭐ Charge and refund stars to users.
- 🧾 Create and store orders based on gift price and supply.
- 🔄 Retrieving gift data from upstream Telegram user bot via API.
- ⚙️ Background worker processes and fulfills orders.
- 🎁 Send gifts to individual users or public channels.
- 👥 Role system:
  - receiver: can only receive gifts.
  - buyer: can create orders and charge stars.
  - admin: same as buyer, plus can add/remove users and change roles.
- 📊 View star balances for all users.


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
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir -p data
python src/main.py
```

#### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdir data
python src\main.py
```


## Docker Setup

You can also run the bot using Docker. Follow these steps:


1. Rename `.env.example` to `.env` and update the environment variables as needed

2. Build and run the Docker containers using Docker Compose:
```bash
docker compose up --build -d
```
## Notes

- To add a **channel** as a receiver: add the bot to the channel and send `/start` command from that channel.  
- Orders and star balances are persisted in `data/app.db`.  

## License

MIT