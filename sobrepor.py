from PIL import Image
import os
import random

def sobrepor_imagens(pasta_png, pasta_fonte, pasta_resultados):
    # Certifica-se de que a pasta de resultados existe
    os.makedirs(pasta_resultados, exist_ok=True)

    # Lista as imagens da pasta PNG
    imagens_png = [f for f in os.listdir(pasta_png) if f.endswith('.png')]

    # Lista as imagens da pasta FONTE
    imagens_fonte = [f for f in os.listdir(pasta_fonte) if f.endswith(('.png', '.jpg', '.jpeg'))]

    for img_png_nome in imagens_png:
        caminho_img_png = os.path.join(pasta_png, img_png_nome)
        img_png = Image.open(caminho_img_png).convert("RGBA")

        for img_fonte_nome in imagens_fonte:
            caminho_img_fonte = os.path.join(pasta_fonte, img_fonte_nome)
            img_fonte = Image.open(caminho_img_fonte).convert("RGBA")

            
            variador = random.uniform(1, 1.20) 
            # print(variador)
            # Calcula a posição no canto inferior esquerdo
            posicao = (int((img_fonte.width/2)*variador), int((img_fonte.height/2)*variador))

            # Cria uma cópia da imagem fonte para preservar a original
            resultado = img_fonte.copy()
            resultado.paste(img_png, posicao, img_png)

            # Salva a imagem resultante
            nome_resultado = f"{os.path.splitext(img_png_nome)[0]}_fundo_{os.path.splitext(img_fonte_nome)[0]}.png"
            caminho_resultado = os.path.join(pasta_resultados, nome_resultado)
            resultado.save(caminho_resultado, "PNG")

if __name__ == "__main__":
    pasta_png = "D:/DOCUMENTOS-D/imagens/GUN_IMAGENS/MONTAGEM/png"
    pasta_fonte = "D:/DOCUMENTOS-D/imagens/GUN_IMAGENS/frames/frontal_esquerda_2/aqui"
    pasta_resultados = "RESULTADOS"

    sobrepor_imagens(pasta_png, pasta_fonte, pasta_resultados)
    print(f"Imagens processadas e salvas em '{pasta_resultados}'!")
