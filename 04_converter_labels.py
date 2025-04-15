import os
import json
import glob
from PIL import Image

def convert_labelme_to_yolo(json_path, output_dir):
    with open(json_path, 'r') as f:
        data = json.load(f)

    image_path = os.path.splitext(json_path)[0] + ".jpg"  # Assumindo que a imagem é jpg
    if not os.path.exists(image_path):
        print(f"Imagem correspondente não encontrada para {json_path}")
        return

    with Image.open(image_path) as img:
        img_width, img_height = img.size

    txt_filename = os.path.join(output_dir, os.path.basename(json_path).replace('.json', '.txt'))
    with open(txt_filename, 'w') as f:
        for shape in data['shapes']:
            label = shape['label']
            points = shape['points']

            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]
            xmin, xmax = min(x_coords), max(x_coords)
            ymin, ymax = min(y_coords), max(y_coords)

            x_center = (xmin + xmax) / 2 / img_width
            y_center = (ymin + ymax) / 2 / img_height
            width = (xmax - xmin) / img_width
            height = (ymax - ymin) / img_height

            class_id = 0  # Modifique conforme necessário para mapear classes
            f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

def process_folder(json_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    json_files = glob.glob(os.path.join(json_folder, "*.json"))

    for json_file in json_files:
        convert_labelme_to_yolo(json_file, output_folder)
    print(f"Conversão concluída! Arquivos YOLO salvos em {output_folder}")

if __name__ == "__main__":
    json_dir = "/home/guilherme_arruda/Downloads/para_por_label_treinamento_paraguai/1-20250307-154622-155813/images"
    output_dir = "/home/guilherme_arruda/Downloads/teste2"

    process_folder(json_dir, output_dir)
