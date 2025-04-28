import requests
from PIL import Image
import torch
from time import perf_counter

device = "cuda" if torch.cuda.is_available() else "cpu"

print("=============================================")
print(f"=============={device}======================")
print("=============================================")

def to_binary(answer):
    if len(answer) > 0:
        return 1
    else:
        return 0

def get_huggingface_model(model_name):
    from transformers import Owlv2Processor, Owlv2ForObjectDetection
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"

    processor = Owlv2Processor.from_pretrained(model_name)
    model = Owlv2ForObjectDetection.from_pretrained(model_name).to(device)

    return model, processor


def detect(img, prompt, model, processor):
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"

    start = perf_counter()
    texts = [prompt.split(';')]

    inputs = processor(text=texts, images=img, return_tensors="pt").to(device)

    with torch.no_grad():
      outputs = model(**inputs)

    # Target image sizes (height, width) to rescale box predictions [batch_size, 2]
    target_sizes = torch.Tensor([img.size[::-1]])
    # Convert outputs (bounding boxes and class logits) to Pascal VOC Format (xmin, ymin, xmax, ymax)
    results = processor.post_process_object_detection(outputs=outputs, target_sizes=target_sizes, threshold=0.1)
    i = 0  # Retrieve predictions for the first image for the corresponding text queries
    text = texts[i]
    boxes, scores, labels = results[i]["boxes"], results[i]["scores"], results[i]["labels"]

    boxes, scores, labels = nms(boxes, scores, labels, iou_threshold=0.0)

    for box, score, label in zip(boxes, scores, labels):
        box = [round(i, 2) for i in box.tolist()]
        #print(f"Detected {text[label]} with confidence {round(score.item(), 3)} at location {box}")

    end = perf_counter()
    latency = end-start
    #print(f'latency: {end-start}')
    detection = to_binary(boxes)

    return detection, round(latency,3), boxes, labels, scores

def plot_results(image, bboxes, labels_detected, scores, labels):
    import cv2

    #print(results.boxes.data.cpu().numpy())
    for bbox, cls, conf in zip(bboxes, labels_detected, scores):  # results.xyxy contÃ©m as coordenadas dos bboxes
        x1, y1, x2, y2 = bbox  # Desempacotando as coordenadas e os dados de detecÃ§Ã£o
        label = labels[cls]  # Nome da classe da detecÃ§Ã£o

        # Desenhando o bounding box na imagem
        color = (0, 255, 0)  # Cor do bounding box (verde)
        thickness = 2  # Espessura do bounding box

        # Desenhando o retÃ¢ngulo
        image = cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)

        # Colocar o nome da classe e a confianÃ§a no topo do bounding box
        label_text = f"{label} {conf:.2f}"
        image = cv2.putText(image, label_text, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)



def plot_detections(image, bboxes, labels_detected, scores, labels):
    # Espera receber coordenadas xc, yc, w, h

    import cv2
    import numpy as np



    #print(results.boxes.data.cpu().numpy())
    #image = image.convert('RGB')
    image = np.array(image)
    for bbox, cls, conf in zip(bboxes, labels_detected, scores):  # results.xyxy contÃ©m as coordenadas dos bboxes

        img_h, img_w, _ = image.shape
        xc, yc, w, h = bbox  # Desempacotando as coordenadas e os dados de detecÃ§Ã£o

        xc = xc*img_w
        yc = yc*img_h
        w = w*img_w
        h = h*img_h

        x1 = xc - w/2
        x2 = x1 + w
        y1 = yc - h/2
        y2 = y1 + h


        label = labels[cls]  # Nome da classe da detecÃ§Ã£o

        # Desenhando o bounding box na imagem
        color = (0, 255, 0)  # Cor do bounding box (verde)
        thickness = 2  # Espessura do bounding box

        # Desenhando o retÃ¢ngulo
        image = cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)

        # Colocar o nome da classe e a confianÃ§a no topo do bounding box
        label_text = f"{label} {conf:.2f}"
        image = cv2.putText(image, label_text, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return image

def nms(bboxes, scores, labels, iou_threshold=0.0):
    import torchvision
    import torch
    import numpy as np

    bboxes_nms = bboxes
    scores_nms = scores
    labels_nms = labels

    bboxes = bboxes.cpu()
    scores = scores.cpu()
    labels = labels.cpu()

    indexes_to_keep = torchvision.ops.nms(boxes=bboxes, scores=scores, iou_threshold=iou_threshold)
    bboxes_nms = bboxes[indexes_to_keep.tolist()]
    scores_nms = scores[indexes_to_keep.tolist()]
    labels_nms = labels[indexes_to_keep.tolist()]

    return bboxes_nms, scores_nms, labels_nms

def filter_image(image):
    import numpy as np
    import cv2
    from PIL import Image

    image = np.array(image)

    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Split channels
    l, a, b = cv2.split(lab)

    # Apply CLAHE to the L-channel
    clahe = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(2,2))
    l_enhanced = clahe.apply(l)

    # Merge the channels back
    lab_enhanced = cv2.merge((l_enhanced, a, b))

    # Convert back to BGR color space
    image =cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)

    image = Image.fromarray(image)

    return image

def main():
    import sys
    import cv2
    from PIL import Image, ImageEnhance
    import numpy as np

    #from gun_detection_owlv2 import get_hugginface_model, detect

    img_path = sys.argv[1]
    prompt='Handgun; Rifle; Shotgun; Submachine Gun; Machine Gun; Assault Rifle; Personal Defense Weapon (PDW); Anti-Material Rifle; Historical Firearm'
    classes = [el.strip() for el in prompt.split(';')]
    if len(sys.argv) > 2:
        prompt = sys.argv[2]

    model, processor = get_huggingface_model(model_name="./owlv2-base-patch16-ensemble")

    image = Image.open(img_path).convert('RGB')

    image = filter_image(image)

    detection, latency, boxes, labels, scores = detect(image, prompt, model, processor)

    boxes, scores, labels = nms(boxes, scores, labels)

    print('detection [bool]: ', detection)
    print('latency [s]: ', latency)
    print('bboxes [xyxy]: ', boxes)
    print('label idxs: ', labels)
    print('classes: ', [classes[i] for i in labels])
    #iif detection == 1:
    import cv2
    bbox_plot = plot_detections(image, boxes, labels, scores, classes)
    cv2.imwrite(f'./owlv2_detection.png', cv2.cvtColor(bbox_plot, cv2.COLOR_RGB2BGR))

if __name__ == '__main__':
    main()