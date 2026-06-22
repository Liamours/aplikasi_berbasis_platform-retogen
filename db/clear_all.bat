@echo off
echo ==============================
echo  Clear Semua Collection Atlas
echo ==============================

set /p MONGO_URI="Masukkan MONGO_URI: "

python "%~dp0clear_articles.py"

pause
