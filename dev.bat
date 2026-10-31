@echo off
title FilmAura Live Dev Mode
echo ========================================================
echo   Starting FilmAura Live Development Mode
echo   Backend API: http://localhost:8000
echo   React Vite Dev: http://localhost:5173
echo ========================================================
start "FilmAura Backend" "C:\Users\Admin\AppData\Local\Programs\Python\Python311\python.exe" server.py
cd frontend
start http://localhost:5173
npm.cmd run dev
