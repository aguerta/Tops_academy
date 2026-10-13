@echo off
setlocal
set "ROOT=%~dp0"
if exist "%ROOT%.venv\Scripts\python.exe" (
    "%ROOT%.venv\Scripts\python.exe" -m pytest %*
) else if exist "%ROOT%.venv\Scripts\pytest.exe" (
    "%ROOT%.venv\Scripts\pytest.exe" %*
) else (
    python "%ROOT%run_tests.py" %*
)
exit /b %ERRORLEVEL%
