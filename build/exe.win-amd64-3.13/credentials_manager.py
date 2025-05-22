#!/usr/bin/env python3
"""
Gerenciador de Credenciais para o Deletador de Emails

Este módulo gerencia o armazenamento seguro de credenciais do Gmail em um banco de dados SQLite3.
As senhas são criptografadas antes de serem armazenadas.
"""

import sqlite3
import os
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Diretório para armazenar o banco de dados
DATA_DIR = "data"
DB_FILE = os.path.join(DATA_DIR, "credentials.db")
KEY_FILE = os.path.join(DATA_DIR, "key.bin")

# Garantir que o diretório de dados exista
os.makedirs(DATA_DIR, exist_ok=True)

def generate_key():
    """Gera uma chave de criptografia e a salva em um arquivo."""
    # Usar um salt fixo para consistência (não é o ideal para segurança máxima,
    # mas simplifica o uso para este aplicativo)
    salt = b'deletador_de_emails_salt'
    
    # Derivar uma chave a partir de uma senha mestra
    # Em um cenário real, você poderia solicitar esta senha ao usuário
    password = b"senha_mestra_do_aplicativo"
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password))
    
    # Salvar a chave em um arquivo
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    
    return key

def get_encryption_key():
    """Obtém a chave de criptografia do arquivo ou gera uma nova se não existir."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    else:
        key = generate_key()
    
    return key

def encrypt_password(password):
    """Criptografa uma senha usando Fernet (criptografia simétrica)."""
    key = get_encryption_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password):
    """Descriptografa uma senha criptografada."""
    key = get_encryption_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password)
    return decrypted_password.decode()

def initialize_database():
    """Inicializa o banco de dados SQLite3 com a tabela de credenciais."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Criar tabela de credenciais se não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS credentials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL,
        last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def save_credentials(email, password):
    """Salva ou atualiza as credenciais no banco de dados."""
    # Criptografar a senha
    encrypted_password = encrypt_password(password)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Inserir ou atualizar as credenciais
    cursor.execute('''
    INSERT OR REPLACE INTO credentials (email, password, last_used)
    VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', (email, encrypted_password))
    
    conn.commit()
    conn.close()
    
    return True

def get_credentials(email=None):
    """
    Recupera as credenciais do banco de dados.
    Se email for None, retorna as credenciais mais recentemente usadas.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    if email:
        cursor.execute('SELECT email, password FROM credentials WHERE email = ?', (email,))
    else:
        cursor.execute('SELECT email, password FROM credentials ORDER BY last_used DESC LIMIT 1')
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        email, encrypted_password = result
        password = decrypt_password(encrypted_password)
        return email, password
    
    return None, None

def list_saved_emails():
    """Retorna uma lista de emails salvos no banco de dados."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT email FROM credentials ORDER BY last_used DESC')
    emails = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return emails

def update_last_used(email):
    """Atualiza o timestamp de último uso para um email específico."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('UPDATE credentials SET last_used = CURRENT_TIMESTAMP WHERE email = ?', (email,))
    
    conn.commit()
    conn.close()

# Inicializar o banco de dados ao importar o módulo
initialize_database()

if __name__ == "__main__":
    # Código de teste
    print("Testando o gerenciador de credenciais...")
    
    # Salvar algumas credenciais de teste
    save_credentials("teste@gmail.com", "senha_teste")
    print("Credenciais salvas com sucesso!")
    
    # Recuperar as credenciais
    email, password = get_credentials("teste@gmail.com")
    print(f"Credenciais recuperadas: {email}, {password}")
    
    # Listar emails salvos
    emails = list_saved_emails()
    print(f"Emails salvos: {emails}")
