import cv2
import os

def draw_yolo_bbox(image_path, txt_path, output_path=None):
    # Lê a imagem
    image = cv2.imread(image_path)
    if image is None:
        print("Imagem não encontrada!")
        return

    h, w, _ = image.shape

    # Lê o arquivo de anotações YOLO
    with open(txt_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])
        x_center, y_center, bbox_width, bbox_height = map(float, parts[1:])

        # Converte para coordenadas absolutas
        x_center *= w
        y_center *= h
        bbox_width *= w
        bbox_height *= h

        x1 = int(x_center - bbox_width / 2)
        y1 = int(y_center - bbox_height / 2)
        x2 = int(x_center + bbox_width / 2)
        y2 = int(y_center + bbox_height / 2)

        # Desenha a bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)
        cv2.putText(image, f'Class {class_id}', (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # Mostra ou salva a imagem
    if output_path:
        cv2.imwrite(output_path, image)
        print(f"Imagem salva em: {output_path}")
    else:
        cv2.imshow("BBoxes", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# --------- Exemplo de uso ---------

def processar_pasta(pasta):
    imagens = {os.path.splitext(f)[0]: os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith('.jpg')}
    anotacoes = {os.path.splitext(f)[0]: os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith('.txt')}

    for nome_base in imagens.keys() & anotacoes.keys():
        image_path = imagens[nome_base]
        txt_path = anotacoes[nome_base]
        draw_yolo_bbox(image_path, txt_path)

# Defina a pasta onde estão os arquivos
pasta = "/home/guilherme_arruda/Downloads/teste2"
processar_pasta(pasta)
