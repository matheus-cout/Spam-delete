#!/usr/bin/env python3
"""
Script de inicialização para o Gerenciador de Spam do Gmail.

Este script garante que todos os módulos necessários sejam encontrados corretamente.
"""

import os
import sys
import logging
import traceback
import importlib.util

# Detectar se estamos executando como executável congelado
if getattr(sys, 'frozen', False):
    # Executando como executável
    application_path = os.path.dirname(sys.executable)
    is_frozen = True
else:
    # Executando como script Python
    application_path = os.path.dirname(os.path.abspath(__file__))
    is_frozen = False

# Configurar logging
log_dir = os.path.join(application_path, "logs")
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

logging.info(f"Aplicação congelada: {is_frozen}")
logging.info(f"Caminho da aplicação: {application_path}")

def load_module_from_file(module_name, file_path):
    """Carrega um módulo Python a partir de um arquivo."""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        logging.error(f"Erro ao carregar módulo {module_name} de {file_path}: {e}")
        return None

def main():
    """Função principal do launcher."""
    try:
        logging.info(f"Diretório da aplicação: {application_path}")

        # Adicionar o diretório da aplicação ao PATH do Python
        if application_path not in sys.path:
            sys.path.insert(0, application_path)
            logging.info(f"Adicionado ao sys.path: {application_path}")

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
        loaded_modules = {}

        for module in modules_to_check:
            module_path = os.path.join(application_path, f"{module}.py")
            if not os.path.exists(module_path):
                missing_modules.append(module)
                logging.error(f"Módulo não encontrado: {module_path}")
            else:
                logging.info(f"Módulo encontrado: {module_path}")
                # Tentar carregar o módulo
                loaded_module = load_module_from_file(module, module_path)
                if loaded_module:
                    loaded_modules[module] = loaded_module
                    logging.info(f"Módulo {module} carregado com sucesso")
                else:
                    missing_modules.append(module)

        if missing_modules:
            error_msg = f"Os seguintes módulos não foram encontrados ou não puderam ser carregados: {', '.join(missing_modules)}"
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

        # Executar o módulo principal
        logging.info("Iniciando gui_app")
        if "gui_app" in loaded_modules:
            gui_app = loaded_modules["gui_app"]
            gui_app.main()
        else:
            # Fallback: tentar importar normalmente
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
