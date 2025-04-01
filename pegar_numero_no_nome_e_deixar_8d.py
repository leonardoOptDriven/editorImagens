import os
import re

def substituir_nomes(arquivo):
    """Extrai um número da string e o formata para 8 dígitos com zeros à esquerda."""
    v_numero = re.findall(r'\d+', arquivo)  # Encontra todos os números na string
    
    if v_numero:  # Se houver números encontrados
        numero = int(v_numero[0])  # Pega o primeiro número encontrado
        novo_nome = str(numero).zfill(8)  # Formata para 8 dígitos com zeros à esquerda
    else:
        novo_nome = "00000000"  # Se não houver número, retorna 8 zeros

    return novo_nome

def renomear_arquivos(pasta):
    """Renomeia todos os arquivos da pasta usando a função substituir_nomes()."""
    if not os.path.exists(pasta):
        print(f"A pasta '{pasta}' não existe.")
        return
    
    for arquivo in os.listdir(pasta):
        caminho_antigo = os.path.join(pasta, arquivo)

        if os.path.isfile(caminho_antigo):  # Apenas arquivos, ignora pastas
            nome, extensao = os.path.splitext(arquivo)  # Divide nome e extensão
            novo_nome = "frame_" + substituir_nomes(nome) + extensao  # Mantém a extensão
            
            caminho_novo = os.path.join(pasta, novo_nome)

            if caminho_antigo != caminho_novo:  # Evita renomear para o mesmo nome
                os.rename(caminho_antigo, caminho_novo)
                print(f'Renomeado: "{arquivo}" → "{novo_nome}"')
            else:
                print(" ============================================ ")
                print(" ================= ERRO ===================== ")
                print(" ============================================ ")

# 🔹 Altere aqui para a pasta que deseja renomear os arquivos
pasta = "E:/GUN_IMAGENS/guilherme_fabrica_t4s_LABEL/validacao/futuramente_por_label"  # Substitua pelo caminho real
pasta = "E:/GUN_IMAGENS/guilherme_fabrica_t4s_LABEL/v_fabrica_6_limpo/images"
renomear_arquivos(pasta)
