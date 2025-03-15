# Definição dos tempos de vídeo em cada cenário
cenarios = {
    "cenário 1": [3, 49],
    "cenário 2": [4, 13, 3, 24],
    "cenário 3": [1, 39, 3, 36, 4, 41, 1, 22],
    "cenário 4": [0, 42, 4, 11],
    "cenário 5": [2, 18, 1, 44, 0, 42],
    "cenário 6 (contraste)": [2, 20],
}

# Função para calcular o tempo total em horas e minutos
def calcular_tempo_total(cenarios):
    tempos_totais = {}
    total_minutos = 0

    for nome, tempos in cenarios.items():
        horas = sum(tempos[::2])  # Soma das horas
        minutos = sum(tempos[1::2])  # Soma dos minutos

        # Convertendo minutos extras para horas
        horas += minutos // 60
        minutos = minutos % 60

        # Salvando o tempo total de cada cenário
        tempos_totais[nome] = (horas, minutos)
        total_minutos += horas * 60 + minutos

    # Convertendo o tempo total geral
    total_horas = total_minutos // 60
    total_minutos = total_minutos % 60

    return tempos_totais, (total_horas, total_minutos)

# Calculando os tempos
tempos_por_cenario, tempo_total = calcular_tempo_total(cenarios)

tempos_por_cenario, tempo_total
