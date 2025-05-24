#!/usr/bin/env python3
"""
Script de Build Final para o Gerenciador de Spam do Gmail
Cria um executável usando a versão integrada que funciona perfeitamente com PyInstaller.
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
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True
    except subprocess.CalledProcessError:
        return False

def clean_build_dirs():
    """Limpa diretórios de build anteriores."""
    dirs_to_clean = ["dist", "build", "__pycache__"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✓ Removido: {dir_name}")
            except PermissionError as e:
                print(f"⚠ Aviso: Não foi possível remover {dir_name}: {e}")
    
    # Remover arquivos .spec
    for file in os.listdir("."):
        if file.endswith(".spec"):
            try:
                os.remove(file)
                print(f"✓ Removido: {file}")
            except:
                pass

def build_executable():
    """Constrói o executável usando PyInstaller."""
    
    # Verificar se o arquivo integrado existe
    if not os.path.exists("gerenciador_spam_integrado.py"):
        print("❌ ERRO: Arquivo gerenciador_spam_integrado.py não encontrado!")
        return False
    
    # Comando do PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Criar um único arquivo executável
        "--windowed",                   # Não mostrar console (Windows)
        "--name=GerenciadorSpamGmail",  # Nome do executável
        "gerenciador_spam_integrado.py"
    ]
    
    # Incluir ícones se existir
    if os.path.exists("icones"):
        icon_file = os.path.join("icones", "gerenciador_spam.ico")
        if os.path.exists(icon_file):
            cmd.extend(["--icon", icon_file])
            print(f"✓ Ícone incluído: {icon_file}")
    
    print("🔨 Executando PyInstaller...")
    print(f"Comando: {' '.join(cmd)}")
    print()
    
    try:
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar PyInstaller: {e}")
        return False

def copy_additional_files():
    """Copia arquivos adicionais para o diretório dist."""
    files_to_copy = [
        "README_SPAM_DELETION.md",
        "configuracao_exclusao_automatica_spam.md"
    ]
    
    if not os.path.exists("dist"):
        return
    
    for file in files_to_copy:
        if os.path.exists(file):
            try:
                shutil.copy2(file, "dist")
                print(f"✓ Copiado: {file}")
            except Exception as e:
                print(f"⚠ Erro ao copiar {file}: {e}")
    
    # Copiar pasta de ícones se existir
    if os.path.exists("icones"):
        try:
            shutil.copytree("icones", os.path.join("dist", "icones"), dirs_exist_ok=True)
            print("✓ Copiado: pasta icones")
        except Exception as e:
            print(f"⚠ Erro ao copiar icones: {e}")

def main():
    """Função principal."""
    print("=" * 50)
    print("🚀 GERENCIADOR DE SPAM DO GMAIL - BUILD FINAL")
    print("=" * 50)
    print()
    
    # Verificar se PyInstaller está instalado
    if not check_pyinstaller():
        print("📦 PyInstaller não encontrado. Instalando...")
        if not install_pyinstaller():
            print("❌ ERRO: Falha ao instalar PyInstaller")
            return 1
        print("✅ PyInstaller instalado com sucesso!")
        print()
    
    # Limpar builds anteriores
    print("🧹 Limpando builds anteriores...")
    clean_build_dirs()
    print()
    
    # Construir o executável
    print("🔨 Construindo executável...")
    if not build_executable():
        print("❌ ERRO: Falha no build!")
        return 1
    
    print()
    print("📁 Copiando arquivos adicionais...")
    copy_additional_files()
    
    print()
    print("=" * 50)
    print("✅ BUILD CONCLUÍDO COM SUCESSO!")
    print("=" * 50)
    print()
    print("📂 O executável foi criado em: dist/")
    print()
    
    # Listar arquivos criados
    if os.path.exists("dist"):
        print("📋 Arquivos criados:")
        for file in os.listdir("dist"):
            file_path = os.path.join("dist", file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                size_mb = size / (1024 * 1024)
                print(f"   📄 {file} ({size_mb:.1f} MB)")
            else:
                print(f"   📁 {file}/")
    
    print()
    print("🎉 Pronto para usar! Execute: dist/GerenciadorSpamGmail.exe")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
