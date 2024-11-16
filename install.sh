#!/bin/bash

# Verificar se o Python3 está instalado
echo "Verificando se o Python 3 está instalado..."

# Se o Python3 não estiver instalado, instala o Python3
if ! command -v python3 &> /dev/null
then
    echo "Python 3 não encontrado, instalando..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-dev python3-venv
else
    echo "Python 3 já está instalado."
fi

# Verificar se o pip está instalado
echo "Verificando se o pip está instalado..."

# Se o pip não estiver instalado, instala o pip
if ! command -v pip3 &> /dev/null
then
    echo "pip não encontrado, instalando..."
    sudo apt-get install -y python3-pip
else
    echo "pip já está instalado."
fi

# Instala dependências do sistema
echo "Instalando dependências do sistema..."

# Para Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3-tk

# Instala as dependências do Python
echo "Instalando dependências do Python..."
pip3 install -r requirements.txt

echo "Instalação concluída!"
