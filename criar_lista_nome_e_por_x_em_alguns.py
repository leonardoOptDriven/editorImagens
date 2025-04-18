import os
import re
import pandas as pd

# Intervalos fornecidos


intervalos = [
   (1,1489),(1509,1520),(1541,1542),(1545,1546),(1565,1626),(1719,1730),(1774,1791),(1855,1868),(1881,1940),(1945,1946),(1953,2007),(2012,2016),(2098,2606),(2976,2977),(3212,3216),(3230,4468),(4859,4962),(4975,5001),(5004,5014),(5029,5045),(5156,6248),(6710,6711),(6831,6838),(6966,8064),(8211,8288),(9017,9716),(10321,15932)
]

# na pasta 4 
#  (1,228),(249,720),(861,1329),(1365,1474),(1554,1906),
#               (1971,2286),(2348,2618),(2652,3473),(3536,3814),
#               (3910,4136),(4175,4343),(4351,4485),(4498,4907),
#               (4946,5273),(5313,5517), (5542,5550),(5585,5842),
#               (5898,6276),(6315,6412),(6445,6607),(6615,6836),
#               (6919,7070),(7111,8280),(8304,8392),(8401,8681),
#               (8739,8949),(8971,9913),(9917,9927),(9947,10002),
#               (10017,10028),(10033,10418),(10434,10645),(10652,10656),
#               (10672,10777),(10880,11318),(11368,11467),
#               (11493,11662),(11971,11966),(11972,12411)

# na pasta 3 o video tem numeracao string talvez tenha que corrigir 
# (1,229),  (241,729), (874,1033),(1037,1318),(1378,1469),(1545,1917),(1983,2275), 
# (2342,2617),(2662,3483),(3549,3806),(3897,4146),(4184,4332),(4356,4487),(4491,4919),
# (4956,5264),(5305,5514),(5549,5552),(5578,5848),(5898,5899),(5917,6272),(6310,6424),
# (6449,6608),(6623,6822),(6893,7084),(7123,8288),(8309,8692),(8751,8941),
# (8966,10814),(10894,11322),(11381,11462),(11505,1654),(11724,11749),(11792,12419)

#cenario 4 parte 1_02 
#    (1033, 1049),(1316,1992),(2277,2669),(2758,2764),(2787,3553),(3808,4190),(4332,4961),(5072,5147),
#    (5263,5925),(6270,6635),(6822,7125),(7349,8756),(8942,10905),(11091,11107),(11148,11390),(11438,11510),
#    (11639,12414)
#

# CENÁRIO 4 PARTE 1
#    (0, 253), (331, 336), (723, 1558), (1674, 1686),
#     (1909, 2352), (2602,2822), (2834,2857),(2993,3218), (3477,3925),(4139,4506), (4712,4721),
#     (4909,5320), (5402,5589),(5841,6323),(6415,6926),(7071,7352),(8687,8978),(9672,9676),(9684,9688),
#     (9692,9694),(9701,10130),(10393,10441),(10638,10679),(10715,10721),(10734,11796),(11859,11864),
#     (11876,12414)

def verificar_numero(numero, intervalos):
    """Verifica se um número está em algum dos intervalos fornecidos."""
    return any(inicio <= numero <= fim for inicio, fim in intervalos)

def processar_arquivos(pasta):
    """Cria ou atualiza um arquivo Excel com os nomes dos arquivos e marcação dos intervalos."""
    # Caminho do arquivo Excel
    caminho_excel = os.path.join("./", "CENARIO_04_PARTE_1_05.xlsx")

    # Verificar se o arquivo já existe
    if os.path.exists(caminho_excel):
        # Carregar os dados existentes
        df = pd.read_excel(caminho_excel)
    else:
        # Criar um DataFrame vazio com as colunas esperadas
        df = pd.DataFrame(columns=["Nome", "SEM_ARMA"])

    # Listar arquivos na pasta
    for arquivo in os.listdir(pasta):
        if not arquivo.endswith(".png"):
            continue
        
        # print(f"arquivo {arquivo}")
        # Extrair número inicial do nome do arquivo
        match = re.search(r"(\d+)(?!.*\d)", arquivo)
        # print(f"numero match: {match}")
        # print(f"limpo {int(match.group(1))}")
        
        # break
        if match:
            numero = int(match.group(1))
            # Verificar se o número está em algum intervalo
            x = "X" if verificar_numero(numero, intervalos) else ""
        else:
            x = ""

        # Adicionar o arquivo ao DataFrame, se ainda não estiver presente
        if not df["Nome"].str.contains(arquivo).any():
            df = pd.concat([df, pd.DataFrame({"Nome": [arquivo], "SEM_ARMA": [x]})], ignore_index=True)

    # Salvar o DataFrame no arquivo Excel
    df.to_excel(caminho_excel, index=False)
    print(f"Planilha salva em: {caminho_excel}")

# Substitua 'sua_pasta' pelo caminho da pasta onde estão os arquivos
pasta = "E:/GUN_IMAGENS/paraguai/picotado_validacao_cenario_4/CENARIO_04_PARTE_1_05/"
processar_arquivos(pasta)
