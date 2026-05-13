@echo off
echo.
echo ========================================
echo    AgentX Auto Deploy Script
echo ========================================
echo.

echo [1/4] Activating virtual environment...
call venv\Scripts\activate

echo [2/4] Installing dependencies...
pip install -r requirements.txt --quiet

echo [3/4] Pushing to GitHub...
git add .
set msg=Auto deploy update
git commit -m "%msg%"
git push

echo [4/4] Done!
echo.
echo ========================================
echo    GitHub push complete!
echo    Render will auto-deploy in 2-3 mins
echo    URL: https://agentx-hat8.onrender.com
echo ========================================
echo.
pause