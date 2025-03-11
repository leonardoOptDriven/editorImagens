
#IMPORTAÇÕES
import os
import json 
import shutil

# de o nome que vc quer para a pasta final com labels e images
dataset_name = 'oitavo_dataset'


# pasta onde estão os arquivos JSON e imagens do labelMe
root_path = '/mnt/d/optdriven_gun_detector/labelme_files/rotulos yotube/'

#OPara onde vão as imagens e labels após arrumar
destination_images = f'/mnt/d/optdriven_gun_detector/{dataset_name}/images/train/'
destination_labels = f'/mnt/d/optdriven_gun_detector/{dataset_name}/labels/train/'

# definir index
c = 0
#inicializa o código rodando os arquivos da root_path
for file in os.listdir(root_path):
    #print(file)
    if file.endswith('.json'):
        with open(root_path+'/'+file, 'r') as json_file:

            #abrir o json
            json_text = json.load(json_file)
            # pegar as dimensões da imagem
            img_w, img_h = json_text['imageWidth'], json_text['imageHeight']
            
            #para cada objeto marcado no labelMe
            for shape in json_text['shapes']:
                #verifica classe
                shape_type = shape['label']
                #verifica coordenadas
                shape_box = shape['points']
                # verificar qual a cordenada é a x1 e qual é a x2 (mesmo para y1 e y2)
                end_cords, init_cords = shape_box
                xa, ya = init_cords
                xb, yb = end_cords
                
                if xa < xb:
                    x1, x2 = xa, xb
                else:
                    x1, x2 = xb, xa

                if ya < yb:
                    y1, y2 = ya, yb
                else:
                    y1, y2 = yb, ya
                
                #Sabendo que toda classe A é arma 
                if shape_type == 'A':
                    cla = 0
                # sabendo que outra classe , caso fosse usar, seria pessoa armada PA
                elif shape_type == 'PA':
                    cla = 1
                else:
                # situação de contorno 
                    print(shape_type)
                    continue
                
                # calcular  e normalizar x centro, y centro, w e  h 
                xc, yc, w, h = (x1+x2)/2, (y1+y2)/2, x2-x1, y2-y1
                xc, yc, w, h = xc/img_w, yc/img_h, w/img_w, h/img_h
                
                # SUBINDO SOMENTE LABELS DE ARMAS SOZINHAS
                if cla == 0: 
                    with open(destination_labels+f'{c}_'+'nome_da_imagem'+'.txt', 'a') as txt_file:
                        yolo_string = str(cla)+' '+str(xc)+' '+str(yc)+' '+str(w)+' '+str(h)+'\n'
                        txt_file.write(yolo_string)
                    shutil.copyfile(root_path+'/'+file.replace('.json', '.jpg'), destination_images+f'{c}_'+'nome_da_imagem'+'.jpg')
    c += 1