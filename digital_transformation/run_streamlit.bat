@echo off
echo Digital Transformation Planner Launcher

REM Check if virtual environment exists and activate it
if exist .venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

REM Install requirements if needed
echo Checking requirements...
pip install -r requirements.txt

REM Run the Streamlit app
echo Starting Digital Transformation Planner...
streamlit run app.py

pause 