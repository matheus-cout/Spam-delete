# Script PowerShell para compilar o instalador do Gerenciador de Spam

Write-Host "Compilando o instalador do Gerenciador de Spam..." -ForegroundColor Green
Write-Host ""

# Tenta encontrar o compilador do Inno Setup em locais comuns
$isccPaths = @(
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 5\ISCC.exe",
    "C:\Program Files (x86)\Inno Setup 5\ISCC.exe"
)

$isccFound = $false

foreach ($path in $isccPaths) {
    if (Test-Path $path) {
        Write-Host "Compilador do Inno Setup encontrado: $path" -ForegroundColor Green
        Write-Host ""
        Write-Host "Compilando o script GerenciadorDeSpam.iss..." -ForegroundColor Yellow
        
        # Executa o compilador
        & $path "GerenciadorDeSpam.iss"
        
        $isccFound = $true
        break
    }
}

if (-not $isccFound) {
    Write-Host "Compilador do Inno Setup não encontrado nos locais comuns." -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor, informe o caminho completo para o ISCC.exe:" -ForegroundColor Yellow
    $isccPath = Read-Host
    
    if (Test-Path $isccPath) {
        Write-Host ""
        Write-Host "Compilando o script GerenciadorDeSpam.iss..." -ForegroundColor Yellow
        
        # Executa o compilador
        & $isccPath "GerenciadorDeSpam.iss"
    }
    else {
        Write-Host ""
        Write-Host "Arquivo não encontrado: $isccPath" -ForegroundColor Red
        Write-Host "Compilação cancelada." -ForegroundColor Red
        
        Write-Host ""
        Write-Host "Para compilar manualmente:" -ForegroundColor Yellow
        Write-Host "1. Abra o Inno Setup Compiler" -ForegroundColor Yellow
        Write-Host "2. Abra o arquivo GerenciadorDeSpam.iss" -ForegroundColor Yellow
        Write-Host "3. Pressione F9 ou clique no botão Compile" -ForegroundColor Yellow
        
        Read-Host "Pressione Enter para sair"
        exit
    }
}

# Verifica se o instalador foi criado com sucesso
if (Test-Path "instalador\GerenciadorDeSpam_Setup.exe") {
    Write-Host ""
    Write-Host "Instalador criado com sucesso!" -ForegroundColor Green
    Write-Host "Arquivo: instalador\GerenciadorDeSpam_Setup.exe" -ForegroundColor Green
}
else {
    Write-Host ""
    Write-Host "Erro ao criar o instalador." -ForegroundColor Red
    
    Write-Host ""
    Write-Host "Para compilar manualmente:" -ForegroundColor Yellow
    Write-Host "1. Abra o Inno Setup Compiler" -ForegroundColor Yellow
    Write-Host "2. Abra o arquivo GerenciadorDeSpam.iss" -ForegroundColor Yellow
    Write-Host "3. Pressione F9 ou clique no botão Compile" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Pressione Enter para sair"
