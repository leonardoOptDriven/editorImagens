import cv2
import os
import torch
import glob
import shutil
import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image
from natsort import natsorted

# Importa modelos de detecção
# Importa modelos de detecção
from gun_detection_owlv2_v2 import get_huggingface_model as hf_model
from gun_detection_owlv2_v2 import detect, plot_detections, filter_image

# Carrega os modelos
model, processor = hf_model(
    model_name='./owlv2-base-patch16-ensemble' 
    )

PROMPT="Handgun; Rifle; Shotgun; Submachine Gun; Machine Gun; Assault Rifle; Personal Defense Weapon (PDW); Anti-Material Rifle; Historical Firearm"
CLASSES = [el.strip() for el in PROMPT.split(';')]

# Função para criar diretórios, se necessário
def create_dirs(paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)

# Normaliza as bounding boxes
def normalize_bbox(bbox, w, h):
    x1, y1, x2, y2 = bbox
    xc = (x1 + x2)/2/w
    yc = (y1 + y2)/2/h
    w = (x2 - x1)/w
    h = (y2 - y1)/h
    return [xc, yc, w, h]
    #return [bbox[0]/w, bbox[1]/h, bbox[2]/w, bbox[3]/h]

# Função para processar um único vídeo
def process_video(video_path, output_root,SAVE_NO_DETECTIONS):
    video_name = video_path.stem  # Nome do vídeo sem extensão
    relative_path = video_path.relative_to(video_path.parents[2]).parent  # Mantém estrutura de pastas
    #output_folder = output_root / relative_path / video_name
    output_folder = output_root / video_name

    # Criar diretórios de saída
    bboxes_plots_path = output_folder / "plots"
    labels_path = output_folder / "labels"
    images_path = output_folder / "images"
    no_detection_path = output_folder / "no_detections"
    #create_dirs([bboxes_plots_path, labels_path, images_path, no_detection_path])
    paths_to_create = [bboxes_plots_path, labels_path, images_path]

    if SAVE_NO_DETECTIONS:
        paths_to_create.append(no_detection_path)
    create_dirs(paths_to_create)

    cap = cv2.VideoCapture(str(video_path))
    frame_count = 0
    detections = []
    indexes = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        img = Image.fromarray(frame)
        img = filter_image(img)
        w, h = img.size

        # Detecção inicial coowlv2
        detection, latency, bboxes, labels, scores = detect(
            img=img,
            model=model,
            prompt=PROMPT,
            processor=processor
        )

        detected_classes = [CLASSES[i] for i in labels]

        if detection:
            # Detecção com Florence
            #bboxes = clean_detection(bboxes, labels)

            indexes.append(frame_count)
            #detections.append((detection, latency, frame_count, scores, detected_classes, bboxes))

            # Se houver armas detectadas, salva o frame
            if detection:
                #bbox_plot = plot_bbox_cv2(image=np.array(img), data=bboxes, annotate=False)
                normalized_bboxes = [normalize_bbox(bbox, w, h) for bbox in bboxes]
                bbox_plot = plot_detections(np.array(img), normalized_bboxes, labels, scores, CLASSES)

                frame_filename = f"frame_{frame_count:06d}.jpg"
                bbox_plot_path = bboxes_plots_path / frame_filename
                img_save_path = images_path / frame_filename
                label_path = labels_path / Path(frame_filename).with_suffix(".txt")

                #cv2.imwrite(str(bbox_plot_path), frame)
                cv2.imwrite(str(bbox_plot_path), bbox_plot)
                cv2.imwrite(str(img_save_path), frame)

                # Salvar bounding boxes normalizadas
                w, h = img.size
                text_bboxes = "\n".join(
                    [f"0\t{bbox[0]}\t{bbox[1]}\t"
                     f"{bbox[2]}\t{bbox[3]}"
                     for bbox in normalized_bboxes]
                )
                with open(label_path, "w") as f:
                    f.write(text_bboxes)

        else:
            #detections.append((detection, latency, frame_count, text, answer, answer))
            indexes.append(frame_count)

            if SAVE_NO_DETECTIONS:
                # Salvar frame sem detecção
                frame_filename = f"frame_{frame_count:04d}.jpg"
                cv2.imwrite(str(no_detection_path / frame_filename), frame)

        detections.append((detection, latency, frame_filename, scores, detected_classes, bboxes))
        print(f"{indexes[-1]}-th detection {detections[-1]}")

    cap.release()

    # Salvar os resultados em CSV
    results_df = pd.DataFrame(detections, columns=['gun_detection', 'latency', 'frame', 'model_output', 'parsed_answer', 'bboxes'], index=indexes)
    results_df.to_csv(output_folder / "detections.csv")

    print(f"[INFO] Processamento finalizado para {video_name}. {len(indexes)} frames processados.")

# Função para processar todos os vídeos dentro de uma pasta e subpastas
def process_videos_in_folders(root_folder, output_root, SAVE_NO_DETECTIONS=False):
    root_folder = Path(root_folder)
    output_root = Path(output_root)

    for video_path in root_folder.rglob("*.mp4"):  # Ajuste para outros formatos, se necessário
        print(f"[INFO] Processando vídeo: {video_path}")
        process_video(video_path, output_root, SAVE_NO_DETECTIONS)

# Configurações e execução
if __name__ == "__main__":
    ROOT_VIDEOS = "D:/GUN_IMAGENS/paraguai/cenario_5_15.3_parte2/15.35-16-26"  # Pasta raiz dos vídeos
    OUTPUT_DIR = "./cenario_5_parte2"  # Pasta de saída
    SAVE_NO_DETECTIONS=True

    process_videos_in_folders(ROOT_VIDEOS, OUTPUT_DIR, SAVE_NO_DETECTIONS)
