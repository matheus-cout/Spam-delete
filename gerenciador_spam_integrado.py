#!/usr/bin/env python3
"""
Gerenciador de Spam do Gmail - Versão Integrada
Todos os módulos em um único arquivo para compatibilidade com PyInstaller.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import threading
import queue
import time
import os
import sys
import io
import contextlib
import logging
import traceback
import sqlite3
import base64
import hashlib
import imaplib
import email
from datetime import datetime
import getpass

# Configurar logging
def setup_logging():
    """Configura o sistema de logging."""
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    log_dir = os.path.join(application_path, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "gerenciador_spam.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

# Configurar logging
setup_logging()

# ===== MÓDULO CREDENTIALS_MANAGER =====
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    logging.warning("Cryptography não disponível. Senhas serão armazenadas sem criptografia.")

# Diretório para armazenar o banco de dados
if getattr(sys, 'frozen', False):
    DATA_DIR = os.path.join(os.path.dirname(sys.executable), "data")
else:
    DATA_DIR = "data"

DB_FILE = os.path.join(DATA_DIR, "credentials.db")
KEY_FILE = os.path.join(DATA_DIR, "key.bin")

os.makedirs(DATA_DIR, exist_ok=True)

def generate_key():
    """Gera uma nova chave de criptografia e a salva no arquivo."""
    if not CRYPTO_AVAILABLE:
        return b"dummy_key"

    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key

def get_encryption_key():
    """Obtém a chave de criptografia do arquivo ou gera uma nova se não existir."""
    if not CRYPTO_AVAILABLE:
        return b"dummy_key"

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            key = key_file.read()
    else:
        key = generate_key()

    return key

def encrypt_password(password):
    """Criptografa uma senha usando Fernet (criptografia simétrica)."""
    if not CRYPTO_AVAILABLE:
        return password.encode()

    key = get_encryption_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password):
    """Descriptografa uma senha criptografada."""
    if not CRYPTO_AVAILABLE:
        return encrypted_password.decode() if isinstance(encrypted_password, bytes) else encrypted_password

    key = get_encryption_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password)
    return decrypted_password.decode()

def initialize_database():
    """Inicializa o banco de dados SQLite3 com a tabela de credenciais."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                encrypted_password BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
        logging.info("Banco de dados inicializado com sucesso")

    except Exception as e:
        logging.error(f"Erro ao inicializar banco de dados: {e}")
        raise

def save_credentials(email, password):
    """Salva as credenciais no banco de dados."""
    try:
        encrypted_password = encrypt_password(password)

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO credentials (email, encrypted_password, last_used)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (email, encrypted_password))

        conn.commit()
        conn.close()
        logging.info(f"Credenciais salvas para {email}")

    except Exception as e:
        logging.error(f"Erro ao salvar credenciais: {e}")
        raise

def get_credentials(email):
    """Recupera as credenciais do banco de dados."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT email, encrypted_password FROM credentials
            WHERE email = ?
        ''', (email,))

        result = cursor.fetchone()
        conn.close()

        if result:
            email, encrypted_password = result
            password = decrypt_password(encrypted_password)
            return email, password
        else:
            return None, None

    except Exception as e:
        logging.error(f"Erro ao recuperar credenciais: {e}")
        return None, None

def list_saved_emails():
    """Lista todos os emails salvos no banco de dados."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('SELECT email FROM credentials ORDER BY last_used DESC')
        emails = [row[0] for row in cursor.fetchall()]

        conn.close()
        return emails

    except Exception as e:
        logging.error(f"Erro ao listar emails: {e}")
        return []

def delete_credentials(email):
    """Remove as credenciais do banco de dados."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM credentials WHERE email = ?', (email,))

        conn.commit()
        conn.close()
        logging.info(f"Credenciais removidas para {email}")

    except Exception as e:
        logging.error(f"Erro ao remover credenciais: {e}")
        raise

# Inicializar o banco de dados
initialize_database()

# ===== MÓDULO CHECK_SPAM_COUNT =====
def check_spam_count(email, password):
    """Verifica a quantidade de emails na pasta de spam."""
    try:
        logging.info("Connecting to imap.gmail.com...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")

        logging.info(f"Logging in as {email}...")
        mail.login(email, password)
        logging.info("Login successful")

        logging.info("Selecting folder: [Gmail]/Spam")
        mail.select("[Gmail]/Spam")

        status, messages = mail.search(None, "ALL")
        if status == "OK":
            message_ids = messages[0].split()
            spam_count = len(message_ids)
            logging.info(f"Number of emails in [Gmail]/Spam: {spam_count}")
        else:
            spam_count = 0
            logging.warning("Failed to search emails in spam folder")

        mail.logout()
        logging.info("Logged out successfully")

        return spam_count

    except Exception as e:
        logging.error(f"Error checking spam count: {e}")
        raise

# ===== MÓDULO DELETE_SPAM_EMAILS =====
def delete_spam_emails(email, password):
    """Deleta todos os emails da pasta de spam."""
    try:
        start_time = time.time()

        logging.info("Connecting to imap.gmail.com...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")

        logging.info(f"Logging in as {email}...")
        mail.login(email, password)
        logging.info("Login successful")

        logging.info("Selecting folder: [Gmail]/Spam")
        mail.select("[Gmail]/Spam")

        status, messages = mail.search(None, "ALL")
        if status == "OK":
            message_ids = messages[0].split()
            total_emails = len(message_ids)

            if total_emails == 0:
                logging.info("No emails found in spam folder")
                mail.logout()
                return 0

            logging.info(f"Found {total_emails} emails in spam folder")
            logging.info("Marking all emails for deletion...")

            for msg_id in message_ids:
                mail.store(msg_id, '+FLAGS', '\\Deleted')

            logging.info("Expunging deleted emails...")
            mail.expunge()

            logging.info(f"Successfully deleted {total_emails} emails from spam folder")
        else:
            total_emails = 0
            logging.warning("Failed to search emails in spam folder")

        mail.logout()
        logging.info("Logged out successfully")

        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Script execution time: {execution_time:.2f} seconds")

        return total_emails

    except Exception as e:
        logging.error(f"Error deleting spam emails: {e}")
        raise

# ===== MÓDULO VERIFICAR_SPAM =====
def verificar_spam(email, password):
    """Verifica emails de spam sem deletar."""
    try:
        start_time = time.time()

        logging.info("Connecting to imap.gmail.com...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")

        logging.info(f"Logging in as {email}...")
        mail.login(email, password)
        logging.info("Login successful")

        logging.info("Selecting folder: [Gmail]/Spam")
        mail.select("[Gmail]/Spam")

        status, messages = mail.search(None, "ALL")
        if status == "OK":
            message_ids = messages[0].split()
            total_emails = len(message_ids)
            logging.info(f"Found {total_emails} emails in spam folder")
        else:
            total_emails = 0
            logging.warning("Failed to search emails in spam folder")

        mail.logout()
        logging.info("Logged out successfully")

        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Script execution time: {execution_time:.2f} seconds")

        return total_emails

    except Exception as e:
        logging.error(f"Error checking spam: {e}")
        raise

# ===== MÓDULO CREDENTIAL_PROMPT =====
def prompt_credentials_gui(parent=None):
    """Solicita credenciais através de uma interface gráfica."""
    try:
        logging.info("Iniciando prompt_credentials_gui")
        saved_emails = list_saved_emails()
        logging.info(f"Emails salvos encontrados: {len(saved_emails)}")
        choice = False  # Inicializar choice

        if saved_emails:
            logging.info("Mostrando diálogo para escolher conta existente")
            # Mostrar diálogo para escolher email salvo ou novo
            choice = messagebox.askyesno(
                "Credenciais Salvas",
                "Foram encontradas credenciais salvas. Deseja usar uma conta existente?",
                parent=parent
            )
            logging.info(f"Usuário escolheu usar conta existente: {choice}")
        else:
            choice = False

        if choice and saved_emails:
            # Mostrar lista de emails salvos
            email = simpledialog.askstring(
                "Selecionar Email",
                f"Emails salvos:\n" + "\n".join(f"{i+1}. {email}" for i, email in enumerate(saved_emails)) +
                f"\n\nDigite o número (1-{len(saved_emails)}) ou o email completo:",
                parent=parent
            )

            if email:
                try:
                    # Tentar interpretar como número
                    index = int(email) - 1
                    if 0 <= index < len(saved_emails):
                        selected_email = saved_emails[index]
                    else:
                        selected_email = email
                except ValueError:
                    selected_email = email

                # Recuperar senha salva
                stored_email, password = get_credentials(selected_email)
                if stored_email and password:
                    logging.info("Credenciais recuperadas com sucesso")
                    return stored_email, password
                else:
                    logging.warning(f"Credenciais não encontradas para {selected_email}")
                    messagebox.showerror("Erro", f"Credenciais não encontradas para {selected_email}", parent=parent)
            else:
                logging.info("Usuário cancelou seleção de email")

        # Solicitar novas credenciais
        logging.info("Solicitando novas credenciais")
        email = simpledialog.askstring("Email", "Digite seu email do Gmail:", parent=parent)
        logging.info(f"Email inserido: {email is not None}")
        if not email:
            logging.info("Email cancelado pelo usuário")
            return None, None

        password = simpledialog.askstring("Senha", "Digite sua senha de aplicativo:", show='*', parent=parent)
        logging.info(f"Senha inserida: {password is not None}")
        if not password:
            logging.info("Senha cancelada pelo usuário")
            return None, None

        # Perguntar se deseja salvar
        save = messagebox.askyesno(
            "Salvar Credenciais",
            "Deseja salvar estas credenciais para uso futuro?",
            parent=parent
        )

        if save:
            try:
                save_credentials(email, password)
                messagebox.showinfo("Sucesso", f"Credenciais salvas para {email}!", parent=parent)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar credenciais: {e}", parent=parent)

        return email, password

    except Exception as e:
        logging.error(f"Erro ao solicitar credenciais: {e}")
        return None, None

# ===== CLASSE TEXTREDIRECTOR =====
class TextRedirector:
    def __init__(self, text_widget, queue):
        self.text_widget = text_widget
        self.queue = queue

    def write(self, string):
        self.queue.put(string)

    def flush(self):
        pass

# ===== CLASSE PRINCIPAL DA GUI =====
class GmailSpamManagerApp:
    def __init__(self, root):
        try:
            logging.info("Inicializando GmailSpamManagerApp")
            self.root = root
            self.root.title("Gerenciador de Spam do Gmail")
            self.root.geometry("800x600")
            self.root.minsize(700, 500)

            # Configurar ícone se disponível
            icon_path = os.path.join("icones", "gerenciador_spam.ico")
            if os.path.exists(icon_path):
                logging.info(f"Ícone encontrado: {icon_path}")
                self.root.iconbitmap(icon_path)
            else:
                logging.warning(f"Ícone não encontrado: {icon_path}")

            # Variáveis
            self.email_var = tk.StringVar()
            self.status_var = tk.StringVar(value="Pronto")
            self.output_queue = queue.Queue()
            self.running_thread = None

            # Criar widgets
            self.create_widgets()

            # Iniciar processamento da fila de saída
            self.process_output_queue()

            # Carregar credenciais salvas
            self.load_saved_credentials()

            logging.info("Inicialização concluída com sucesso")

        except Exception as e:
            logging.error(f"Erro na inicialização: {e}")
            logging.error(traceback.format_exc())
            messagebox.showerror("Erro de Inicialização", f"Erro ao inicializar a aplicação: {e}")

    def create_widgets(self):
        try:
            logging.info("Criando widgets da interface")

            # Frame principal
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.pack(fill=tk.BOTH, expand=True)

            # Área de credenciais
            cred_frame = ttk.LabelFrame(main_frame, text="Credenciais do Gmail", padding="10")
            cred_frame.pack(fill=tk.X, padx=5, pady=5)

            # Dropdown de emails salvos
            try:
                logging.info("Obtendo lista de emails salvos")
                saved_emails = list_saved_emails()
                logging.info(f"Emails salvos encontrados: {len(saved_emails)}")
            except Exception as e:
                logging.error(f"Erro ao obter emails salvos: {e}")
                saved_emails = []

            if saved_emails:
                logging.info("Criando combobox para emails salvos")
                ttk.Label(cred_frame, text="Email salvo:").pack(anchor=tk.W)
                self.email_combo = ttk.Combobox(cred_frame, textvariable=self.email_var,
                                              values=saved_emails, state="readonly", width=50)
                self.email_combo.pack(fill=tk.X, pady=(0, 10))

                if saved_emails:
                    self.email_combo.set(saved_emails[0])
            else:
                ttk.Label(cred_frame, text="Nenhuma credencial salva encontrada.").pack(anchor=tk.W)
                self.email_combo = None

            # Botões de credenciais
            cred_buttons_frame = ttk.Frame(cred_frame)
            cred_buttons_frame.pack(fill=tk.X, pady=5)

            ttk.Button(cred_buttons_frame, text="Nova Conta",
                      command=self.add_new_account).pack(side=tk.LEFT, padx=(0, 5))

            if saved_emails:
                ttk.Button(cred_buttons_frame, text="Remover Conta",
                          command=self.remove_account).pack(side=tk.LEFT, padx=5)

            # Área de operações
            ops_frame = ttk.LabelFrame(main_frame, text="Operações", padding="10")
            ops_frame.pack(fill=tk.X, padx=5, pady=5)

            # Botões de operação
            buttons_frame = ttk.Frame(ops_frame)
            buttons_frame.pack(fill=tk.X, pady=5)

            ttk.Button(buttons_frame, text="Verificar Spam",
                      command=self.check_spam).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(buttons_frame, text="Deletar Spam",
                      command=self.delete_spam).pack(side=tk.LEFT, padx=5)
            ttk.Button(buttons_frame, text="Parar",
                      command=self.stop_operation).pack(side=tk.LEFT, padx=5)

            # Área de status
            status_frame = ttk.Frame(main_frame)
            status_frame.pack(fill=tk.X, padx=5, pady=5)

            ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
            ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=(5, 0))

            # Área de saída
            output_frame = ttk.LabelFrame(main_frame, text="Saída do Programa", padding="10")
            output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            self.output_text = scrolledtext.ScrolledText(output_frame, height=15, state=tk.DISABLED)
            self.output_text.pack(fill=tk.BOTH, expand=True)

            logging.info("Widgets criados com sucesso")

        except Exception as e:
            logging.error(f"Erro ao criar widgets: {e}")
            logging.error(traceback.format_exc())
            raise

    def process_output_queue(self):
        """Processa a fila de saída para atualizar a interface."""
        try:
            while True:
                message = self.output_queue.get_nowait()
                self.output_text.config(state=tk.NORMAL)
                self.output_text.insert(tk.END, message)
                self.output_text.see(tk.END)
                self.output_text.config(state=tk.DISABLED)
        except queue.Empty:
            pass

        # Agendar próxima verificação
        self.root.after(100, self.process_output_queue)

    def load_saved_credentials(self):
        """Carrega credenciais salvas na inicialização."""
        try:
            logging.info("Carregando credenciais salvas")
            saved_emails = list_saved_emails()
            if saved_emails and hasattr(self, 'email_combo') and self.email_combo:
                self.email_combo['values'] = saved_emails
                if not self.email_var.get():
                    self.email_combo.set(saved_emails[0])
        except Exception as e:
            logging.error(f"Erro ao carregar credenciais: {e}")

    def get_current_credentials(self):
        """Obtém as credenciais atuais selecionadas."""
        logging.info("Iniciando get_current_credentials")

        # Verificar se há combo box e email selecionado
        has_combo = hasattr(self, 'email_combo') and self.email_combo
        has_email = self.email_var.get() if has_combo else None

        logging.info(f"Has combo: {has_combo}, Email selecionado: '{has_email}'")

        if has_combo and has_email:
            email = self.email_var.get().strip()
            logging.info(f"Tentando obter credenciais para: '{email}'")

            try:
                stored_email, password = get_credentials(email)
                logging.info(f"Credenciais obtidas: email={stored_email is not None}, password={password is not None}")

                if stored_email and password:
                    logging.info("Credenciais válidas encontradas - usando credenciais salvas")
                    return stored_email, password
                else:
                    logging.warning(f"Credenciais não encontradas para '{email}'")
            except Exception as e:
                logging.error(f"Erro ao obter credenciais para '{email}': {e}")

        # Se não há credenciais salvas ou houve erro, solicitar novas
        logging.info("Solicitando novas credenciais via prompt")
        result = prompt_credentials_gui(self.root)
        logging.info(f"Resultado do prompt: {result[0] is not None if result else False}, {result[1] is not None if result else False}")
        return result

    def add_new_account(self):
        """Adiciona uma nova conta."""
        try:
            logging.info("Botão 'Nova Conta' clicado")
            self.output_queue.put("Abrindo diálogo para nova conta...\n")

            email, password = prompt_credentials_gui(self.root)
            logging.info(f"Resultado do prompt: email={email is not None}, password={password is not None}")

            if email and password:
                # Atualizar a interface
                self.refresh_credentials_list()
                messagebox.showinfo("Sucesso", f"Conta {email} adicionada com sucesso!")
                self.output_queue.put(f"Nova conta adicionada: {email}\n")
            else:
                self.output_queue.put("Operação cancelada pelo usuário.\n")

        except Exception as e:
            logging.error(f"Erro ao adicionar conta: {e}")
            logging.error(traceback.format_exc())
            messagebox.showerror("Erro", f"Erro ao adicionar conta: {e}")
            self.output_queue.put(f"ERRO ao adicionar conta: {e}\n")

    def remove_account(self):
        """Remove a conta selecionada."""
        try:
            if not hasattr(self, 'email_combo') or not self.email_combo or not self.email_var.get():
                messagebox.showwarning("Aviso", "Nenhuma conta selecionada.")
                return

            email = self.email_var.get()
            confirm = messagebox.askyesno(
                "Confirmar Remoção",
                f"Tem certeza que deseja remover a conta {email}?"
            )

            if confirm:
                delete_credentials(email)
                self.refresh_credentials_list()
                messagebox.showinfo("Sucesso", f"Conta {email} removida com sucesso!")

        except Exception as e:
            logging.error(f"Erro ao remover conta: {e}")
            messagebox.showerror("Erro", f"Erro ao remover conta: {e}")

    def refresh_credentials_list(self):
        """Atualiza a lista de credenciais na interface."""
        try:
            saved_emails = list_saved_emails()
            if hasattr(self, 'email_combo') and self.email_combo:
                self.email_combo['values'] = saved_emails
                if saved_emails:
                    self.email_combo.set(saved_emails[0])
                else:
                    self.email_var.set("")
        except Exception as e:
            logging.error(f"Erro ao atualizar lista de credenciais: {e}")

    def check_spam(self):
        """Verifica a quantidade de spam."""
        if self.running_thread and self.running_thread.is_alive():
            messagebox.showwarning("Operação em Andamento", "Aguarde a operação atual terminar.")
            return

        # Adicionar debug para verificar se o botão está sendo clicado
        logging.info("Botão 'Verificar Spam' clicado")
        self.output_queue.put("Iniciando verificação de spam...\n")

        self.running_thread = threading.Thread(target=self._check_spam_thread)
        self.running_thread.daemon = True
        self.running_thread.start()

    def _check_spam_thread(self):
        """Thread para verificar spam."""
        try:
            self.status_var.set("Verificando spam...")

            # Redirecionar saída para a interface
            old_stdout = sys.stdout
            sys.stdout = TextRedirector(self.output_text, self.output_queue)

            email, password = self.get_current_credentials()
            if not email or not password:
                self.output_queue.put("Operação cancelada pelo usuário.\n")
                return

            spam_count = verificar_spam(email, password)
            self.output_queue.put(f"\n=== RESULTADO ===\n")
            self.output_queue.put(f"Emails de spam encontrados: {spam_count}\n")
            self.output_queue.put("=================\n\n")

            self.status_var.set("Verificação concluída")

        except Exception as e:
            self.output_queue.put(f"ERRO: {e}\n")
            self.status_var.set("Erro na verificação")
            logging.error(f"Erro na verificação de spam: {e}")
        finally:
            sys.stdout = old_stdout

    def delete_spam(self):
        """Deleta emails de spam."""
        if self.running_thread and self.running_thread.is_alive():
            messagebox.showwarning("Operação em Andamento", "Aguarde a operação atual terminar.")
            return

        # Confirmar operação
        confirm = messagebox.askyesno(
            "Confirmar Exclusão",
            "Tem certeza que deseja deletar TODOS os emails de spam?\n\nEsta operação não pode ser desfeita!"
        )

        if not confirm:
            return

        self.running_thread = threading.Thread(target=self._delete_spam_thread)
        self.running_thread.daemon = True
        self.running_thread.start()

    def _delete_spam_thread(self):
        """Thread para deletar spam."""
        try:
            self.status_var.set("Deletando spam...")

            # Redirecionar saída para a interface
            old_stdout = sys.stdout
            sys.stdout = TextRedirector(self.output_text, self.output_queue)

            email, password = self.get_current_credentials()
            if not email or not password:
                self.output_queue.put("Operação cancelada pelo usuário.\n")
                return

            deleted_count = delete_spam_emails(email, password)
            self.output_queue.put(f"\n=== RESULTADO ===\n")
            self.output_queue.put(f"Emails deletados: {deleted_count}\n")
            self.output_queue.put("=================\n\n")

            self.status_var.set("Exclusão concluída")

        except Exception as e:
            self.output_queue.put(f"ERRO: {e}\n")
            self.status_var.set("Erro na exclusão")
            logging.error(f"Erro na exclusão de spam: {e}")
        finally:
            sys.stdout = old_stdout

    def stop_operation(self):
        """Tenta interromper a operação atual."""
        if self.running_thread and self.running_thread.is_alive():
            self.status_var.set("Tentando interromper a operação...")
            messagebox.showinfo("Interrupção",
                               "Tentando interromper a operação. Aguarde a conclusão do processo atual.")
        else:
            messagebox.showinfo("Nenhuma operação", "Nenhuma operação em andamento.")

# ===== FUNÇÃO PRINCIPAL =====
def main():
    """Função principal da aplicação."""
    try:
        logging.info("Iniciando Gerenciador de Spam do Gmail")
        root = tk.Tk()

        # Suprimir erros específicos do Tkinter relacionados a janelas sendo fechadas
        def tk_error_handler(exc, val, tb):
            error_msg = str(val)
            if "querystring" in error_msg and "was deleted before its visibility changed" in error_msg:
                # Ignorar este erro específico do Tkinter
                return
            # Para outros erros, usar o handler padrão
            sys.__excepthook__(exc, val, tb)

        sys.excepthook = tk_error_handler

        app = GmailSpamManagerApp(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Erro crítico: {e}")
        logging.error(traceback.format_exc())
        try:
            messagebox.showerror("Erro Crítico", f"Erro crítico na aplicação: {e}")
        except:
            print(f"ERRO CRÍTICO: {e}")

if __name__ == "__main__":
    main()
