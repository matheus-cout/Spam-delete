#!/usr/bin/env python3
"""
Teste simples da interface gráfica para verificar se o botão funciona
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_gui.log'),
        logging.StreamHandler()
    ]
)

class TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teste do Botão Nova Conta")
        self.root.geometry("400x300")
        
        # Criar widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label de status
        self.status_label = ttk.Label(main_frame, text="Clique no botão para testar")
        self.status_label.pack(pady=10)
        
        # Botão de teste
        test_button = ttk.Button(main_frame, text="Nova Conta (Teste)", 
                                command=self.test_new_account)
        test_button.pack(pady=10)
        
        # Área de log
        self.log_text = tk.Text(main_frame, height=10, width=50)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def test_new_account(self):
        """Testa a função de nova conta"""
        try:
            logging.info("Botão 'Nova Conta' clicado")
            self.log_message("Botão clicado - Abrindo diálogo...")
            
            # Simular prompt de credenciais
            email = simpledialog.askstring("Email", "Digite seu email do Gmail:")
            if not email:
                self.log_message("Email cancelado pelo usuário")
                return
                
            password = simpledialog.askstring("Senha", "Digite sua senha:", show='*')
            if not password:
                self.log_message("Senha cancelada pelo usuário")
                return
                
            # Simular salvamento
            save = messagebox.askyesno("Salvar", "Deseja salvar as credenciais?")
            
            if save:
                self.log_message(f"Credenciais salvas para: {email}")
                messagebox.showinfo("Sucesso", f"Conta {email} adicionada!")
            else:
                self.log_message("Credenciais não salvas")
                
            self.status_label.config(text="Teste concluído com sucesso!")
            
        except Exception as e:
            logging.error(f"Erro no teste: {e}")
            self.log_message(f"ERRO: {e}")
            
    def log_message(self, message):
        """Adiciona mensagem ao log visual"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

def main():
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
