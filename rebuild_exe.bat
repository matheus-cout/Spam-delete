@echo off
title Rebuild - Gerenciador de Spam do Gmail
echo ========================================
echo  Rebuild do Executavel
echo  Gerenciador de Spam do Gmail
echo ========================================
echo.

echo Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

echo.
echo Criando novo executavel com PyInstaller...
echo.

python build_final.py

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao criar o executavel!
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Executavel criado com sucesso!
echo ========================================
echo.
echo Arquivo: dist\GerenciadorSpamGmail.exe
echo.
echo Testando o executavel...
echo.

start "" "dist\GerenciadorSpamGmail.exe"

echo.
echo Pressione qualquer tecla para sair...
pause >nul
