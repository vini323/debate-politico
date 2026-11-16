@echo off
chcp 65001 >nul
REM Instala o Django, cria o banco, popula exemplos e sobe o site.
cd /d "%~dp0"
if not exist venv (
  python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py popular_dados
echo.
echo Para criar o login do Admin rode:  venv\Scripts\python manage.py createsuperuser
echo Site em http://127.0.0.1:8000/   ^|   Admin em http://127.0.0.1:8000/admin/
echo.
python manage.py runserver
