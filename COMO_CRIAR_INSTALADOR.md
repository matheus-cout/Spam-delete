# Como Criar um Instalador para o Gerenciador de Spam

Este guia explica como criar um instalador profissional para o Gerenciador de Spam usando o Inno Setup.

## Passo 1: Baixar e Instalar o Inno Setup

1. Acesse o site oficial do Inno Setup: [https://jrsoftware.org/isdl.php](https://jrsoftware.org/isdl.php)
2. Baixe a versão mais recente do Inno Setup (atualmente 6.4.3)
3. Execute o arquivo baixado (`innosetup-6.4.3.exe`) e siga as instruções de instalação

## Passo 2: Abrir o Script de Configuração

Um arquivo de script do Inno Setup (`GerenciadorDeSpam.iss`) já foi criado para você. Este arquivo contém todas as configurações necessárias para criar um instalador profissional.

1. Abra o Inno Setup Compiler (instalado no passo anterior)
2. No menu, selecione `File` > `Open` e navegue até o arquivo `GerenciadorDeSpam.iss`
3. O script será aberto no editor do Inno Setup

## Passo 3: Personalizar o Script (Opcional)

Você pode personalizar o script de acordo com suas necessidades:

### Informações Básicas

No início do arquivo, você pode editar as seguintes definições:

```
#define MyAppName "Gerenciador de Spam do Gmail"
#define MyAppVersion "1.0"
#define MyAppPublisher "Seu Nome ou Empresa"
#define MyAppURL "https://seusite.com.br"
```

Substitua "Seu Nome ou Empresa" pelo seu nome ou nome da sua empresa, e "https://seusite.com.br" pelo seu site (se tiver).

### Gerar um Novo GUID

É recomendável gerar um novo GUID (identificador único) para o seu aplicativo:

1. No Inno Setup Compiler, vá para `Tools` > `Generate GUID`
2. Clique em `Copy` para copiar o GUID gerado
3. Substitua o GUID existente na linha `AppId={{A1B2C3D4-E5F6-4A5B-9C8D-7E6F5A4B3C2D}` pelo novo GUID

### Adicionar um Ícone (Opcional)

Se você tiver um ícone personalizado para o seu aplicativo:

1. Adicione a seguinte linha na seção `[Setup]`:
   ```
   SetupIconFile=caminho\para\seu\icone.ico
   ```

2. Para adicionar um ícone ao executável, você precisará modificar o script `setup_exe.py` e recriar o executável antes de compilar o instalador.

## Passo 4: Compilar o Instalador

1. No Inno Setup Compiler, pressione F9 ou clique no botão `Compile` (ícone de engrenagem verde)
2. O Inno Setup irá compilar o script e criar o instalador
3. Se não houver erros, uma mensagem de sucesso será exibida
4. O instalador será criado na pasta `instalador` com o nome `GerenciadorDeSpam_Setup.exe`

## Passo 5: Testar o Instalador

Antes de distribuir o instalador, é importante testá-lo:

1. Execute o arquivo `GerenciadorDeSpam_Setup.exe` criado
2. Siga o assistente de instalação
3. Verifique se o programa é instalado corretamente
4. Teste se o programa funciona após a instalação
5. Teste a desinstalação através do Painel de Controle > Programas e Recursos

## Dicas Adicionais

### Criar uma Pasta para o Instalador

O script está configurado para criar o instalador em uma pasta chamada `instalador`. Certifique-se de que esta pasta existe antes de compilar o script:

```
mkdir instalador
```

### Personalizar a Aparência do Instalador

Você pode personalizar ainda mais a aparência do instalador adicionando:

1. **Imagem de fundo**: Adicione a seguinte linha na seção `[Setup]`:
   ```
   WizardImageFile=caminho\para\sua\imagem.bmp
   ```
   A imagem deve ter 164x314 pixels.

2. **Imagem pequena**: Adicione a seguinte linha na seção `[Setup]`:
   ```
   WizardSmallImageFile=caminho\para\sua\imagem_pequena.bmp
   ```
   A imagem deve ter 55x58 pixels.

### Adicionar Arquivos de Licença

Se você quiser incluir um arquivo de licença que o usuário precisa aceitar durante a instalação:

1. Crie um arquivo de texto com sua licença (por exemplo, `licenca.txt`)
2. Adicione a seguinte linha na seção `[Setup]`:
   ```
   LicenseFile=licenca.txt
   ```

## Solução de Problemas

### Erro: Arquivo não encontrado

Se o compilador não encontrar algum arquivo mencionado no script, verifique:

1. Se o caminho está correto
2. Se o arquivo realmente existe no local especificado
3. Se você tem permissão para acessar o arquivo

### Erro: Não é possível criar a pasta de saída

Se o compilador não conseguir criar o instalador:

1. Verifique se a pasta `instalador` existe
2. Verifique se você tem permissão para escrever nessa pasta
3. Verifique se o arquivo de saída não está sendo usado por outro programa

## Distribuição do Instalador

Após criar e testar o instalador, você pode distribuí-lo:

1. Compartilhe o arquivo `GerenciadorDeSpam_Setup.exe` com seus usuários
2. Considere hospedar o instalador em um site para download
3. Forneça instruções básicas de instalação e uso

## Recursos Adicionais

- [Documentação oficial do Inno Setup](https://jrsoftware.org/ishelp/)
- [Exemplos de scripts do Inno Setup](https://jrsoftware.org/ishelp/index.php?topic=examples)
- [Fórum do Inno Setup](https://jrsoftware.org/forums.php)
