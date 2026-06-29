@echo off
:: Navigate to your project directory
cd /d "C:\Users\casti\OneDrive\Desktop\Tech Job Market Tracker"

:: Activate your virtual environment
call .venv\Scripts\activate

:: Execute the scraper command
python manage.py scrape_jobs

:: Deactivate the virtual environment and close cleanly
call deactivate
exit
