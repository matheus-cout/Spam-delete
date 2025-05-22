#!/usr/bin/env python3
"""
Script para testar os módulos usados pelo programa.
"""

import sys
import traceback

def test_import(module_name):
    try:
        __import__(module_name)
        print(f"✓ Módulo '{module_name}' importado com sucesso.")
        return True
    except Exception as e:
        print(f"✗ Erro ao importar o módulo '{module_name}': {e}")
        traceback.print_exc()
        return False

def main():
    print("=== Teste de Importação de Módulos ===\n")
    
    # Módulos da biblioteca padrão
    std_modules = [
        "tkinter", "sqlite3", "logging", "threading", 
        "queue", "imaplib", "email", "datetime", 
        "base64", "hashlib", "os", "sys", "time"
    ]
    
    # Módulos de terceiros
    third_party_modules = [
        "cryptography", "cryptography.fernet", 
        "cryptography.hazmat.primitives", 
        "cryptography.hazmat.primitives.kdf.pbkdf2"
    ]
    
    # Módulos do projeto
    project_modules = [
        "credential_prompt", "credentials_manager",
        "delete_spam_emails", "check_spam_count",
        "verificar_spam", "gui_app"
    ]
    
    # Testar módulos da biblioteca padrão
    print("Testando módulos da biblioteca padrão:")
    std_success = all(test_import(module) for module in std_modules)
    print()
    
    # Testar módulos de terceiros
    print("Testando módulos de terceiros:")
    third_party_success = all(test_import(module) for module in third_party_modules)
    print()
    
    # Testar módulos do projeto
    print("Testando módulos do projeto:")
    project_success = all(test_import(module) for module in project_modules)
    print()
    
    # Resumo
    print("=== Resumo ===")
    print(f"Módulos da biblioteca padrão: {'OK' if std_success else 'FALHA'}")
    print(f"Módulos de terceiros: {'OK' if third_party_success else 'FALHA'}")
    print(f"Módulos do projeto: {'OK' if project_success else 'FALHA'}")
    
    # Manter o terminal aberto para ver o resultado
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
