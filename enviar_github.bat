@echo off
chcp 65001 >nul
REM ============================================================
REM  Envia este projeto para o seu GitHub.
REM  1) Crie um repositorio VAZIO em https://github.com/new
REM     (nome sugerido: debate-politico, sem README)
REM  2) De dois cliques neste arquivo e cole a URL do repositorio.
REM ============================================================
cd /d "%~dp0"

where git >nul 2>nul
if errorlevel 1 (
  echo Git nao encontrado. Instale em https://git-scm.com/download/win e rode de novo.
  pause
  exit /b 1
)

set /p REPO="Cole a URL do repositorio (ex: https://github.com/SEU_USUARIO/debate-politico.git): "

git config user.name >nul 2>nul
if errorlevel 1 goto pedir_nome
goto checar_email
:pedir_nome
set /p NOME="Seu nome para o git: "
git config --global user.name "%NOME%"
:checar_email
git config user.email >nul 2>nul
if errorlevel 1 goto pedir_email
goto enviar
:pedir_email
set /p EMAIL="Seu e-mail do GitHub: "
git config --global user.email "%EMAIL%"
:enviar

git remote remove origin >nul 2>nul
git remote add origin %REPO%
git branch -M main
git push -u origin main

echo.
echo Pronto! Abra %REPO% no navegador para conferir.
pause
