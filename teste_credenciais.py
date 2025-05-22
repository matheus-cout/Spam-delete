#!/usr/bin/env python3
"""
Script de teste para o sistema de gerenciamento de credenciais
"""

import credential_prompt
import credentials_manager as cm

def main():
    print("=== Teste do Sistema de Gerenciamento de Credenciais ===")
    
    # Listar credenciais salvas
    saved_emails = cm.list_saved_emails()
    if saved_emails:
        print(f"\nCredenciais salvas: {len(saved_emails)}")
        for i, email in enumerate(saved_emails, 1):
            print(f"{i}. {email}")
    else:
        print("\nNenhuma credencial salva.")
    
    # Solicitar credenciais
    print("\nSolicitando credenciais...")
    email, password = credential_prompt.get_credentials()
    
    print(f"\nCredenciais obtidas: {email}, {'*' * len(password)}")
    
    # Verificar se as credenciais foram salvas
    saved_emails_after = cm.list_saved_emails()
    if len(saved_emails_after) > len(saved_emails):
        print("\nNovas credenciais foram salvas com sucesso!")
    
    print("\nTeste concluído!")

if __name__ == "__main__":
    main()
