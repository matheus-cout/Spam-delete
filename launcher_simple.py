#!/usr/bin/env python3
"""
Launcher simples para o Gerenciador de Spam do Gmail.
Otimizado para funcionar com PyInstaller.
"""

import os
import sys
import logging

# Configurar logging
def setup_logging():
    """Configura o sistema de logging."""
    # Detectar se estamos executando como executável congelado
    if getattr(sys, 'frozen', False):
        # Executando como executável
        application_path = os.path.dirname(sys.executable)
    else:
        # Executando como script Python
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    log_dir = os.path.join(application_path, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "launcher.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return application_path

def main():
    """Função principal do launcher."""
    try:
        application_path = setup_logging()
        logging.info(f"Iniciando Gerenciador de Spam do Gmail")
        logging.info(f"Aplicação congelada: {getattr(sys, 'frozen', False)}")
        logging.info(f"Caminho da aplicação: {application_path}")
        
        # Adicionar o diretório da aplicação ao PATH do Python
        if application_path not in sys.path:
            sys.path.insert(0, application_path)
        
        # Tentar importar e executar o módulo principal
        logging.info("Importando gui_app...")
        
        try:
            import gui_app
            logging.info("gui_app importado com sucesso")
            gui_app.main()
        except ImportError as e:
            logging.error(f"Erro ao importar gui_app: {e}")
            
            # Mostrar mensagem de erro
            try:
                import tkinter as tk
                from tkinter import messagebox
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror(
                    "Erro", 
                    f"Não foi possível iniciar o programa.\n\n"
                    f"Erro: {e}\n\n"
                    f"Verifique se todos os arquivos estão presentes."
                )
            except:
                print(f"ERRO: Não foi possível iniciar o programa: {e}")
            
            return 1
        
        return 0
        
    except Exception as e:
        logging.error(f"Erro crítico: {e}")
        import traceback
        logging.error(traceback.format_exc())
        
        # Mostrar mensagem de erro
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Erro Crítico", 
                f"Erro crítico no programa:\n\n{e}\n\n"
                f"Consulte os logs para mais detalhes."
            )
        except:
            print(f"ERRO CRÍTICO: {e}")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
