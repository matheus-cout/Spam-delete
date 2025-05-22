"""
Script para criar um ícone simples para o Gerenciador de Spam.
Requer a biblioteca Pillow (PIL).
"""

from PIL import Image, ImageDraw, ImageFont
import os

def criar_icone():
    # Verificar se o diretório existe
    if not os.path.exists('icones'):
        os.makedirs('icones')
    
    # Tamanhos de ícones a serem criados
    tamanhos = [16, 32, 48, 64, 128, 256]
    
    # Cores
    cor_fundo = (65, 105, 225)  # Azul real
    cor_texto = (255, 255, 255)  # Branco
    
    # Criar ícones em vários tamanhos
    for tamanho in tamanhos:
        # Criar uma nova imagem com fundo azul
        imagem = Image.new('RGB', (tamanho, tamanho), cor_fundo)
        desenho = ImageDraw.Draw(imagem)
        
        # Adicionar um círculo branco no centro
        raio = tamanho // 3
        centro = tamanho // 2
        desenho.ellipse((centro - raio, centro - raio, centro + raio, centro + raio), fill=cor_texto)
        
        # Adicionar a letra "S" no centro
        try:
            # Tentar usar uma fonte do sistema
            fonte = ImageFont.truetype("arial.ttf", tamanho // 2)
            # Calcular a posição do texto para centralizá-lo
            texto = "S"
            largura_texto, altura_texto = desenho.textsize(texto, font=fonte)
            posicao_texto = ((tamanho - largura_texto) // 2, (tamanho - altura_texto) // 2 - tamanho // 10)
            desenho.text(posicao_texto, texto, font=fonte, fill=cor_fundo)
        except:
            # Se não conseguir usar a fonte, apenas desenhar um retângulo
            desenho.rectangle((centro - raio//2, centro - raio//2, centro + raio//2, centro + raio//2), fill=cor_fundo)
        
        # Salvar a imagem como PNG
        imagem.save(f'icones/icone_{tamanho}x{tamanho}.png')
    
    print(f"Ícones criados na pasta 'icones'")

if __name__ == "__main__":
    try:
        criar_icone()
    except ImportError:
        print("Erro: A biblioteca Pillow (PIL) não está instalada.")
        print("Instale-a usando: pip install pillow")
    except Exception as e:
        print(f"Erro ao criar ícones: {e}")
