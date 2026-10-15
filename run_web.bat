@echo off
title Web Monitoring Air IoT
echo ========================================================
echo   MENJALANKAN WEB MONITORING AIR IoT (STREAMLIT)
echo ========================================================
echo.
echo Sedang mengaktifkan server web lokal... Mohon tunggu sebentar...
echo Browser Anda akan terbuka secara otomatis di http://localhost:8501
echo.

cd /d "%~dp0"

if exist "%~dp0venv\Scripts\python.exe" (
    "%~dp0venv\Scripts\python.exe" -m streamlit run app.py
) else (
    python -m streamlit run app.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================================
    echo   Gagal membuka dengan interpreter venv.
    echo   Mencoba dengan Python global...
    echo ========================================================
    python -m streamlit run app.py
)

pause
