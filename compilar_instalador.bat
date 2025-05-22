@echo off
echo Compilando o instalador do Gerenciador de Spam...
echo.

REM Tenta encontrar o compilador do Inno Setup em locais comuns
set ISCC_PATHS=^
"C:\Program Files\Inno Setup 6\ISCC.exe" ^
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" ^
"C:\Program Files\Inno Setup 5\ISCC.exe" ^
"C:\Program Files (x86)\Inno Setup 5\ISCC.exe"

set ISCC_FOUND=0

for %%i in (%ISCC_PATHS%) do (
    if exist %%i (
        echo Compilador do Inno Setup encontrado: %%i
        echo.
        echo Compilando o script GerenciadorDeSpam.iss...
        %%i GerenciadorDeSpam.iss
        set ISCC_FOUND=1
        goto :DONE
    )
)

if %ISCC_FOUND%==0 (
    echo Compilador do Inno Setup nao encontrado nos locais comuns.
    echo.
    echo Por favor, informe o caminho completo para o ISCC.exe:
    set /p ISCC_PATH=
    
    if exist "%ISCC_PATH%" (
        echo.
        echo Compilando o script GerenciadorDeSpam.iss...
        "%ISCC_PATH%" GerenciadorDeSpam.iss
    ) else (
        echo.
        echo Arquivo nao encontrado: %ISCC_PATH%
        echo Compilacao cancelada.
        goto :ERROR
    )
)

:DONE
if exist instalador\GerenciadorDeSpam_Setup.exe (
    echo.
    echo Instalador criado com sucesso!
    echo Arquivo: instalador\GerenciadorDeSpam_Setup.exe
) else (
    echo.
    echo Erro ao criar o instalador.
    goto :ERROR
)

goto :END

:ERROR
echo.
echo Para compilar manualmente:
echo 1. Abra o Inno Setup Compiler
echo 2. Abra o arquivo GerenciadorDeSpam.iss
echo 3. Pressione F9 ou clique no botao Compile

:END
echo.
echo Pressione qualquer tecla para sair...
pause > nul
