@echo off
REM Stop script for Windows
REM Stops and removes the Docker container

echo Stopping container...
docker stop pm-kanban 2>nul || echo Container not running

echo Removing container...
docker rm pm-kanban 2>nul || echo Container not found

echo Container stopped and removed successfully!
pause
