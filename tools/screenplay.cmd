@echo off
rem Screenplay mode: local server + browser tab. Close this window to stop it.
chcp 65001 >nul
cd /d "%~dp0.."
python tools\screenplay\server.py %*
if errorlevel 1 pause
