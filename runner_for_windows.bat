@echo off
echo Creating virtual environment...
python -m venv venv
echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    exit /b %errorlevel%
)

echo Starting the FastAPI server...
uvicorn app.main:app --reload

pause