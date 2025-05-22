#!/usr/bin/env python3
"""
Interface para gerenciamento de credenciais do Gmail

Este módulo fornece funções para solicitar, salvar e recuperar credenciais do Gmail.
"""

import os
import getpass
import credentials_manager as cm

def prompt_credentials(use_saved=True):
    """
    Solicita as credenciais do usuário, com opção de usar credenciais salvas.
    
    Args:
        use_saved (bool): Se True, tenta usar credenciais salvas primeiro.
        
    Returns:
        tuple: (email, password)
    """
    # Verificar se existem credenciais salvas
    saved_emails = cm.list_saved_emails()
    
    if use_saved and saved_emails:
        print("\n=== Credenciais Salvas ===")
        print("Escolha uma conta ou digite 'nova' para adicionar uma nova conta:")
        
        # Mostrar as contas salvas
        for i, email in enumerate(saved_emails, 1):
            print(f"{i}. {email}")
        
        print("n. Nova conta")
        
        # Solicitar escolha do usuário
        while True:
            choice = input("\nSua escolha (número ou 'n'): ").strip().lower()
            
            if choice == 'n' or choice == 'nova':
                # Usuário quer adicionar uma nova conta
                return prompt_new_credentials()
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(saved_emails):
                    # Usuário escolheu uma conta existente
                    email = saved_emails[idx]
                    email, password = cm.get_credentials(email)
                    
                    # Atualizar o timestamp de último uso
                    cm.update_last_used(email)
                    
                    print(f"Usando credenciais salvas para: {email}")
                    return email, password
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Por favor, digite um número ou 'n'.")
    
    # Se não há credenciais salvas ou o usuário não quer usá-las
    return prompt_new_credentials()

def prompt_new_credentials():
    """
    Solicita novas credenciais do usuário.
    
    Returns:
        tuple: (email, password)
    """
    print("\n=== Nova Conta ===")
    email = input("Email do Gmail: ").strip()
    
    # Tentar usar getpass para ocultar a senha durante a digitação
    try:
        password = getpass.getpass("Senha de aplicativo do Gmail: ")
    except Exception:
        # Fallback para input normal se getpass não funcionar
        password = input("Senha de aplicativo do Gmail: ")
    
    # Perguntar se deseja salvar as credenciais
    save = input("Deseja salvar estas credenciais para uso futuro? (s/n): ").strip().lower()
    
    if save.startswith('s'):
        cm.save_credentials(email, password)
        print(f"Credenciais para {email} salvas com sucesso!")
    
    return email, password

def get_credentials():
    """
    Função principal para obter credenciais, com tratamento de erros.
    
    Returns:
        tuple: (email, password)
    """
    try:
        # Verificar se o usuário quer usar credenciais salvas
        saved_emails = cm.list_saved_emails()
        
        if saved_emails:
            use_saved = input("\nDeseja usar uma conta salva? (s/n): ").strip().lower()
            use_saved = use_saved.startswith('s')
        else:
            use_saved = False
        
        return prompt_credentials(use_saved)
    
    except Exception as e:
        print(f"Erro ao obter credenciais: {e}")
        print("Usando método de entrada padrão...")
        
        # Fallback para entrada simples em caso de erro
        email = input("Email do Gmail: ").strip()
        password = input("Senha de aplicativo do Gmail: ")
        
        return email, password

if __name__ == "__main__":
    # Testar a interface
    print("=== Teste da Interface de Credenciais ===")
    email, password = get_credentials()
    print(f"\nCredenciais obtidas: {email}, {'*' * len(password)}")
