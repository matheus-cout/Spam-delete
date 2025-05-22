#!/usr/bin/env python3
"""
Interface Gráfica para o Gerenciador de Spam do Gmail

Este módulo fornece uma interface gráfica para o programa de exclusão de spam do Gmail.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import queue
import time
import os
import sys
import io
import contextlib
import credential_prompt
import credentials_manager as cm

# Importar os módulos de funcionalidade
import delete_spam_emails
import check_spam_count
import verificar_spam

# Classe para redirecionar a saída para a interface gráfica
class TextRedirector:
    def __init__(self, text_widget, queue):
        self.text_widget = text_widget
        self.queue = queue

    def write(self, string):
        self.queue.put(string)

    def flush(self):
        pass

class GmailSpamManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Spam do Gmail")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)

        # Configurar ícone se disponível
        icon_path = os.path.join("icones", "gerenciador_spam.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        # Variáveis
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.remember_credentials = tk.BooleanVar(value=True)
        self.output_queue = queue.Queue()
        self.running_thread = None

        # Criar interface
        self.create_widgets()

        # Iniciar processamento da fila de saída
        self.process_output_queue()

        # Carregar credenciais salvas
        self.load_saved_credentials()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Área de credenciais
        cred_frame = ttk.LabelFrame(main_frame, text="Credenciais do Gmail", padding="10")
        cred_frame.pack(fill=tk.X, padx=5, pady=5)

        # Dropdown de emails salvos
        saved_emails = cm.list_saved_emails()
        email_frame = ttk.Frame(cred_frame)
        email_frame.pack(fill=tk.X, pady=5)

        ttk.Label(email_frame, text="Email:").pack(side=tk.LEFT, padx=(0, 5))

        if saved_emails:
            self.email_combo = ttk.Combobox(email_frame, textvariable=self.email_var, values=saved_emails)
            self.email_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.email_combo.bind("<<ComboboxSelected>>", self.on_email_selected)
        else:
            ttk.Entry(email_frame, textvariable=self.email_var).pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Campo de senha
        pass_frame = ttk.Frame(cred_frame)
        pass_frame.pack(fill=tk.X, pady=5)

        ttk.Label(pass_frame, text="Senha:").pack(side=tk.LEFT, padx=(0, 5))
        self.password_entry = ttk.Entry(pass_frame, textvariable=self.password_var, show="*")
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Checkbox para lembrar credenciais e botão para limpar campos
        cred_options_frame = ttk.Frame(cred_frame)
        cred_options_frame.pack(fill=tk.X, pady=5)

        ttk.Checkbutton(cred_options_frame, text="Lembrar credenciais", variable=self.remember_credentials).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(cred_options_frame, text="Limpar Campos", command=self.clear_credentials).pack(side=tk.LEFT)

        # Área de ações
        action_frame = ttk.LabelFrame(main_frame, text="Ações", padding="10")
        action_frame.pack(fill=tk.X, padx=5, pady=5)

        # Botões de ação
        btn_frame = ttk.Frame(action_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Verificar Spam", command=self.check_spam).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Excluir Spam", command=self.delete_spam).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Parar", command=self.stop_operation).pack(side=tk.LEFT, padx=5)

        # Área de saída
        output_frame = ttk.LabelFrame(main_frame, text="Saída", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Área de texto com rolagem
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=15)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.output_text.config(state=tk.DISABLED)

        # Barra de status
        self.status_var = tk.StringVar(value="Pronto")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_saved_credentials(self):
        """Mostra as credenciais salvas no dropdown, mas não preenche os campos automaticamente."""
        # Apenas atualiza o status para indicar que o programa está pronto
        self.status_var.set("Pronto. Por favor, insira suas credenciais ou selecione uma conta salva.")

    def on_email_selected(self, event):
        """Atualiza o status quando um email é selecionado no dropdown, mas não preenche a senha."""
        email = self.email_var.get()
        if email:
            # Apenas atualiza o status para indicar que o email foi selecionado
            self.status_var.set(f"Email selecionado: {email}. Por favor, digite sua senha.")

    def save_current_credentials(self):
        """Salva as credenciais atuais se a opção estiver marcada."""
        if self.remember_credentials.get():
            email = self.email_var.get()
            password = self.password_var.get()
            if email and password:
                cm.save_credentials(email, password)
                self.status_var.set(f"Credenciais salvas para: {email}")

    def clear_credentials(self):
        """Limpa os campos de credenciais."""
        self.email_var.set("")
        self.password_var.set("")
        self.status_var.set("Campos de credenciais limpos. Por favor, insira suas credenciais.")

    def clear_output(self):
        """Limpa a área de saída."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)

    def append_output(self, text):
        """Adiciona texto à área de saída."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)  # Rola para o final
        self.output_text.config(state=tk.DISABLED)

    def process_output_queue(self):
        """Processa a fila de saída e atualiza a interface."""
        try:
            while not self.output_queue.empty():
                text = self.output_queue.get_nowait()
                self.append_output(text)
        except queue.Empty:
            pass
        finally:
            # Agendar a próxima verificação
            self.root.after(100, self.process_output_queue)

    def check_spam(self):
        """Verifica a quantidade de emails na pasta de spam."""
        if self.running_thread and self.running_thread.is_alive():
            messagebox.showwarning("Operação em andamento", "Aguarde a conclusão da operação atual.")
            return

        email = self.email_var.get()
        password = self.password_var.get()

        if not email or not password:
            messagebox.showerror("Erro", "Por favor, forneça email e senha.")
            return

        # Confirmar as credenciais com o usuário
        if not messagebox.askyesno("Confirmar credenciais",
                                  f"Você está prestes a conectar-se com o email:\n{email}\n\nContinuar?"):
            return

        self.save_current_credentials()
        self.clear_output()
        self.status_var.set("Verificando spam...")

        # Redirecionar saída para a interface
        self.running_thread = threading.Thread(target=self.run_check_spam, args=(email, password))
        self.running_thread.daemon = True
        self.running_thread.start()

    def delete_spam(self):
        """Exclui todos os emails da pasta de spam."""
        if self.running_thread and self.running_thread.is_alive():
            messagebox.showwarning("Operação em andamento", "Aguarde a conclusão da operação atual.")
            return

        email = self.email_var.get()
        password = self.password_var.get()

        if not email or not password:
            messagebox.showerror("Erro", "Por favor, forneça email e senha.")
            return

        # Confirmar as credenciais com o usuário
        if not messagebox.askyesno("Confirmar credenciais",
                                  f"Você está prestes a conectar-se com o email:\n{email}\n\nContinuar?"):
            return

        # Confirmar a exclusão
        if not messagebox.askyesno("Confirmar exclusão",
                                  "Isso excluirá TODOS os emails da pasta de spam. Continuar?"):
            return

        self.save_current_credentials()
        self.clear_output()
        self.status_var.set("Excluindo spam...")

        # Redirecionar saída para a interface
        self.running_thread = threading.Thread(target=self.run_delete_spam, args=(email, password))
        self.running_thread.daemon = True
        self.running_thread.start()

    def run_check_spam(self, email, password):
        """Executa a verificação de spam em uma thread separada."""
        # Redirecionar stdout para a interface
        old_stdout = sys.stdout
        sys.stdout = TextRedirector(self.output_text, self.output_queue)

        try:
            # Configurar o módulo para usar as credenciais fornecidas
            check_spam_count.check_spam_with_credentials(email, password)
            self.root.after(0, lambda: self.status_var.set("Verificação concluída"))
        except Exception as e:
            error_msg = f"Erro: {str(e)}"
            self.output_queue.put(f"\n{error_msg}\n")
            self.root.after(0, lambda: self.status_var.set("Erro na verificação"))
        finally:
            # Restaurar stdout
            sys.stdout = old_stdout

    def run_delete_spam(self, email, password):
        """Executa a exclusão de spam em uma thread separada."""
        # Redirecionar stdout para a interface
        old_stdout = sys.stdout
        sys.stdout = TextRedirector(self.output_text, self.output_queue)

        try:
            # Configurar o módulo para usar as credenciais fornecidas
            delete_spam_emails.delete_spam_with_credentials(email, password)
            self.root.after(0, lambda: self.status_var.set("Exclusão concluída"))
        except Exception as e:
            error_msg = f"Erro: {str(e)}"
            self.output_queue.put(f"\n{error_msg}\n")
            self.root.after(0, lambda: self.status_var.set("Erro na exclusão"))
        finally:
            # Restaurar stdout
            sys.stdout = old_stdout

    def stop_operation(self):
        """Tenta interromper a operação atual."""
        if self.running_thread and self.running_thread.is_alive():
            # Não podemos realmente interromper a thread, mas podemos sinalizar
            self.status_var.set("Tentando interromper a operação...")
            messagebox.showinfo("Interrupção",
                               "Tentando interromper a operação. Aguarde a conclusão do processo atual.")
        else:
            messagebox.showinfo("Nenhuma operação", "Nenhuma operação em andamento.")

def main():
    root = tk.Tk()
    app = GmailSpamManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
