@echo off
setlocal

echo Creating virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Creating data directory...
if not exist data mkdir data

echo Setup completed successfully!
echo.
echo To start the bot, activate your virtual environment first:
echo    call .venv\Scripts\activate.bat
echo Then run:
echo    Scripts\start-bot.bat
