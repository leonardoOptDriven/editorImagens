import os
from PIL import Image

# Substitua 'caminho/da/pasta' pelo caminho da pasta contendo suas imagens
pasta_imagens = 'D:\DOCUMENTOS-D\imagens\GUN_IMAGENS\DATASET_NOVO_VALIDACAO_V3\giro'

# Criar uma pasta para salvar as imagens giradas
pasta_giradas = os.path.join(pasta_imagens, 'giradas')
os.makedirs(pasta_giradas, exist_ok=True)

# Iterar sobre todos os arquivos da pasta
for nome_arquivo in os.listdir(pasta_imagens):
    caminho_arquivo = os.path.join(pasta_imagens, nome_arquivo)
    
    # Verificar se o arquivo é uma imagem
    if caminho_arquivo.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        # Abrir a imagem
        imagem = Image.open(caminho_arquivo)
        
        # Girar a imagem 15 graus para a esquerda
        imagem_girada = imagem.rotate(15, expand=True)
        
        # Salvar a imagem girada
        caminho_girado = os.path.join(pasta_giradas, nome_arquivo)
        imagem_girada.save(caminho_girado)

print('Todas as imagens foram giradas com sucesso!')
