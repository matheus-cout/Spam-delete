@echo off
title Gerenciador de Spam do Gmail
echo ========================================
echo  Gerenciador de Spam do Gmail
echo  Executavel Compilado
echo ========================================
echo.

if not exist "dist\GerenciadorSpamGmail.exe" (
    echo ERRO: Executavel nao encontrado!
    echo.
    echo O executavel deve estar em: dist\GerenciadorSpamGmail.exe
    echo.
    echo Para criar o executavel, execute:
    echo   python build_pyinstaller.py
    echo   ou
    echo   pyinstaller --onefile --windowed --name=GerenciadorSpamGmail launcher.py
    echo.
    pause
    exit /b 1
)

echo Iniciando o Gerenciador de Spam do Gmail...
echo.

start "" "dist\GerenciadorSpamGmail.exe"

echo Programa iniciado com sucesso!
echo.
echo Se houver algum problema, verifique os logs na pasta 'logs\'
echo.
pause
