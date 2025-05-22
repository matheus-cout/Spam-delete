#!/usr/bin/env python3
"""
Verificador de Emails de Spam do Gmail

Este script tenta se conectar ao Gmail via IMAP para verificar a quantidade de emails na pasta de spam.
É uma versão simplificada que usa um timeout mais curto e tratamento de erros aprimorado.

Uso:
    python verificar_spam.py
"""

import imaplib
import socket
import time
import sys

def verificar_pasta_spam():
    """Conecta ao Gmail e verifica a quantidade de emails na pasta de spam."""
    
    # Configurações da conta Gmail
    username = "souzasoftm@gmail.com"
    password = "xmxsgunchbfavftq"  # Senha de app, não a senha regular do Gmail
    imap_server = "imap.gmail.com"
    pasta_spam = "[Gmail]/Spam"
    
    # Configurar timeout para operações de socket
    socket.setdefaulttimeout(15)  # 15 segundos de timeout
    
    print("=== Verificador de Emails de Spam do Gmail ===")
    print(f"Tentando conectar à conta: {username}")
    
    try:
        # Conectar ao servidor IMAP
        print(f"Conectando ao servidor {imap_server}...")
        mail = imaplib.IMAP4_SSL(imap_server)
        print("Conexão estabelecida com sucesso")
        
        # Fazer login
        print("Fazendo login...")
        mail.login(username, password)
        print("Login realizado com sucesso")
        
        # Selecionar a pasta de spam
        print(f"Selecionando pasta: {pasta_spam}")
        status, mensagens = mail.select(pasta_spam, readonly=True)
        
        if status != 'OK':
            print(f"Erro ao selecionar a pasta {pasta_spam}")
            mail.logout()
            return
        
        # Obter a quantidade de emails
        print("Contando emails...")
        status, mensagens = mail.search(None, 'ALL')
        
        if status != 'OK':
            print("Erro ao buscar emails")
            mail.logout()
            return
        
        # Contar emails
        ids_emails = mensagens[0].split()
        quantidade = len(ids_emails)
        
        # Mostrar resultado
        print(f"\nQuantidade de emails na pasta {pasta_spam}: {quantidade}")
        
        # Fazer logout
        mail.logout()
        print("Logout realizado com sucesso")
        
    except socket.timeout:
        print("Erro: Tempo de conexão esgotado. A operação demorou muito para ser concluída.")
    except imaplib.IMAP4.error as e:
        print(f"Erro IMAP: {e}")
    except Exception as e:
        print(f"Erro: {e}")
    
    print("\nExecução do script concluída")

if __name__ == "__main__":
    # Registrar o tempo de início
    tempo_inicio = time.time()
    
    # Executar a verificação
    verificar_pasta_spam()
    
    # Mostrar o tempo total de execução
    tempo_total = time.time() - tempo_inicio
    print(f"Tempo total de execução: {tempo_total:.2f} segundos")
