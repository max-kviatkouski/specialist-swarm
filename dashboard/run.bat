@echo off
REM ====================================================================
REM  AI Wealth Advisory — Case Console (Windows launcher)
REM  Easiest option: just DOUBLE-CLICK index.html instead of this.
REM  This script serves the folder on http://localhost:8000 and opens it.
REM ====================================================================
cd /d "%~dp0"
echo Opening the dashboard at http://localhost:8000/index.html ...
start "" http://localhost:8000/index.html
where py >nul 2>nul && (py -m http.server 8000) || (python -m http.server 8000)
