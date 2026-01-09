@echo off
echo Initializing Metabolomics Imputation Project...

REM Create project structure
echo Creating directory structure...
mkdir data\raw 2>nul
mkdir data\processed 2>nul
mkdir data\results 2>nul
mkdir results\figures 2>nul
mkdir results\tables 2>nul
mkdir logs 2>nul
mkdir src\preprocessing 2>nul
mkdir src\imputation 2>nul
mkdir src\evaluation 2>nul
mkdir src\utils 2>nul
mkdir notebooks 2>nul
mkdir tests 2>nul
mkdir docs 2>nul

REM Create .gitkeep files
type nul > data\raw\.gitkeep
type nul > data\processed\.gitkeep
type nul > data\results\.gitkeep
type nul > results\figures\.gitkeep
type nul > results\tables\.gitkeep
type nul > logs\.gitkeep

REM Create __init__.py files
echo Creating Python package files...
type nul > src\__init__.py
type nul > src\preprocessing\__init__.py
type nul > src\imputation\__init__.py
type nul > src\evaluation\__init__.py
type nul > src\utils\__init__.py
type nul > tests\__init__.py

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Install package in development mode
echo Installing package in development mode...
pip install -e .

echo.
echo Project setup complete!
echo.
echo Next steps:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Place your mzML files in data\raw\
echo 3. Review and customize config.yaml
echo 4. Start with notebooks\01_data_exploration.ipynb
echo.
echo Happy analyzing!
pause
