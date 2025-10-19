dicionario_sentimentos = {
    "positivo": [
        "chuva", "regular", "ideal", "favorável", "úmido", "equilibrado",
        "estável", "satisfatório", "bom", "ótimo", "produtivo",
        "abundante", "crescimento", "floração", "desenvolvimento", "rendimento",
        "colheita", "plantio", "precoce", "resiliente"
    ],

    "negativo": [
        "seca", "estiagem", "geada", "granizo", "alagamento", "enchente",
        "excesso", "escassez", "praga", "doença", "baixo", "fraco", "morte",
        "perda", "queda", "estresse", "tóxico", "insuficiente", "calor",
        "frost", "impacto", "danificado", "atraso"
    ],

    "neutro": [
        "temperatura", "umidade", "vento", "sol", "chuvisco", "nevoeiro",
        "plantação", "grãos", "campo", "lavoura", "clima", "nuvem",
        "cultivo", "milho", "soja", "trigo", "produtor", "região",
        "estação", "previsão", "monitoramento", "meteorologia"
    ]
}


def distancia_levenshtein(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)

    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        dp[i][0] = i
    for j in range(len_s2 + 1):
        dp[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            custo = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + custo
            )

    return dp[len_s1][len_s2]


def encontrar_categoria_aproximada(palavra, dicionario, limiar=1):
    for categoria, palavras in dicionario.items():
        for palavra_dicionario in palavras:
            if distancia_levenshtein(palavra, palavra_dicionario) <= limiar:
                return categoria
    return "desconhecido"



def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return [linha.strip() for linha in arquivo if linha.strip()]
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return []

def analisar_linha(linha):
    palavras = linha.lower().split()
    positivas = 0
    negativas = 0
    neutras = 0

    for palavra in palavras:
        categoria = encontrar_categoria_aproximada(palavra, dicionario_sentimentos)
        if categoria == "positivo":
            positivas += 1
        elif categoria == "negativo":
            negativas += 1
        elif categoria == "neutro":
            neutras += 1

    if positivas > max(negativas, neutras):
        return 'Positivo'
    elif negativas > max(positivas, neutras):
        return 'Negativo'
    elif neutras > max(positivas, negativas):
        return 'Neutro'
    else:
        return 'Desconhecido'


def analisador_lexico_com_resumo(nome_arquivo):
    texto = ler_arquivo(nome_arquivo)

    total_positivas = 0
    total_negativas = 0
    total_neutras = 0
    total_desconhecidas = 0
    total_palavras = 0

    linhas_positiva = []
    linhas_negativa = []

    for linha in texto:
        palavras = linha.lower().split()

        for palavra in palavras:
            total_palavras += 1
            categoria = encontrar_categoria_aproximada(palavra, dicionario_sentimentos)

            if categoria == "positivo":
                total_positivas += 1
            elif categoria == "negativo":
                total_negativas += 1
            elif categoria == "neutro":
                total_neutras += 1
            else:
                total_desconhecidas += 1

        classificacao = analisar_linha(linha)

        if classificacao == 'Positivo':
            linhas_positiva.append(linha)
        elif classificacao == 'Negativo':
            linhas_negativa.append(linha)


    print('Resumo da análise:')
    print(f'- Total de palavras positivas: {total_positivas}')
    print(f'- Total de palavras negativas: {total_negativas}')
    print(f'- Total de palavras neutras:   {total_neutras}')
    print(f'- Total de palavras desconhecidas: {total_desconhecidas}')
    print(f'- Total de palavras analisadas:   {total_palavras}\n')

    with open('analise.csv', 'w', encoding='utf-8') as arquivo:
        arquivo.write('Positivas;Negativas;Neutras;Total\n')
        arquivo.write(f'{total_positivas};{total_negativas};{total_neutras};{total_palavras}\n')

    return linhas_positiva, linhas_negativa

if __name__ == '__main__':
    instrucao = 3

    positivo, negativo = analisador_lexico_com_resumo('agro.txt')

    while instrucao != 3:
        instrucao = int(input('\nPara Salvar escolha:\n'+
                              '1 - Salvar positivo \n'+
                              '2 - Salvar negativo \n'+
                              '3 - sair \n'))

        if instrucao == 1:
            with open('linhas_positivas.txt', 'w', encoding='utf-8') as f:
                for linha in positivo:
                    f.write(linha + '\n')

        elif instrucao == 2:
            with open('linhas_negativas.txt', 'w', encoding='utf-8') as f:
                for linha in negativo:
                    f.write(linha + '\n')