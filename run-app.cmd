@echo off
setlocal
cd /d "%~dp0"
start "" /B "%~dp0\node_modules\.bin\electron.cmd" "%~dp0"
