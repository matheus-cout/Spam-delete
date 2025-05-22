"""
Script para criar um executável do programa de exclusão de spam usando cx_Freeze.

Para usar este script:
1. Instale o cx_Freeze: python -m pip install cx_Freeze
2. Execute este script: python setup_exe.py build

O executável será criado na pasta 'build'.
"""

import sys
from cx_Freeze import setup, Executable

# Dependências
build_exe_options = {
    "packages": ["os", "imaplib", "email", "socket", "time", "logging", "datetime"],
    "excludes": ["tkinter", "unittest"],
    "include_files": ["README_SPAM_DELETION.md", "configuracao_exclusao_automatica_spam.md"]
}

# Configurações base para o executável
base = None
if sys.platform == "win32":
    base = "Console"  # Para aplicativos de console

# Escolha qual script você quer converter em executável
# Opções: verificar_spam.py, delete_spam_emails.py, check_spam_count.py
main_script = "verificar_spam.py"  # Altere para o script que você deseja converter

setup(
    name="GerenciadorDeSpam",
    version="1.0",
    description="Ferramenta para gerenciar emails de spam no Gmail",
    options={"build_exe": build_exe_options},
    executables=[Executable(
        main_script,
        base=base,
        target_name="GerenciadorDeSpam.exe",
        icon="icones/gerenciador_spam.ico"
    )]
)

print("\nInstruções para criar o executável:")
print("1. Instale o cx_Freeze: python -m pip install cx_Freeze")
print("2. Execute este script: python setup_exe.py build")
print("3. O executável será criado na pasta 'build'")
