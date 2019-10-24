@echo off
call %LOCALAPPDATA%\Continuum\miniconda3\Scripts\activate.bat
if not exist %userprofile%\.cookiecutters (
    call md %userprofile%\.cookiecutters
)
call cd %userprofile%\.cookiecutters
call git clone https://github.com/ciaranjudge/broccolicutter
if %errorlevel% neq 0 (
    echo Arg! Looks like you're behind a corporate firewall.
    echo As a workaround, set git http.sslverify to false.
    call git config --global --replace-all http.sslverify false
    echo ...and try again
    call git clone https://github.com/ciaranjudge/broccolicutter
)

