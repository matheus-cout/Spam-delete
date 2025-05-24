#!/usr/bin/env python3
"""
Script de build alternativo usando PyInstaller.

Este script pode ser usado como alternativa ao cx_Freeze.
"""

import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """Verifica se o PyInstaller está instalado."""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Instala o PyInstaller."""
    print("Instalando PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True
    except subprocess.CalledProcessError:
        return False

def build_with_pyinstaller():
    """Constrói o executável usando PyInstaller."""

    # Limpar builds anteriores com tratamento de erro
    def safe_rmtree(path):
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                print(f"Removido: {path}")
            except PermissionError as e:
                print(f"Aviso: Não foi possível remover {path}: {e}")
                print("Continuando mesmo assim...")

    safe_rmtree("dist")
    safe_rmtree("build")
    safe_rmtree("__pycache__")

    # Verificar se todos os módulos Python existem
    required_modules = [
        "credential_prompt.py",
        "credentials_manager.py",
        "delete_spam_emails.py",
        "check_spam_count.py",
        "verificar_spam.py",
        "gui_app.py",
        "launcher_simple.py"
    ]

    missing_modules = []
    for module in required_modules:
        if not os.path.exists(module):
            missing_modules.append(module)

    if missing_modules:
        print(f"ERRO: Módulos não encontrados: {missing_modules}")
        return False

    # Comando do PyInstaller com todos os módulos explicitamente incluídos
    cmd = [
        "pyinstaller",
        "--onefile",                    # Criar um único arquivo executável
        "--windowed",                   # Não mostrar console (Windows)
        "--name=GerenciadorSpamGmail",  # Nome do executável
        "--add-data=credential_prompt.py;.",
        "--add-data=credentials_manager.py;.",
        "--add-data=delete_spam_emails.py;.",
        "--add-data=check_spam_count.py;.",
        "--add-data=verificar_spam.py;.",
        "--add-data=gui_app.py;.",
        "--hidden-import=credential_prompt",
        "--hidden-import=credentials_manager",
        "--hidden-import=delete_spam_emails",
        "--hidden-import=check_spam_count",
        "--hidden-import=verificar_spam",
        "--hidden-import=gui_app",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.simpledialog",
        "--hidden-import=google.auth",
        "--hidden-import=google.auth.transport.requests",
        "--hidden-import=google_auth_oauthlib.flow",
        "--hidden-import=googleapiclient.discovery",
        "--hidden-import=googleapiclient.errors",
        "--hidden-import=sqlite3",
        "--hidden-import=hashlib",
        "--hidden-import=base64",
        "--hidden-import=imaplib",
        "--hidden-import=email.mime.text",
        "--hidden-import=email.mime.multipart",
        "--hidden-import=threading",
        "--hidden-import=queue",
        "--hidden-import=datetime",
        "--hidden-import=time",
        "--hidden-import=json",
        "--hidden-import=logging",
        "--hidden-import=traceback",
        "--hidden-import=importlib.util",
        "launcher_simple.py"
    ]

    # Incluir credentials.json se existir
    if os.path.exists("credentials.json"):
        cmd.insert(-1, "--add-data=credentials.json;.")

    # Incluir pasta de ícones se existir
    if os.path.exists("icones"):
        cmd.insert(-1, "--add-data=icones;icones")

    print("Executando PyInstaller...")
    print(f"Comando: {' '.join(cmd)}")

    try:
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar PyInstaller: {e}")
        return False

def main():
    """Função principal."""
    print("========================================")
    print(" Gerenciador de Spam do Gmail - Build")
    print(" (usando PyInstaller)")
    print("========================================")
    print()

    # Verificar se PyInstaller está instalado
    if not check_pyinstaller():
        print("PyInstaller não encontrado.")
        if not install_pyinstaller():
            print("ERRO: Falha ao instalar PyInstaller")
            return 1
        print("PyInstaller instalado com sucesso!")
        print()

    # Construir o executável
    if build_with_pyinstaller():
        print()
        print("========================================")
        print(" Build concluído com sucesso!")
        print("========================================")
        print()
        print("O executável foi criado em: dist/")
        print()

        # Listar arquivos criados
        if os.path.exists("dist"):
            print("Arquivos criados:")
            for file in os.listdir("dist"):
                print(f"  - {file}")

        return 0
    else:
        print()
        print("ERRO: Falha no build!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
