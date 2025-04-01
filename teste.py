


import re


arquivo = "E:\GUN_IMAGENS\paraguai\picotado_validacao_cenario_4\CENARIO_04_PARTE_1_03\img_cont_008290.png"

match = re.search(r"(\d+)(?!.*\d)", arquivo)
numero = int(match.group(1))

print(numero)