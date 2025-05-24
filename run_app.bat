@echo off
title Gerenciador de Spam do Gmail
echo ========================================
echo  Gerenciador de Spam do Gmail
echo ========================================
echo.
echo Iniciando aplicacao...
echo.

python launcher.py

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao executar o programa!
    echo Verifique se o Python esta instalado e as dependencias estao corretas.
    echo.
    pause
)
