@echo off
echo ========================================
echo  Gerenciador de Spam do Gmail - Build
echo ========================================
echo.

echo Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo Verificando dependencias...
python -c "import cx_Freeze; print('cx_Freeze OK')" 2>nul
if errorlevel 1 (
    echo ERRO: cx_Freeze nao encontrado. Instalando...
    pip install cx_Freeze
    if errorlevel 1 (
        echo ERRO: Falha ao instalar cx_Freeze
        pause
        exit /b 1
    )
)

echo.
echo Iniciando build...
python setup_simple.py build

if errorlevel 1 (
    echo.
    echo ERRO: Falha no build!
    echo Verifique os logs acima para mais detalhes.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Build concluido com sucesso!
echo ========================================
echo.
echo O executavel foi criado em: build\exe\
echo.
echo Testando o executavel...
cd build\exe
GerenciadorSpamGmail.exe
cd ..\..

echo.
echo Pressione qualquer tecla para sair...
pause >nul
