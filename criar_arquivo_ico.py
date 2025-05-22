"""
Script para converter os ícones PNG em um único arquivo ICO.
Requer a biblioteca Pillow (PIL).
"""

from PIL import Image
import os

def criar_arquivo_ico():
    # Verificar se o diretório de ícones existe
    if not os.path.exists('icones'):
        print("Erro: A pasta 'icones' não existe.")
        return
    
    # Lista para armazenar as imagens
    imagens = []
    
    # Tamanhos de ícones a serem incluídos
    tamanhos = [16, 32, 48, 64, 128, 256]
    
    # Carregar cada imagem PNG
    for tamanho in tamanhos:
        arquivo_png = f'icones/icone_{tamanho}x{tamanho}.png'
        if os.path.exists(arquivo_png):
            imagem = Image.open(arquivo_png)
            imagens.append(imagem)
        else:
            print(f"Aviso: O arquivo {arquivo_png} não foi encontrado.")
    
    if not imagens:
        print("Erro: Nenhum ícone PNG encontrado.")
        return
    
    # Salvar como arquivo ICO
    arquivo_ico = 'icones/gerenciador_spam.ico'
    imagens[0].save(arquivo_ico, format='ICO', sizes=[(img.width, img.height) for img in imagens], append_images=imagens[1:])
    
    print(f"Arquivo ICO criado: {arquivo_ico}")

if __name__ == "__main__":
    try:
        criar_arquivo_ico()
    except ImportError:
        print("Erro: A biblioteca Pillow (PIL) não está instalada.")
        print("Instale-a usando: pip install pillow")
    except Exception as e:
        print(f"Erro ao criar arquivo ICO: {e}")
