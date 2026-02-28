@echo off
REM change to project directory
cd /d C:\Users\tent9\OneDrive\Desktop\DMBI_Project
REM run pipeline and append both stdout/stderr to fetch.log
python fetch_youtube.py >> C:\Users\tent9\OneDrive\Desktop\DMBI_Project\fetch.log 2>&1
