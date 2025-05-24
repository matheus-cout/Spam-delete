#!/usr/bin/env python3
"""
Script para verificar e instalar dependências do Gerenciador de Spam do Gmail.
"""

import subprocess
import sys
import importlib

def check_module(module_name):
    """Verifica se um módulo está instalado."""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    """Instala um pacote usando pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Função principal."""
    print("========================================")
    print(" Verificação de Dependências")
    print("========================================")
    print()
    
    # Lista de dependências necessárias
    dependencies = [
        ("google-auth", "google.auth"),
        ("google-auth-oauthlib", "google_auth_oauthlib"),
        ("google-auth-httplib2", "google.auth.transport.requests"),
        ("google-api-python-client", "googleapiclient"),
        ("requests", "requests"),
        ("cryptography", "cryptography")
    ]
    
    missing_packages = []
    
    # Verificar cada dependência
    for package_name, module_name in dependencies:
        print(f"Verificando {package_name}...", end=" ")
        if check_module(module_name):
            print("✓ OK")
        else:
            print("✗ FALTANDO")
            missing_packages.append(package_name)
    
    print()
    
    if not missing_packages:
        print("✓ Todas as dependências estão instaladas!")
        return 0
    
    print(f"Encontradas {len(missing_packages)} dependências faltando:")
    for package in missing_packages:
        print(f"  - {package}")
    
    print()
    response = input("Deseja instalar as dependências faltando? (s/n): ").lower().strip()
    
    if response in ['s', 'sim', 'y', 'yes']:
        print()
        print("Instalando dependências...")
        
        failed_packages = []
        for package in missing_packages:
            print(f"Instalando {package}...", end=" ")
            if install_package(package):
                print("✓ OK")
            else:
                print("✗ FALHOU")
                failed_packages.append(package)
        
        print()
        
        if not failed_packages:
            print("✓ Todas as dependências foram instaladas com sucesso!")
            return 0
        else:
            print(f"✗ Falha ao instalar {len(failed_packages)} pacotes:")
            for package in failed_packages:
                print(f"  - {package}")
            return 1
    else:
        print("Instalação cancelada pelo usuário.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
