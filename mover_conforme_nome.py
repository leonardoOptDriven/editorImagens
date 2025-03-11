import os
import shutil

# Caminhos das pastas
pasta_imagens = 'D:/DOCUMENTOS-D/imagens/GUN_IMAGENS/DATASET_NOVO_TREINAMENTO/oitavo_dataset/images/train'
pasta_textos =  'D:/DOCUMENTOS-D/imagens/GUN_IMAGENS/DATASET_NOVO_TREINAMENTO/oitavo_dataset/labels/train'
pasta_destino = 'D:/DOCUMENTOS-D/imagens/GUN_IMAGENS/DATASET_NOVO_TREINAMENTO/oitavo_dataset/labels/train_ok'

# Cria a pasta de destino se não existir
os.makedirs(pasta_destino, exist_ok=True)

# Lista todos os arquivos na pasta de imagens
for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        nome_base = os.path.splitext(nome_arquivo)[0]
        arquivo_texto = f"{nome_base}.txt"
        
        caminho_imagem = os.path.join(pasta_imagens, nome_arquivo)
        caminho_texto = os.path.join(pasta_textos, arquivo_texto)
        
        if os.path.exists(caminho_texto):
            # Move a imagem e o texto para a pasta de destino
            shutil.move(caminho_imagem, os.path.join(pasta_destino, nome_arquivo))
            shutil.move(caminho_texto, os.path.join(pasta_destino, arquivo_texto))
            print(f"Arquivos '{nome_arquivo}' e '{arquivo_texto}' movidos para '{pasta_destino}'.")

print("Programa concluído.")
