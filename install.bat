@echo off
echo Instalando dependências do sistema...

:: Verifica se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python não encontrado, instalando...
    :: Baixando e instalando o Python
    echo Baixando o Python...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe -OutFile python-installer.exe"
    echo Instalando o Python...
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    :: Verifica se o Python foi instalado corretamente
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Falha ao instalar o Python. Saindo...
        exit /b 1
    )
) else (
    echo Python já está instalado.
)

:: Verifica se o pip está instalado
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip não encontrado, instalando...
    python -m ensurepip --upgrade
)

:: Verifica se o tkinter está instalado
python -m tkinter >nul 2>&1
if %errorlevel% neq 0 (
    echo Tkinter não encontrado, instalando...
    echo O Tkinter já vem com o Python, mas o Python deve ser instalado corretamente.
)

echo Instalando dependências do Python...
pip install -r requirements.txt

echo Instalação concluída!
pause
