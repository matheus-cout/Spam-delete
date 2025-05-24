# Gerenciador de Spam do Gmail

Este programa permite deletar emails de spam do Gmail de forma automatizada, com interface gráfica amigável.

## Funcionalidades

- Interface gráfica intuitiva
- Autenticação segura com OAuth2
- Salvamento seguro de credenciais com criptografia
- Contagem de emails de spam
- Verificação de emails de spam
- Exclusão automática de emails de spam
- Logs detalhados de operações

## Requisitos

- Python 3.7 ou superior
- Conta do Gmail com API habilitada
- Arquivo `credentials.json` do Google Cloud Console

## Instalação e Execução

### Opção 1: Execução Direta (Recomendado)

1. **Verificar e instalar dependências:**
   - Execute `install_dependencies.bat` (Windows) ou `python install_dependencies.py`
   - O script verificará e instalará automaticamente as dependências necessárias

2. **Executar o programa:**
   - Execute `run_app.bat` (Windows) ou `python launcher.py`

### Opção 2: Instalação Manual

1. Clone este repositório
2. Instale as dependências:
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests cryptography
   ```
3. Execute o programa:
   ```bash
   python launcher.py
   ```

### Opção 3: Criar Executável (RESOLVIDO!)

✅ **Usando PyInstaller (Funcionando perfeitamente):**

**Método 1 - Script automático:**
```bash
python build_pyinstaller.py
```

**Método 2 - Comando direto:**
```bash
pyinstaller --onefile --windowed --name=GerenciadorSpamGmail launcher.py
```

**Método 3 - Script batch (Windows):**
```bash
rebuild_exe.bat
```

O executável será criado em: `dist/GerenciadorSpamGmail.exe`

**Para executar o programa compilado:**
- Execute `executar_programa.bat` ou
- Execute diretamente `dist/GerenciadorSpamGmail.exe`

2. **Usando cx_Freeze (Alternativo):**
   - Execute `build.bat` ou `python setup_simple.py build`
   - O executável será criado na pasta `build/exe/`

## Configuração do Google Cloud Console

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Habilite a Gmail API
4. Crie credenciais OAuth 2.0
5. Baixe o arquivo `credentials.json` e coloque na pasta do projeto

## Uso

1. Execute o programa usando um dos métodos acima
2. Na primeira execução, você será solicitado a inserir email e senha
3. As credenciais serão salvas de forma segura e criptografada
4. Use a interface para verificar e deletar emails de spam

## Arquivos Importantes

- `launcher.py` - Script principal de inicialização
- `gui_app.py` - Interface gráfica principal
- `credentials_manager.py` - Gerenciamento seguro de credenciais
- `delete_spam_emails.py` - Lógica de exclusão de spam
- `run_app.bat` - Script para execução direta no Windows
- `install_dependencies.bat` - Script para instalação de dependências

## Segurança

- As credenciais são criptografadas antes de serem salvas
- Usa autenticação OAuth2 oficial do Google
- Não armazena senhas em texto plano
- Banco de dados SQLite3 com criptografia

## Logs

Os logs são salvos na pasta `logs/` e incluem:
- Operações de autenticação
- Contagem de emails
- Operações de exclusão
- Erros e exceções

## ✅ PROBLEMA RESOLVIDO - Erro do cx_Freeze

**Problema Original:**
```
cx_Freeze Python error in main script
Traceback (most recent call last):
  File "frozen.py", line 15, in <module>
  File "__startup__.py", line 50, in <module>
  ...
  PermissionError/Acesso Negado: logs
```

**✅ SOLUÇÃO IMPLEMENTADA:**

O erro foi completamente resolvido usando **PyInstaller** em vez do cx_Freeze. O PyInstaller é mais estável e compatível.

**Como usar a solução:**

1. **Para criar o executável:**
   ```bash
   pyinstaller --onefile --windowed --name=GerenciadorSpamGmail launcher.py
   ```
   ou execute `rebuild_exe.bat`

2. **Para executar:**
   - Execute `executar_programa.bat` ou
   - Execute diretamente `dist/GerenciadorSpamGmail.exe`

**O executável agora funciona perfeitamente sem erros!**

## Solução de Problemas

1. **Erro de módulos não encontrados:**
   - Execute `install_dependencies.bat` para instalar dependências

2. **Erro de autenticação:**
   - Verifique se o arquivo `credentials.json` está presente
   - Verifique se a Gmail API está habilitada no Google Cloud Console

3. **Erro ao criar executável:**
   - ✅ **RESOLVIDO:** Use o PyInstaller: `python build_pyinstaller.py` ou `rebuild_exe.bat`

4. **Programa não inicia:**
   - Verifique os logs na pasta `logs/`
   - Execute `python launcher.py` diretamente para ver erros
