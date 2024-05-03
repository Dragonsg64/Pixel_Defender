@echo off

rem Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installé. Installation en cours...
    REM Télécharger et installer Python 3.11.9
    bitsadmin /transfer pythonDownloadJob /download /priority normal https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe %TEMP%\python-3.12.3-amd64.exe
    %TEMP%\python-3.12.3-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_launcher=1
) else (
    echo python est bien installer
)

rem Vérifier si Pygame est installé
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo Pygame n'est pas installé. Installation en cours...
    REM Installer Pygame
    python -m pip install pygame
) else (
    echo pygame est bien installer
)

rem Vérifier si tkinter est installé
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo tkinter n'est pas installé. Installation en cours...
    REM Installer tkinter
    python -m pip install tkinter
) else (
    echo tkinter est bien installer
)

rem Lancer votre jeu
python page_de_connexion/login.py

pause