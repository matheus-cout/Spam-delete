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
    
    # Limpar builds anteriores
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
    
    # Comando do PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Criar um único arquivo executável
        "--windowed",                   # Não mostrar console (Windows)
        "--name=GerenciadorSpamGmail",  # Nome do executável
        "--add-data=credentials.json;.", # Incluir credentials.json se existir
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
        "launcher.py"
    ]
    
    # Verificar se credentials.json existe
    if not os.path.exists("credentials.json"):
        # Remover a opção --add-data se o arquivo não existir
        cmd = [arg for arg in cmd if not arg.startswith("--add-data=credentials.json")]
    
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
