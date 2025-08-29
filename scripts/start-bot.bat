@echo off
setlocal

set /p choice=Do you want to connect your account? (yes/no): 

if /i "%choice%"=="yes" (
    echo Running login_once.py...
    python src\login_once.py
) else if /i "%choice%"=="y" (
    echo Running login_once.py...
    python src\login_once.py
) else (
    echo Skipping userbot setup.
)

echo Starting main bot...
python src\main.py
