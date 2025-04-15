# função mudar nome
def substituir_nomes(arquivo):
    import re
    """Extrai um número da string e o formata para 8 dígitos com zeros à esquerda."""
    v_numero = re.findall(r'\d+', arquivo)  # Encontra todos os números na string
    
    if v_numero:  # Se houver números encontrados
        numero = int(v_numero[0])  # Pega o primeiro número encontrado
        novo_nome = str(numero).zfill(8)  # Formata para 8 dígitos com zeros à esquerda
    else:
        novo_nome = "00000000"  # Se não houver número, retorna 8 zeros

    return novo_nome

# path do txt antigo
txt_path = "./nome_arquivo.txt"
# path do txt novo
txt_filename = "./nome_arquivo_corrigido_3.txt"


# Lê o arquivo de anotações txt
with open(txt_path, 'r') as f:
    lines = f.readlines()

with open(txt_filename, 'w') as f:
        for line in lines:
            new_line ="frame_" + substituir_nomes(line) + "." + line.split(".")[-1]
            f.write(f"{new_line}")



    