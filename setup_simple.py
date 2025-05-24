#!/usr/bin/env python3
"""
Script de build simplificado para o Gerenciador de Spam do Gmail.

Este script usa cx_Freeze com configurações mais robustas.
"""

import sys
import os
from cx_Freeze import setup, Executable

# Determinar o diretório base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Configurações para Windows
if sys.platform == "win32":
    base = "Win32GUI"  # Remove a janela do console
else:
    base = None

# Lista de módulos a incluir explicitamente
includes = [
    "tkinter",
    "tkinter.ttk",
    "tkinter.messagebox",
    "tkinter.simpledialog",
    "sqlite3",
    "hashlib",
    "base64",
    "os",
    "sys",
    "logging",
    "traceback",
    "importlib.util",
    "threading",
    "time",
    "datetime",
    "json",
    "email",
    "email.mime.text",
    "email.mime.multipart",
    "imaplib",
    "ssl",
    "socket",
    "re",
    "urllib.parse",
    "webbrowser",
    "subprocess",
    "pathlib",
    "configparser"
]

# Lista de pacotes a incluir
packages = [
    "google",
    "google.auth",
    "google.auth.transport",
    "google.auth.transport.requests",
    "google_auth_oauthlib",
    "google_auth_oauthlib.flow",
    "googleapiclient",
    "googleapiclient.discovery",
    "googleapiclient.errors",
    "requests",
    "urllib3",
    "certifi",
    "charset_normalizer",
    "idna",
    "oauthlib",
    "pyasn1",
    "pyasn1_modules",
    "rsa",
    "cachetools",
    "six"
]

# Arquivos a incluir
include_files = [
    ("credentials.json", "credentials.json"),
    ("README.md", "README.md")
]

# Verificar se os arquivos existem antes de incluí-los
filtered_include_files = []
for src, dst in include_files:
    if os.path.exists(src):
        filtered_include_files.append((src, dst))
        print(f"Incluindo arquivo: {src}")
    else:
        print(f"Arquivo não encontrado (ignorando): {src}")

# Opções de build
build_exe_options = {
    "packages": packages,
    "includes": includes,
    "include_files": filtered_include_files,
    "excludes": [
        "test",
        "unittest",
        "pydoc",
        "doctest",
        "argparse",
        "difflib",
        "inspect",
        "calendar",
        "pdb",
        "profile",
        "pstats",
        "timeit"
    ],
    "optimize": 2,
    "build_exe": "build/exe"
}

# Configuração do executável
executables = [
    Executable(
        "launcher.py",
        base=base,
        target_name="GerenciadorSpamGmail.exe",
        icon=None,  # Você pode adicionar um ícone aqui se tiver
        shortcut_name="Gerenciador de Spam do Gmail",
        shortcut_dir="DesktopFolder"
    )
]

# Configuração do setup
setup(
    name="GerenciadorSpamGmail",
    version="1.0.0",
    description="Gerenciador de Spam do Gmail - Remove emails de spam automaticamente",
    author="Seu Nome",
    options={"build_exe": build_exe_options},
    executables=executables
)
