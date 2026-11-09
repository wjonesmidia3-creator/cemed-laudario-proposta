"""Relatório semanal 02 a 08/11/2026 (comparado com 26/10 a 01/11/2026).

Dados extraídos do Reportei em 09/11/2026 (Meta Ads, Google Ads, Instagram
Business, Página do Facebook, Google Meu Negócio, YouTube e ChatGPT Ads).
"""
from gerar import delta_linha, f_brl, f_int

SEMANA = {
    "prev_curto": "26/10 a 01/11",
    "cur_curto": "02 a 08/11",
    "cur_longo": "02 a 08 de novembro/2026",
    "dias": ["26/10", "27/10", "28/10", "29/10", "30/10", "31/10", "01/11",
             "02/11", "03/11", "04/11", "05/11", "06/11", "07/11", "08/11"],
    "pasta": "2026-11-02_a_08",
    "sufixo": "02-08nov2026",
}


def K(valor, rotulo, cur, prev, melhor, sufixo="vs. sem. anterior"):
    return {"valor": valor, "rotulo": rotulo, "delta": delta_linha(cur, prev, melhor, sufixo)}


def hl(t):
    return f'<span class="hl">{t}</span>'


FONTE = "Fonte: Reportei ({canais}). Semana com feriado de Finados (02/11). "

CLIENTES = []

# =====================================================================  EGO
CLIENTES.append({
    "arquivo": "EGO_Odontologia",
    "nome": "EGO Odontologia",
    "titulo": [f"Semana de {hl('verba menor')}.", "Contato segue barato."],
    "lead": "Resumo semanal de <b>anúncios Meta, Google Ads, Instagram e Facebook</b> da EGO Odontologia, "
            "comparando a semana de 02 a 08/11 com a semana anterior (26/10 a 01/11).",
    "destaque": {
        "num": "35", "rotulo": "CONVERSAS",
        "titulo": f"Com {hl('37% menos investimento')}, a semana gerou 35 conversas a {hl('R$ 18,10')} cada.",
        "texto": "O custo por conversa subiu frente à semana anterior (R$ 13,96), mas segue menos da metade "
                 "do registrado no início de outubro (R$ 37,81).",
    },
    "faixa": [
        (f"R$ {hl('633')}", "investidos em Meta Ads na semana (anterior: R$ 1.005)"),
        (f"R$ {hl('18,10')}", "custo por conversa iniciada (anterior: R$ 13,96)"),
        (f"4 {hl('leads')}", "cadastros pelos anúncios, contra 1 na semana anterior"),
        (f"2 {hl('posts')}", "novos no Instagram; Reels com 14,3% de engajamento"),
    ],
    "intro_p2": "A semana teve <b>37% menos verba</b> no Meta Ads e o volume de conversas acompanhou. "
                "O custo por resultado segue baixo para o histórico da conta.",
    "kpis": [
        K('35<small>/72</small>', "Conversas iniciadas<br>esta semana / anterior", 35, 72, "up"),
        K("R$ 18,10", "Custo por conversa<br>esta semana", 18.0951, 13.9628, "down"),
        K("R$ 633", "Investimento em<br>Meta Ads", 633.33, 1005.32, None),
        K("5.933", "Alcance no Instagram<br>(soma diária)", 5933, 8306, "up"),
    ],
    "grupos": [
        {"titulo": "ANÚNCIOS · META ADS", "linhas": [
            ("Conversas iniciadas", 72, 35, "int", "up", True),
            ("Custo por conversa", 13.9628, 18.0951, "brl", "down", True),
            ("Investimento", 1005.32, 633.33, "brl", None),
            ("Alcance", 19148, 12985, "int", "up"),
            ("Impressões", 44074, 22874, "int", "up"),
            ("Custo por clique", 0.4448, 0.5522, "brl", "down", True),
        ]},
        {"titulo": "GOOGLE ADS", "linhas": [
            ("Investimento", 75.57, 41.68, "brl", None),
            ("Cliques", 13, 9, "int", "up"),
        ]},
        {"titulo": "INSTAGRAM", "linhas": [
            ("Alcance (soma diária)", 8306, 5933, "int", "up"),
            ("Visualizações", 12531, 8570, "int", "up"),
            ("Novos seguidores", 21, 12, "int", "up"),
        ]},
        {"titulo": "FACEBOOK", "linhas": [
            ("Alcance da página", 28133, 16256, "int", "up"),
        ]},
    ],
    "grafico": {"titulo": "Alcance diário no Instagram", "sub": "Pessoas alcançadas por dia, de 26/10 a 08/11",
                "prev": [2338, 1416, 979, 717, 823, 906, 1127], "cur": [876, 114, 92, 1349, 1328, 1670, 504]},
    "fonte": FONTE.format(canais="Meta Ads, Google Ads, Instagram Business e Página do Facebook")
             + "Alcance do Instagram é a soma do alcance diário.",
    "titulo_p3": 'Conteúdo e <em>próximos passos</em>',
    "intro_p3": "Duas publicações no Instagram na semana. O Reels educativo sobre <b>tabagismo e implantes</b> "
                "foi o conteúdo com mais interações.",
    "posts": [
        {"data": "03/NOV", "tag": "REELS · MAIS ENGAJAMENTO", "titulo": "Tabagismo e implantes dentários",
         "metricas": [("308", "views"), ("27", "interações"), ("14,3%", "eng.")]},
        {"data": "06/NOV", "tag": "CARROSSEL", "titulo": "Hábitos que podem causar mau hálito",
         "metricas": [("165", "views"), ("7", "interações"), ("12,5%", "eng.")]},
    ],
    "insights": [
        ("neu", "Conversas acompanharam a verba",
         "O investimento caiu <b>37%</b> e as conversas caíram <b>51%</b>. O volume responde diretamente ao orçamento."),
        ("bom", "Custo ainda competitivo",
         "<b>R$ 18,10</b> por conversa: acima da semana anterior, mas bem abaixo dos R$ 37,81 do início de outubro."),
        ("ruim", "Google Ads com pouco volume",
         "Apenas <b>9 cliques</b> e R$ 41,68 investidos na semana, sem conversões registradas."),
    ],
    "leitura": "A semana foi mais curta em orçamento e o resultado acompanhou. Como o custo por conversa segue saudável, "
               "o principal fator para recuperar volume é a <b>verba diária</b>. No conteúdo, vídeos que respondem "
               "dúvidas (implante, prótese, hábitos) seguem sendo os que mais engajam.",
    "proximos": [
        ("Retomar o ritmo de verba", "Voltar ao investimento da semana anterior para recuperar o volume de ~70 conversas por semana."),
        ("Revisar o Google Ads", "Ajustar palavras-chave e orçamento: a campanha teve só 9 cliques na semana."),
        ("Mais vídeos de dúvida", "Seguir a linha de Reels educativos e testar o de tabagismo como criativo de anúncio."),
    ],
    "nota_p3": "Visualizações e interações dos posts são orgânicas e acumuladas desde a publicação até 08/11.",
})

# =====================================================================  CEMED
CLIENTES.append({
    "arquivo": "CEMED",
    "nome": "CEMED",
    "titulo": [f"{hl('Mais resultados')}, custo menor.", "Google Ads puxou a semana."],
    "lead": "Resumo semanal de <b>anúncios Meta e Google Ads</b> do CEMED – Centro de Especialidades Médicas de Mirassol, "
            "comparando a semana de 02 a 08/11 com a semana anterior (26/10 a 01/11).",
    "destaque": {
        "num": "82", "rotulo": "CONTATOS",
        "titulo": f"{hl('66 conversões')} no Google Ads e {hl('16 conversas')} pelo Meta: 28% a mais que na semana anterior (64).",
        "texto": "Contatos somam as conversões registradas no Google Ads (todas as ações) e as conversas iniciadas "
                 "por mensagem a partir dos anúncios Meta.",
    },
    "faixa": [
        (f"R$ {hl('1.191')}", "investidos na semana em Meta + Google (anterior: R$ 1.151)"),
        (f"R$ {hl('14,53')}", "custo médio por contato (anterior: R$ 17,98)"),
        (f"{hl('+35%')}", "conversões no Google Ads vs. semana anterior"),
        (f"R$ {hl('21,33')}", "custo por conversa no Meta, 10% menor"),
    ],
    "intro_p2": "Com investimento total <b>3,5% maior</b>, a semana trouxe 28% mais contatos. "
                "O destaque foi o Google Ads, com mais conversões e custo menor por resultado.",
    "kpis": [
        K("82<small>/64</small>", "Contatos na semana<br>esta semana / anterior", 82, 64, "up"),
        K("66", "Conversões no<br>Google Ads", 66, 49, "up"),
        K("R$ 12,88", "Custo por conversão<br>no Google Ads", 12.8772, 16.2655, "down"),
        K("R$ 21,33", "Custo por conversa<br>no Meta Ads", 21.3256, 23.59, "down"),
    ],
    "grupos": [
        {"titulo": "ANÚNCIOS · META ADS", "linhas": [
            ("Conversas iniciadas", 15, 16, "int", "up", True),
            ("Custo por conversa", 23.59, 21.3256, "brl", "down", True),
            ("Investimento", 353.85, 341.21, "brl", None),
            ("Alcance", 10375, 9171, "int", "up"),
            ("Impressões", 35619, 28528, "int", "up"),
            ("Cliques no link", 203, 137, "int", "up"),
            ("Custo por clique", 1.0531, 1.3174, "brl", "down", True),
        ]},
        {"titulo": "GOOGLE ADS", "linhas": [
            ("Conversões (todas as ações)", 49, 66, "int", "up", True),
            ("Custo por conversão", 16.2655, 12.8772, "brl", "down", True),
            ("Investimento", 797.01, 849.90, "brl", None),
            ("Cliques", 205, 229, "int", "up"),
            ("Impressões", 1795, 2758, "int", "up", True),
            ("CPC médio", 3.8879, 3.7113, "brl", "down"),
        ]},
    ],
    "grafico": {"titulo": "Investimento diário em Meta Ads", "sub": "Valor investido por dia, de 26/10 a 08/11",
                "unidade": "brl",
                "prev": [50.31, 84.64, 51.95, 43.75, 40.15, 40.72, 42.33],
                "cur": [26.02, 82.17, 80.82, 46.32, 35.80, 35.12, 34.96]},
    "fonte": FONTE.format(canais="Meta Ads e Google Ads")
             + "Custo por conversão do Google = investimento ÷ conversões (todas as ações).",
    "titulo_p3": 'O que mudou e <em>próximos passos</em>',
    "intro_p3": "Os dois canais pagos ficaram mais eficientes na semana, com destaque para o <b>Google Ads</b>.",
    "insights": [
        ("bom", "Google Ads em alta",
         "Impressões <b>+54%</b> e cliques <b>+12%</b>, com 66 conversões (anterior: 49) e custo por conversão 21% menor."),
        ("bom", "Meta estável e mais barato",
         "16 conversas com investimento parecido; custo por conversa caiu de <b>R$ 23,59 para R$ 21,33</b>."),
        ("ruim", "Clique mais caro no Meta",
         "O CPC subiu <b>25%</b> (R$ 1,32) e os cliques no link caíram 33%. Sinal de desgaste dos criativos."),
    ],
    "leitura": "O <b>Google Ads</b> foi o canal mais eficiente da semana: mais conversões com custo menor por resultado. "
               "No Meta, as conversas se mantiveram mesmo com menos alcance, mas o clique ficou mais caro, o que indica "
               "necessidade de renovar as peças.",
    "proximos": [
        ("Reforçar o Google Ads", "Avaliar aumento de verba nas campanhas com melhor custo por conversão."),
        ("Novos criativos no Meta", "Testar novas peças e chamadas para baixar o CPC e recuperar cliques."),
        ("Medir agendamentos", "Cruzar os 82 contatos com os agendamentos da semana para medir a conversão real."),
    ],
})

# =====================================================================  DREISSON
CLIENTES.append({
    "arquivo": "Dreisson",
    "nome": "Dreisson",
    "titulo": [f"Mesma verba, {hl('mais conversas')}.", "Custo por conversa caiu 13%."],
    "lead": "Resumo semanal dos <b>anúncios Meta</b> do Dreisson (Vivo Imóveis), comparando a semana de "
            "02 a 08/11 com a semana anterior (26/10 a 01/11).",
    "destaque": {
        "num": "24", "rotulo": "CONVERSAS",
        "titulo": f"{hl('24 conversas')} iniciadas pelos anúncios, 3 a mais que na semana anterior, com o {hl('mesmo investimento')}.",
        "texto": "Pessoas que chamaram por mensagem (WhatsApp, Direct ou Messenger) a partir dos anúncios. "
                 "O custo por conversa caiu de R$ 23,15 para R$ 20,12.",
    },
    "faixa": [
        (f"R$ {hl('483')}", "investidos na semana (anterior: R$ 486)"),
        (f"R$ {hl('20,12')}", "custo por conversa, 13% menor"),
        (f"{hl('474')}", "cliques no link dos anúncios (anterior: 520)"),
        (f"9,1 {hl('mil')}", "pessoas alcançadas pelos anúncios"),
    ],
    "intro_p2": "Investimento praticamente igual ao da semana anterior, com <b>mais conversas</b> e "
                "<b>custo menor</b> por contato.",
    "kpis": [
        K("24<small>/21</small>", "Conversas iniciadas<br>esta semana / anterior", 24, 21, "up"),
        K("R$ 20,12", "Custo por conversa<br>esta semana", 20.1183, 23.1476, "down"),
        K("R$ 483", "Investimento em<br>Meta Ads", 482.84, 486.10, None),
        K("R$ 0,57", "Custo por clique<br>esta semana", 0.5734, 0.3786, "down"),
    ],
    "grupos": [
        {"titulo": "ANÚNCIOS · META ADS", "linhas": [
            ("Conversas iniciadas", 21, 24, "int", "up", True),
            ("Custo por conversa", 23.1476, 20.1183, "brl", "down", True),
            ("Investimento", 486.10, 482.84, "brl", None),
            ("Alcance", 12799, 9120, "int", "up"),
            ("Impressões", 25739, 19243, "int", "up"),
            ("Cliques no link", 520, 474, "int", "up"),
            ("Custo por clique", 0.3786, 0.5734, "brl", "down", True),
        ]},
        {"titulo": "META ADS · POR PLATAFORMA", "linhas": [
            ("Conversas no Facebook", 12, 13, "int", "up"),
            ("Custo por conversa no Facebook", 17.0017, 15.2154, "brl", "down", True),
            ("Conversas no Instagram", 9, 11, "int", "up"),
            ("Custo por conversa no Instagram", 31.3422, 25.9127, "brl", "down", True),
        ]},
    ],
    "grafico": {"titulo": "Investimento diário em Meta Ads", "sub": "Valor investido por dia, de 26/10 a 08/11",
                "unidade": "brl",
                "prev": [75.49, 84.78, 72.07, 58.91, 55.39, 58.55, 80.91],
                "cur": [92.57, 82.05, 73.88, 61.94, 52.65, 45.52, 74.23]},
    "fonte": FONTE.format(canais="Meta Ads"),
    "titulo_p3": 'O que mudou e <em>próximos passos</em>',
    "intro_p3": "A campanha ficou mais eficiente em gerar conversas, mesmo alcançando menos pessoas.",
    "insights": [
        ("bom", "Mais conversas pelo mesmo valor",
         "<b>+14%</b> de conversas com investimento estável (R$ 483) e custo por conversa 13% menor."),
        ("bom", "Facebook converte mais barato",
         "No Facebook a conversa custou <b>R$ 15,22</b>; no Instagram, R$ 25,91. Os dois ficaram mais baratos que na semana anterior."),
        ("ruim", "Clique mais caro",
         "O CPC subiu de <b>R$ 0,38 para R$ 0,57</b>, sem impacto no custo por conversa até aqui."),
    ],
    "leitura": "O público impactado na semana <b>converteu melhor</b>: alcance 29% menor e, ainda assim, mais conversas. "
               "O ponto de atenção é o custo por clique, que subiu 51% e pode pressionar o custo por conversa nas próximas semanas.",
    "proximos": [
        ("Qualificar as conversas", "Acompanhar quantas das 24 conversas viraram visita ou proposta de imóvel."),
        ("Renovar criativos", "Testar novos imóveis e peças para reduzir o CPC e ampliar o alcance."),
        ("Testar mais verba no Facebook", "Deslocar parte do orçamento para o Facebook, onde a conversa custou ~40% menos."),
    ],
})

# =====================================================================  D'PLACIDO
CLIENTES.append({
    "arquivo": "DPlacido",
    "nome": "D'Placido Odonto",
    "titulo": [f"{hl('110 conversas')} na semana.", "R$ 6,75 por contato."],
    "lead": "Resumo semanal de <b>anúncios Meta e Instagram</b> da D'Placido Odonto (@dralucianadeplacido), "
            "comparando a semana de 02 a 08/11 com a semana anterior (26/10 a 01/11).",
    "destaque": {
        "num": "110", "rotulo": "CONVERSAS",
        "titulo": f"Mais {hl('conversas')} e {hl('custo menor')}: 110 contatos a R$ 6,75 cada.",
        "texto": "Pessoas que chamaram a clínica por mensagem a partir dos anúncios. Na semana anterior foram 103, a R$ 7,10 cada.",
    },
    "faixa": [
        (f"R$ {hl('742')}", "investidos em Meta Ads (anterior: R$ 731)"),
        (f"R$ {hl('6,75')}", "custo por conversa, 4,9% menor"),
        (f"{hl('+9%')}", "alcance no Instagram vs. semana anterior"),
        (f"{hl('21,5%')}", "engajamento do post de 08/11"),
    ],
    "intro_p2": "Com investimento praticamente igual, a semana teve <b>mais conversas</b>, custo menor e "
                "<b>crescimento no Instagram</b>.",
    "kpis": [
        K("110<small>/103</small>", "Conversas iniciadas<br>esta semana / anterior", 110, 103, "up"),
        K("R$ 6,75", "Custo por conversa<br>esta semana", 6.7495, 7.0967, "down"),
        K("2.952", "Alcance no Instagram<br>(soma diária)", 2952, 2707, "up"),
        K("8.988", "Visualizações no<br>Instagram", 8988, 8207, "up"),
    ],
    "grupos": [
        {"titulo": "ANÚNCIOS · META ADS", "linhas": [
            ("Conversas iniciadas", 103, 110, "int", "up", True),
            ("Custo por conversa", 7.0967, 6.7495, "brl", "down", True),
            ("Investimento", 730.96, 742.45, "brl", None),
            ("Alcance", 18977, 16120, "int", "up"),
            ("Impressões", 29628, 25179, "int", "up"),
            ("Custo por clique", 1.0749, 1.2478, "brl", "down"),
        ]},
        {"titulo": "INSTAGRAM", "linhas": [
            ("Alcance (soma diária)", 2707, 2952, "int", "up", True),
            ("Visualizações", 8207, 8988, "int", "up", True),
            ("Visitas ao perfil", 93, 82, "int", "up"),
            ("Novos seguidores", 4, 7, "int", "up"),
        ]},
    ],
    "grafico": {"titulo": "Alcance diário no Instagram", "sub": "Pessoas alcançadas por dia, de 26/10 a 08/11",
                "prev": [412, 417, 74, 704, 238, 116, 746], "cur": [525, 273, 201, 342, 461, 619, 531]},
    "fonte": FONTE.format(canais="Meta Ads e Instagram Business") + "Alcance do Instagram é a soma do alcance diário.",
    "titulo_p3": 'Conteúdo e <em>próximos passos</em>',
    "intro_p3": "Uma publicação no Instagram na semana, com a melhor taxa de engajamento do período.",
    "posts": [
        {"data": "08/NOV", "tag": "IMAGEM · MAIS ENGAJAMENTO", "titulo": "“O extraordinário de Deus ainda está por vir”",
         "metricas": [("465", "views"), ("47", "interações"), ("7", "coment."), ("21,5%", "eng.")]},
    ],
    "insights": [
        ("bom", "Volume em alta",
         "<b>110 conversas</b>, 7 a mais que na semana anterior, com investimento praticamente igual."),
        ("bom", "Custo por conversa menor",
         "Caiu de <b>R$ 7,10 para R$ 6,75</b>, mesmo com o clique um pouco mais caro (R$ 1,25)."),
        ("bom", "Instagram crescendo",
         "Alcance <b>+9%</b>, visualizações +9,5% e 7 novos seguidores na semana."),
    ],
    "leitura": "Semana consistente: mais conversas, custo menor e Instagram em crescimento. O post pessoal de 08/11 teve "
               "<b>21,5% de engajamento</b> e 7 comentários — conteúdo com a voz da Dra. Luciana aproxima o público.",
    "proximos": [
        ("Manter a verba", "Sustentar o investimento atual, que entrega conversas a menos de R$ 7."),
        ("Mais conteúdo pessoal", "Intercalar posts da rotina e da história da Dra. Luciana com conteúdo de tratamentos."),
        ("Postar com mais frequência", "Foi 1 publicação na semana; mais frequência ajuda a sustentar o alcance orgânico."),
    ],
    "nota_p3": "Visualizações e interações dos posts são orgânicas e acumuladas desde a publicação até 08/11.",
})

# =====================================================================  FIORINI
CLIENTES.append({
    "arquivo": "Fiorini",
    "nome": "Fiorini Odonto",
    "titulo": [f"Meta Ads {hl('acelerou')}.", "Google Ads ficou parado."],
    "lead": "Resumo semanal de <b>anúncios Meta e Google Ads</b> da Fiorini Odonto & Estética, comparando a semana "
            "de 02 a 08/11 com a semana anterior (26/10 a 01/11).",
    "destaque": {
        "num": "75", "rotulo": "CONVERSAS",
        "titulo": f"{hl('+29% de conversas')} no Meta, com custo por conversa {hl('17% menor')}.",
        "texto": "75 pessoas chamaram a clínica por mensagem a partir dos anúncios (anterior: 58). "
                 "O custo por conversa caiu de R$ 23,77 para R$ 19,82.",
    },
    "faixa": [
        (f"R$ {hl('1.487')}", "investidos em Meta Ads (anterior: R$ 1.379)"),
        (f"R$ {hl('19,82')}", "custo por conversa no Meta Ads"),
        (f"105,8 {hl('mil')}", "impressões dos anúncios Meta, 9% a mais"),
        (f"R$ {hl('2,46')}", "investidos no Google Ads: campanha sem veiculação"),
    ],
    "intro_p2": "O Meta Ads teve <b>mais conversas e custo menor</b>. O Google Ads, por outro lado, "
                "<b>praticamente não veiculou</b> na semana.",
    "kpis": [
        K("75<small>/58</small>", "Conversas iniciadas<br>esta semana / anterior", 75, 58, "up"),
        K("R$ 19,82", "Custo por conversa<br>no Meta Ads", 19.8239, 23.7698, "down"),
        K("R$ 0,97", "Custo por clique<br>no Meta Ads", 0.9680, 1.0890, "down"),
        K("3<small>/699</small>", "Cliques no Google Ads<br>esta semana / anterior", 3, 699, "up"),
    ],
    "grupos": [
        {"titulo": "ANÚNCIOS · META ADS", "linhas": [
            ("Conversas iniciadas", 58, 75, "int", "up", True),
            ("Custo por conversa", 23.7698, 19.8239, "brl", "down", True),
            ("Investimento", 1378.65, 1486.79, "brl", None),
            ("Alcance", 32924, 34148, "int", "up"),
            ("Impressões", 96974, 105796, "int", "up"),
            ("Cliques no link", 505, 505, "int", "up"),
            ("Custo por clique", 1.0890, 0.9680, "brl", "down", True),
        ]},
        {"titulo": "GOOGLE ADS", "linhas": [
            ("Investimento", 425.64, 2.46, "brl", None),
            ("Cliques", 699, 3, "int", "up", True),
            ("Impressões", 10988, 44, "int", "up"),
            ("Conversões (todas as ações)", 3, 0, "int", "up"),
        ]},
    ],
    "grafico": {"titulo": "Investimento diário em Meta Ads", "sub": "Valor investido por dia, de 26/10 a 08/11",
                "unidade": "brl",
                "prev": [229.92, 264.23, 242.47, 209.60, 146.77, 137.99, 147.67],
                "cur": [236.41, 272.85, 258.71, 236.33, 189.95, 151.97, 140.57]},
    "fonte": FONTE.format(canais="Meta Ads e Google Ads") + "A página do Facebook está com a integração inativa no Reportei.",
    "titulo_p3": 'O que mudou e <em>próximos passos</em>',
    "intro_p3": "Melhor semana do Meta Ads no comparativo, e um alerta importante no Google Ads.",
    "insights": [
        ("bom", "Meta mais eficiente",
         "Conversas <b>+29%</b>, CPC <b>−11%</b> e alcance +4%, com 8% a mais de investimento."),
        ("ruim", "Google Ads sem veiculação",
         "Só <b>R$ 2,46</b> investidos e 3 cliques na semana, contra 699 cliques na anterior."),
        ("neu", "Verba concentrada no início da semana",
         "Nas duas semanas, o investimento diário no Meta cai de <b>sexta a domingo</b>."),
    ],
    "leitura": "O Meta Ads entregou mais conversas com custo menor. Em compensação, o <b>Google Ads ficou praticamente "
               "sem veiculação</b> — vale checar pagamento, orçamento ou status da campanha para não perder quem procura "
               "a clínica no Google.",
    "proximos": [
        ("Reativar o Google Ads", "Verificar forma de pagamento, orçamento e status da campanha e retomar a veiculação."),
        ("Manter o ritmo no Meta", "Sustentar a verba atual, que entrega conversas abaixo de R$ 20."),
        ("Acompanhar agendamentos", "Cruzar as 75 conversas com os agendamentos da semana para medir a conversão."),
    ],
})

# =====================================================================  SANRIRE
CLIENTES.append({
    "arquivo": "Instituto_Sanrire",
    "nome": "Instituto Sanrire",
    "titulo": [f"Conversa {hl('19% mais barata')}.", "Google Ads estável."],
    "lead": "Resumo semanal de <b>anúncios Meta, Google Ads e ChatGPT Ads</b>, além de <b>Facebook e YouTube</b>, "
            "do Instituto Sanrire, comparando a semana de 02 a 08/11 com a semana anterior (26/10 a 01/11).",
    "destaque": {
        "num": "30", "rotulo": "CONVERSAS",
        "titulo": f"{hl('30 conversas')} pelo Meta, com custo por conversa {hl('19% menor')} (R$ 64,93).",
        "texto": "Na semana anterior foram 26 conversas a R$ 80,15 cada. No Google Ads, as conversões principais "
                 "ficaram em 33 (anterior: 32).",
    },
    "faixa": [
        (f"R$ {hl('3.802')}", "investidos em Meta, Google e ChatGPT Ads (anterior: R$ 3.999)"),
        (f"R$ {hl('64,93')}", "custo por conversa no Meta (anterior: R$ 80,15)"),
        (f"{hl('33')}", "conversões principais no Google Ads (96 em todas as ações)"),
        (f"38,7 {hl('mil')}", "alcance da página no Facebook, 6% a mais"),
    ],
    "intro_p2": "Investimento total <b>5% menor</b>, com mais conversas no Meta e conversões estáveis no Google Ads.",
    "kpis": [
        K("30<small>/26</small>", "Conversas iniciadas<br>no Meta Ads", 30, 26, "up"),
        K("R$ 64,93", "Custo por conversa<br>no Meta Ads", 64.9333, 80.15, "down"),
        K("33", "Conversões principais<br>no Google Ads", 33.0, 31.8, "up"),
        K("R$ 3.802", "Investimento total<br>(Meta + Google + ChatGPT)", 3802.22, 3999.06, None),
    ],
    "denso": True,
    "grupos": [
        {"titulo": "ANÚNCIOS · META ADS (CA 03)", "linhas": [
            ("Conversas iniciadas", 26, 30, "int", "up", True),
            ("Custo por conversa", 80.15, 64.9333, "brl", "down", True),
            ("Investimento", 2083.90, 1948.00, "brl", None),
            ("Alcance", 21419, 23018, "int", "up"),
            ("Cliques no link", 441, 322, "int", "up"),
            ("Custo por clique", 3.7146, 4.3677, "brl", "down"),
        ]},
        {"titulo": "GOOGLE ADS", "linhas": [
            ("Conversões principais", 31.8, 33.0, "int", "up", True),
            ("Investimento", 1635.62, 1726.98, "brl", None),
            ("Cliques", 7928, 5319, "int", "up"),
            ("Impressões", 231595, 199124, "int", "up"),
        ]},
        {"titulo": "CHATGPT ADS", "linhas": [
            ("Investimento", 279.54, 127.24, "brl", None),
            ("Cliques", 38, 14, "int", "up"),
        ]},
        {"titulo": "FACEBOOK · YOUTUBE", "linhas": [
            ("Alcance da página (Facebook)", 36440, 38679, "int", "up"),
            ("Visualizações (YouTube)", 28232, 3215, "int", "up", True),
        ]},
    ],
    "grafico": {"titulo": "Alcance diário da página no Facebook", "sub": "Pessoas alcançadas por dia, de 26/10 a 08/11",
                "prev": [4835, 5026, 6438, 4823, 4289, 5239, 5790], "cur": [6388, 7032, 6002, 5853, 4193, 4633, 4578]},
    "fonte": FONTE.format(canais="Meta Ads, Google Ads, ChatGPT Ads, Página do Facebook e YouTube")
             + "A conta de anúncios CA 02 não teve veiculação nas duas semanas. Google Ads: conta Dra. Ingrid Aquino.",
    "titulo_p3": 'O que mudou e <em>próximos passos</em>',
    "intro_p3": "Mais eficiência no Meta, volume estável no Google e um canal novo em teste (ChatGPT Ads).",
    "insights": [
        ("bom", "Meta mais eficiente",
         "Mais conversas (<b>30</b>) e custo por conversa <b>19% menor</b>, com 6,5% a menos de investimento."),
        ("bom", "Google Ads estável",
         "<b>33 conversões principais</b> (96 em todas as ações), mesmo com 33% menos cliques."),
        ("neu", "ChatGPT Ads em teste",
         "R$ 127 investidos e <b>14 cliques</b> (CPC de R$ 9,09), sem conversões registradas na semana."),
        ("ruim", "YouTube e Instagram",
         "Visualizações no YouTube caíram de 28,2 mil para <b>3,2 mil</b>. O Instagram não retornou dados de alcance no período."),
    ],
    "leitura": "O Meta Ads melhorou a eficiência: mais conversas gastando menos. O Google Ads manteve o volume de "
               "conversões com menos cliques, sinal de <b>tráfego mais qualificado</b>. O ChatGPT Ads ainda não gerou "
               "conversões e merece acompanhamento antes de ampliar a verba.",
    "proximos": [
        ("Escalar o que converte", "Direcionar verba para os conjuntos do Meta com menor custo por conversa."),
        ("Avaliar o ChatGPT Ads", "Definir meta e prazo de teste; sem conversões, reduzir ou pausar."),
        ("Reconectar o Instagram", "Revisar permissões da conta no Reportei para voltar a medir alcance e posts."),
    ],
})

# =====================================================================  LUISA ALVES
CLIENTES.append({
    "arquivo": "Luisa_Alves_Tattoo",
    "nome": "Luisa Alves Tattoo",
    "titulo": [f"Anúncios {hl('pausados')} desde 31/10.", "O alcance caiu junto."],
    "lead": "Resumo semanal de <b>anúncios Meta, Instagram e Facebook</b> do estúdio Luisa Alves Tattoo (@luisaalvestattoo), "
            "comparando a semana de 02 a 08/11 com a semana anterior (26/10 a 01/11).",
    "destaque": {
        "num": "R$ 0", "rotulo": "INVESTIDOS",
        "titulo": f"Sem anúncios no ar, o Instagram passou de {hl('~39 mil')} para {hl('~20 pessoas')} alcançadas por dia.",
        "texto": "A última veiculação foi em 31/10 (R$ 21,01). Na semana anterior, os anúncios geraram 9 conversas e "
                 "1.637 cliques no link com R$ 241,33 investidos.",
    },
    "faixa": [
        (f"R$ {hl('0')}", "investidos em anúncios na semana (anterior: R$ 241)"),
        (f"{hl('141')}", "alcance do Instagram na semana (anterior: 192,9 mil)"),
        (f"0 {hl('posts')}", "publicados no Instagram nas duas últimas semanas"),
        (f"{hl('9')}", "conversas na semana anterior, com anúncios ativos"),
    ],
    "intro_p2": "Com os anúncios pausados, <b>todas as frentes caíram</b>: alcance, visualizações, visitas ao perfil e conversas.",
    "kpis": [
        K("R$ 0", "Investimento em<br>Meta Ads", 0, 241.33, None),
        K("0<small>/9</small>", "Conversas iniciadas<br>esta semana / anterior", 0, 9, "up"),
        K("141", "Alcance no Instagram<br>(soma diária)", 141, 192906, "up"),
        K("29", "Visitas ao perfil<br>no Instagram", 29, 336, "up"),
    ],
    "grupos": [
        {"titulo": "ANÚNCIOS · META ADS", "linhas": [
            ("Investimento", 241.33, 0, "brl", None, True),
            ("Conversas iniciadas", 9, 0, "int", "up", True),
            ("Custo por conversa", 26.8144, None, "brl", "down"),
            ("Alcance", 22465, 0, "int", "up"),
            ("Cliques no link", 1637, 0, "int", "up"),
        ]},
        {"titulo": "INSTAGRAM", "linhas": [
            ("Alcance (soma diária)", 192906, 141, "int", "up", True),
            ("Visualizações", 413455, 248, "int", "up"),
            ("Visitas ao perfil", 336, 29, "int", "up"),
        ]},
        {"titulo": "FACEBOOK", "linhas": [
            ("Alcance da página", 1507, 0, "int", "up"),
        ]},
    ],
    "grafico": {"titulo": "Alcance diário no Instagram", "sub": "Pessoas alcançadas por dia, de 26/10 a 08/11",
                "prev": [43383, 36749, 35468, 38898, 32566, 5836, 6], "cur": [6, 6, 2, 6, 2, 105, 14]},
    "fonte": FONTE.format(canais="Meta Ads, Instagram Business e Página do Facebook")
             + "Contas conectadas ao Reportei em 04/11. A segunda conta de anúncios (LA Tattoo) não teve dados nas duas semanas.",
    "titulo_p3": 'O que aconteceu e <em>próximos passos</em>',
    "intro_p3": "A queda da semana tem uma causa clara: a <b>pausa dos anúncios</b> em 31/10, somada à ausência de posts.",
    "insights": [
        ("ruim", "Anúncios fora do ar",
         "A conta de anúncios <b>não veiculou</b> de 01/11 a 08/11. Última veiculação: 31/10."),
        ("ruim", "Alcance dependia da mídia paga",
         "O alcance diário caiu de <b>~39 mil</b> para perto de zero a partir de 31/10, mesma data da pausa."),
        ("ruim", "Sem publicações",
         "<b>Nenhum post novo</b> no Instagram entre 26/10 e 08/11."),
    ],
    "leitura": "O comportamento do alcance indica que <b>quase toda a visibilidade do perfil vinha dos anúncios</b>. "
               "Com a pausa em 31/10, o perfil praticamente deixou de ser visto e as conversas zeraram. "
               "Retomar a veiculação e o calendário de posts é a prioridade.",
    "proximos": [
        ("Reativar os anúncios", "Definir verba e voltar a veicular as campanhas de mensagem e alcance."),
        ("Retomar as postagens", "Publicar trabalhos recentes (Reels de processo e resultado) para alimentar o perfil."),
        ("Conferir a 2ª conta", "A conta “LA Tattoo” não teve dados no período; confirmar se deve ser usada."),
    ],
})

# =====================================================================  TRAIT
CLIENTES.append({
    "arquivo": "Trait_Odontologia",
    "nome": "Trait Odontologia",
    "titulo": [f"Semana mais {hl('fraca')} em contatos.", "Hora de ajustar campanhas."],
    "lead": "Resumo semanal de <b>anúncios Meta, Google Ads, Instagram e Google Meu Negócio</b> da Trait Odontologia, "
            "comparando a semana de 02 a 08/11 com a semana anterior (26/10 a 01/11).",
    "destaque": {
        "num": "23", "rotulo": "CONVERSAS",
        "titulo": f"Conversas pelo Meta caíram para {hl('23')} e o custo por conversa subiu para {hl('R$ 33,76')}.",
        "texto": "Na semana anterior foram 35 conversas a R$ 23,76 cada. No Google Ads, as conversões caíram de 182 para 60. "
                 "Semana com feriado de Finados (02/11).",
    },
    "faixa": [
        (f"R$ {hl('1.122')}", "investidos em Meta + Google (anterior: R$ 1.217)"),
        (f"55,7 {hl('mil')}", "alcance do Instagram na semana (soma diária)"),
        (f"53,1 {hl('mil')}", "pico de alcance diário no Instagram, em 01/11"),
        (f"4 {hl('posts')}", "publicados no Instagram na semana"),
    ],
    "intro_p2": "Investimento <b>8% menor</b> e queda de contatos nos dois canais pagos, em semana com feriado.",
    "kpis": [
        K("23<small>/35</small>", "Conversas iniciadas<br>no Meta Ads", 23, 35, "up"),
        K("R$ 33,76", "Custo por conversa<br>no Meta Ads", 33.7591, 23.7577, "down"),
        K("60<small>/182</small>", "Conversões no<br>Google Ads", 60, 182, "up"),
        K("R$ 0,50", "Custo por clique<br>no Google Ads", 0.5038, 0.5187, "down"),
    ],
    "denso": True,
    "grupos": [
        {"titulo": "ANÚNCIOS · META ADS", "linhas": [
            ("Conversas iniciadas", 35, 23, "int", "up", True),
            ("Custo por conversa", 23.7577, 33.7591, "brl", "down", True),
            ("Investimento", 831.52, 776.46, "brl", None),
            ("Alcance", 21570, 18785, "int", "up"),
            ("Custo por clique", 1.4955, 2.0220, "brl", "down", True),
        ]},
        {"titulo": "GOOGLE ADS", "linhas": [
            ("Conversões (todas as ações)", 182, 60, "int", "up", True),
            ("Investimento", 385.40, 345.13, "brl", None),
            ("Cliques", 743, 685, "int", "up"),
        ]},
        {"titulo": "INSTAGRAM · GOOGLE MEU NEGÓCIO", "linhas": [
            ("Alcance Instagram (soma diária)", 89225, 55712, "int", "up"),
            ("Visualizações Instagram", 179037, 90458, "int", "up"),
            ("Visualizações no Google", 156, 59, "int", "up"),
        ]},
    ],
    "grafico": {"titulo": "Alcance diário no Instagram", "sub": "Pessoas alcançadas por dia, de 26/10 a 08/11",
                "prev": [3549, 3515, 1789, 4382, 5897, 16982, 53111], "cur": [19704, 9697, 14515, 5842, 2497, 1890, 1567]},
    "fonte": FONTE.format(canais="Meta Ads, Google Ads, Instagram Business e Google Meu Negócio")
             + "Alcance do Instagram é a soma do alcance diário.",
    "titulo_p3": 'Conteúdo e <em>próximos passos</em>',
    "intro_p3": "Quatro publicações no Instagram na semana. O carrossel sobre <b>facetas em resina</b> teve o melhor engajamento.",
    "posts": [
        {"data": "05/NOV", "tag": "CARROSSEL · MAIS ENGAJAMENTO", "titulo": "3 motivos para conhecer as facetas em resina",
         "metricas": [("279", "views"), ("12", "interações"), ("10,7%", "eng.")]},
        {"data": "06/NOV", "tag": "REELS · MAIS ALCANCE", "titulo": "Sorriso, autoestima e confiança",
         "metricas": [("297", "views"), ("9", "interações"), ("4,5%", "eng.")]},
        {"data": "03/NOV", "tag": "REELS", "titulo": "Sorrir sem receio",
         "metricas": [("215", "views"), ("2", "interações"), ("1,3%", "eng.")]},
        {"data": "04/NOV", "tag": "REELS · IMPLANTES", "titulo": "Como funciona um implante dentário",
         "metricas": [("213", "views"), ("2", "interações"), ("1,4%", "eng.")]},
    ],
    "insights": [
        ("ruim", "Conversas mais caras",
         "Custo por conversa <b>+42%</b> (R$ 33,76) e CPC +35%: sinal de desgaste dos anúncios."),
        ("ruim", "Conversões do Google em queda",
         "<b>60 conversões</b> contra 182, com cliques e investimento quase estáveis. Vale revisar o rastreamento."),
        ("neu", "Pico no Instagram",
         "Alcance chegou a <b>53 mil</b> em 01/11 e foi caindo ao longo da semana. 1 nova avaliação 5,0 no Google."),
    ],
    "leitura": "Semana abaixo da anterior nos dois canais pagos, com feriado no início. No Meta, o clique ficou mais caro "
               "e as conversas caíram; no Google, a queda de conversões foi bem maior que a de cliques, o que pede "
               "checagem. No conteúdo, <b>carrossel educativo</b> engajou bem mais que os Reels.",
    "proximos": [
        ("Renovar criativos no Meta", "Novas peças e públicos para trazer o custo por conversa de volta para perto de R$ 24."),
        ("Checar conversões no Google", "Revisar ações de conversão e campanha para entender a queda de 182 para 60."),
        ("Mais carrosséis educativos", "O formato teve 10,7% de engajamento, bem acima dos Reels da semana (1% a 4,5%)."),
    ],
    "nota_p3": "Visualizações e interações dos posts são orgânicas e acumuladas desde a publicação até 08/11.",
})
