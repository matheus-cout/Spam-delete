# Exclusão Automática de Emails de Spam no Gmail

Este projeto contém scripts e guias para ajudar a gerenciar automaticamente emails de spam no Gmail.

## Arquivos incluídos

1. `configuracao_exclusao_automatica_spam.md` - Guia detalhado sobre como configurar o Gmail para excluir automaticamente emails de spam usando as configurações nativas do Gmail.

2. `verificar_spam.py` - Script Python para verificar a quantidade de emails na pasta de spam do Gmail.

3. `delete_spam_emails.py` - Script Python para excluir automaticamente todos os emails da pasta de spam do Gmail.

4. `check_spam_count.py` - Script Python para verificar e listar informações sobre os emails na pasta de spam.

## Recomendações

### Método recomendado: Configurações nativas do Gmail

A maneira mais simples e confiável de gerenciar automaticamente emails de spam é usar as configurações nativas do Gmail:

1. Abra o Gmail em seu navegador
2. Clique no ícone de engrenagem (⚙️) no canto superior direito
3. Selecione "Ver todas as configurações"
4. Na aba "Geral", role para baixo até encontrar a seção "Spam"
5. Procure a opção "Excluir mensagens de spam após:" e selecione o período desejado
6. Clique em "Salvar alterações" na parte inferior da página

Para instruções mais detalhadas, consulte o arquivo `configuracao_exclusao_automatica_spam.md`.

### Usando os scripts Python

Os scripts Python incluídos neste projeto podem ser usados para verificar e gerenciar emails de spam, mas podem enfrentar limitações devido às políticas de segurança do Gmail.

#### Requisitos

- Python 3.6 ou superior
- Conta do Gmail com IMAP habilitado
- Senha de aplicativo para o Gmail (se a autenticação de dois fatores estiver ativada)

#### Configuração da senha de aplicativo

Se você usa autenticação de dois fatores no Gmail, precisará criar uma senha de aplicativo:

1. Acesse sua Conta do Google
2. Selecione "Segurança"
3. Em "Como fazer login no Google", selecione "Senhas de app"
4. Gere uma nova senha para o aplicativo "Email" e dispositivo "Outro"
5. Use essa senha nos scripts em vez da sua senha regular do Gmail

## Problemas conhecidos

- Os scripts que usam IMAP podem enfrentar problemas de conexão ou timeout
- O Gmail pode bloquear conexões IMAP de aplicativos menos seguros
- A API do Gmail é uma alternativa mais robusta, mas requer configuração adicional

## Alternativas

Se os scripts não funcionarem conforme o esperado, considere:

1. Usar as configurações nativas do Gmail (recomendado)
2. Criar filtros personalizados no Gmail
3. Usar o aplicativo oficial do Gmail em dispositivos móveis, que oferece opções para gerenciar spam
4. Usar clientes de email de terceiros com recursos avançados de gerenciamento de spam

## Suporte

Se você encontrar problemas ao usar estes scripts ou seguir as instruções, consulte a documentação oficial do Gmail ou entre em contato com o suporte do Google.
