#!/usr/bin/env python3
"""
Script de inicialização para o Gerenciador de Spam do Gmail.

Este script garante que todos os módulos necessários sejam encontrados corretamente.
"""

import os
import sys
import logging
import traceback

# Configurar logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "launcher.log")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    """Função principal do launcher."""
    try:
        # Obter o diretório do script atual
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logging.info(f"Diretório atual: {current_dir}")
        
        # Adicionar o diretório atual ao PATH do Python
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
            logging.info(f"Adicionado ao sys.path: {current_dir}")
        
        # Verificar se os módulos necessários estão disponíveis
        modules_to_check = [
            "credential_prompt",
            "credentials_manager",
            "delete_spam_emails",
            "check_spam_count",
            "verificar_spam",
            "gui_app"
        ]
        
        missing_modules = []
        for module in modules_to_check:
            module_path = os.path.join(current_dir, f"{module}.py")
            if not os.path.exists(module_path):
                missing_modules.append(module)
                logging.error(f"Módulo não encontrado: {module_path}")
            else:
                logging.info(f"Módulo encontrado: {module_path}")
        
        if missing_modules:
            error_msg = f"Os seguintes módulos não foram encontrados: {', '.join(missing_modules)}"
            logging.error(error_msg)
            
            # Mostrar mensagem de erro
            try:
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Erro", f"Não foi possível iniciar o programa.\n\n{error_msg}\n\nConsulte o arquivo de log para mais detalhes:\n{log_file}")
            except:
                print(f"ERRO: {error_msg}")
                print(f"Consulte o arquivo de log para mais detalhes: {log_file}")
            
            return 1
        
        # Importar e executar o módulo principal
        logging.info("Iniciando gui_app.py")
        import gui_app
        gui_app.main()
        
        return 0
    
    except Exception as e:
        logging.error(f"Erro ao iniciar o programa: {e}")
        traceback.print_exc(file=open(log_file, "a"))
        
        # Mostrar mensagem de erro
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Erro", f"Ocorreu um erro ao iniciar o programa:\n\n{e}\n\nConsulte o arquivo de log para mais detalhes:\n{log_file}")
        except:
            print(f"ERRO: {e}")
            print(f"Consulte o arquivo de log para mais detalhes: {log_file}")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
