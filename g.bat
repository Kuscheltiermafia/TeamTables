@echo off
if "%1"=="" (
echo.
echo Error: No commit message provided.
echo Usage: %0 Your commit message here
goto :eof
)

echo.
echo Staging changes...
git add .

echo.
echo Committing changes with message: "%*"
git commit -m "%*"

echo.
echo Pushing to remote repository...
git push

echo.
echo Done! All changes have been committed and pushed.