# Como Compilar o Instalador Manualmente

Este guia explica como compilar o instalador do Gerenciador de Spam manualmente usando o Inno Setup.

## Método 1: Usando o Script Automatizado

Foi criado um script batch (`compilar_instalador.bat`) que tenta encontrar automaticamente o compilador do Inno Setup e compilar o instalador.

1. Dê um duplo clique no arquivo `compilar_instalador.bat`
2. O script tentará encontrar o compilador do Inno Setup em locais comuns
3. Se encontrado, o script compilará automaticamente o instalador
4. Se não encontrado, o script solicitará que você informe o caminho completo para o executável `ISCC.exe`

## Método 2: Usando o Inno Setup Compiler (Interface Gráfica)

Se o método automatizado não funcionar, você pode compilar o instalador manualmente usando a interface gráfica do Inno Setup:

1. Abra o Inno Setup Compiler (geralmente disponível no menu Iniciar)
2. No menu, selecione `File` > `Open` e navegue até o arquivo `GerenciadorDeSpam.iss`
3. O script será aberto no editor do Inno Setup
4. Pressione F9 ou clique no botão `Compile` (ícone de engrenagem verde) na barra de ferramentas
5. O Inno Setup irá compilar o script e criar o instalador
6. Se não houver erros, uma mensagem de sucesso será exibida
7. O instalador será criado na pasta `instalador` com o nome `GerenciadorDeSpam_Setup.exe`

## Método 3: Usando o Compilador de Linha de Comando

Se você souber o caminho exato para o compilador do Inno Setup, pode executá-lo diretamente:

1. Abra o Prompt de Comando (CMD)
2. Navegue até a pasta onde está o arquivo `GerenciadorDeSpam.iss`
3. Execute o comando:
   ```
   "C:\Caminho\Para\ISCC.exe" GerenciadorDeSpam.iss
   ```
   Substitua `C:\Caminho\Para\ISCC.exe` pelo caminho real para o executável `ISCC.exe`

## Locais Comuns do Compilador do Inno Setup

O compilador do Inno Setup (`ISCC.exe`) geralmente está localizado em um dos seguintes caminhos:

- `C:\Program Files\Inno Setup 6\ISCC.exe`
- `C:\Program Files (x86)\Inno Setup 6\ISCC.exe`
- `C:\Program Files\Inno Setup 5\ISCC.exe`
- `C:\Program Files (x86)\Inno Setup 5\ISCC.exe`

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

### Erro: Compilador não encontrado

Se você não conseguir encontrar o compilador do Inno Setup:

1. Verifique se o Inno Setup está instalado corretamente
2. Tente reinstalar o Inno Setup
3. Use a ferramenta de busca do Windows para procurar por `ISCC.exe`

## Após a Compilação

Após compilar o instalador com sucesso:

1. O instalador será criado na pasta `instalador` com o nome `GerenciadorDeSpam_Setup.exe`
2. Você pode executar o instalador para instalar o aplicativo
3. Você pode distribuir o instalador para outros usuários

## Recursos Adicionais

- [Documentação oficial do Inno Setup](https://jrsoftware.org/ishelp/)
- [Exemplos de scripts do Inno Setup](https://jrsoftware.org/ishelp/index.php?topic=examples)
- [Fórum do Inno Setup](https://jrsoftware.org/forums.php)
