# Guia Visual para Compilar o Instalador do Gerenciador de Spam

Este guia passo a passo mostra como compilar o instalador do Gerenciador de Spam usando a interface gráfica do Inno Setup.

## Passo 1: Abrir o Inno Setup Compiler

1. Clique no menu Iniciar do Windows
2. Procure por "Inno Setup Compiler" e clique para abrir
3. A interface do Inno Setup Compiler será exibida

## Passo 2: Abrir o Script do Instalador

1. No menu do Inno Setup, clique em `File` > `Open...` (ou pressione Ctrl+O)
2. Navegue até a pasta onde está o arquivo `GerenciadorDeSpam.iss`
3. Selecione o arquivo e clique em `Open`
4. O script será aberto no editor do Inno Setup

## Passo 3: Compilar o Instalador

1. No menu do Inno Setup, clique em `Build` > `Compile` (ou pressione F9)
2. Alternativamente, clique no botão `Compile` (ícone de engrenagem verde) na barra de ferramentas
3. O Inno Setup começará a compilar o instalador
4. Uma janela de progresso será exibida durante a compilação

## Passo 4: Verificar o Resultado

1. Se a compilação for bem-sucedida, uma mensagem de sucesso será exibida
2. O instalador será criado na pasta `instalador` com o nome `GerenciadorDeSpam_Setup.exe`
3. Você pode clicar em `Close` para fechar a mensagem de sucesso

## Passo 5: Localizar o Instalador

1. Navegue até a pasta `instalador` no seu projeto
2. Você encontrará o arquivo `GerenciadorDeSpam_Setup.exe`
3. Este é o instalador que você pode distribuir para os usuários

## Solução de Problemas

### Erro: Pasta de saída não encontrada

Se você receber um erro indicando que a pasta de saída não existe:

1. Feche a mensagem de erro
2. Crie manualmente a pasta `instalador` no mesmo diretório do arquivo `GerenciadorDeSpam.iss`
3. Tente compilar novamente

### Erro: Arquivo não encontrado

Se o compilador não encontrar algum arquivo mencionado no script:

1. Verifique se todos os arquivos mencionados no script existem nos locais especificados
2. Verifique especialmente os arquivos na seção `[Files]` do script
3. Corrija os caminhos no script se necessário
4. Tente compilar novamente

### Erro: Permissão negada

Se você receber um erro de permissão:

1. Feche o Inno Setup Compiler
2. Clique com o botão direito no ícone do Inno Setup Compiler
3. Selecione "Executar como administrador"
4. Abra o script e tente compilar novamente

## Testando o Instalador

Após criar o instalador com sucesso:

1. Execute o arquivo `GerenciadorDeSpam_Setup.exe`
2. Siga o assistente de instalação
3. Verifique se o programa é instalado corretamente
4. Teste se o programa funciona após a instalação

## Distribuindo o Instalador

Para distribuir o instalador para outros usuários:

1. Copie o arquivo `GerenciadorDeSpam_Setup.exe` para um dispositivo de armazenamento ou serviço de compartilhamento
2. Forneça instruções básicas de instalação
3. Os usuários podem executar o instalador para instalar o aplicativo em seus computadores
