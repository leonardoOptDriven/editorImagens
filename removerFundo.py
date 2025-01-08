from rembg import remove
from PIL import Image


path_images = "D:/DOCUMENTOS-D/imagens/GUN_IMAGENS/t4s_1/teste.jpg"
path_saida = "./teste.png"

input = Image.open(path_images)
saida = remove(input)

saida.save(path_saida)
