@echo off
chcp 65001 >nul
REM Instala o Django, cria o banco, popula exemplos e sobe o site.
cd /d "%~dp0"

REM --- acha o Python (python ou py) ---
set PY=
python --version >nul 2>nul && set PY=python
if not defined PY py --version >nul 2>nul && set PY=py
if not defined PY (
  echo [ERRO] Python nao encontrado.
  echo Instale em https://www.python.org/downloads/ e MARQUE "Add python.exe to PATH".
  goto fim
)
echo Usando: %PY%
%PY% --version

REM --- ambiente virtual ---
if not exist venv\Scripts\python.exe (
  echo Criando ambiente virtual...
  %PY% -m venv venv
  if errorlevel 1 ( echo [ERRO] Falha ao criar o venv. & goto fim )
)
set VPY=venv\Scripts\python.exe

echo Instalando Django...
%VPY% -m pip install -r requirements.txt
if errorlevel 1 ( echo [ERRO] Falha ao instalar o Django. Verifique a internet. & goto fim )

%VPY% manage.py migrate
if errorlevel 1 ( echo [ERRO] Falha no migrate. & goto fim )

%VPY% manage.py popular_dados

echo.
echo ============================================================
echo  Site:  http://127.0.0.1:8000/
echo  Admin: http://127.0.0.1:8000/admin/
echo  (para criar login do admin: venv\Scripts\python manage.py createsuperuser)
echo  Deixe ESTA janela aberta enquanto usa o site. Ctrl+C para parar.
echo ============================================================
start "" /min cmd /c "timeout /t 5 >nul & start http://127.0.0.1:8000/"
%VPY% manage.py runserver

:fim
echo.
pause
