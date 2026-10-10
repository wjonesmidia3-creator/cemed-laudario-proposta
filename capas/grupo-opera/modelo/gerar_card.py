"""Gera o card de cliente no modelo Grupo Opera ("GO." + traço dourado + nome do cliente).

O "GO." e o traço vêm exatamente do card-modelo (go-modelo-sanrire.png); só o nome muda.
Fonte do nome: Rosario Bold (a mais próxima da usada no modelo).

Uso:
  python3 gerar_card.py "CEMED" -o go-cemed.png
  python3 gerar_card.py "DREISSON" --linha2 "IMÓVEIS" -o go-dreisson-imoveis.png
"""
import argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).parent
MODELO = AQUI / "go-modelo-sanrire.png"
FONTE = str(AQUI / "Rosario-700.ttf")
FUNDO = (10, 35, 121)            # azul do modelo, #0a2379
BRANCO = (255, 255, 255)
LADO = 1280                      # card final quadrado
CAP = 114                        # altura das maiúsculas do "SANRIRE" no modelo
ESPACO = 26 / 114                # espaçamento entre letras, proporcional à altura
TOPO_NOME = 769 + 3              # +3: o modelo tem 1274 px de altura


def tamanho_para_cap(cap):
    f = ImageFont.truetype(FONTE, 1000)
    b = f.getbbox("H")
    return round(cap * 1000 / (b[3] - b[1]))


def desenhar(texto, cap, espaco, topo):
    """Desenha o texto centralizado em uma máscara e devolve (máscara, largura)."""
    f = ImageFont.truetype(FONTE, tamanho_para_cap(cap))
    y = topo - f.getbbox("H")[1]
    avancos = [f.getlength(c) for c in texto]
    total = sum(avancos) + espaco * (len(texto) - 1)

    def render(x):
        m = Image.new("L", (LADO, LADO), 0)
        d = ImageDraw.Draw(m)
        for c, a in zip(texto, avancos):
            d.text((x, y), c, font=f, fill=255)
            x += a + espaco
        return m

    m = render(LADO / 2 - total / 2)
    cols = np.where(np.array(m).max(axis=0) > 0)[0]
    # centraliza pela tinta visível, não pela caixa da fonte
    m = render(LADO / 2 - total / 2 + LADO / 2 - (cols[0] + cols[-1]) / 2)
    cols = np.where(np.array(m).max(axis=0) > 0)[0]
    return m, cols[-1] - cols[0]


def caber(texto, cap_max, largura_max, espaco_rel):
    cap = cap_max
    while cap > 20:
        _, w = desenhar(texto, cap, cap * espaco_rel, 0)
        if w <= largura_max:
            return cap
        cap -= 1
    return cap


def gerar(nome, linha2, saida):
    modelo = Image.open(MODELO).convert("RGB").crop((0, 0, LADO, 1274))
    card = Image.new("RGB", (LADO, LADO), FUNDO)
    card.paste(modelo, (0, 3))
    card.paste(Image.new("RGB", (LADO, 200), FUNDO), (0, TOPO_NOME - 40))  # apaga "SANRIRE"

    linhas = [(nome.upper(), CAP, 820 if linha2 else 1000, ESPACO, 44)]
    if linha2:
        linhas.append((linha2.upper(), 50, 820, 0.62, 0))
    y = TOPO_NOME
    for texto, cap_max, largura_max, espaco_rel, vao in linhas:
        cap = caber(texto, cap_max, largura_max, espaco_rel)
        mascara, _ = desenhar(texto, cap, cap * espaco_rel, y)
        card.paste(Image.new("RGB", card.size, BRANCO), (0, 0), mascara)
        y += cap + vao
    card.save(saida)
    print(f"ok: {saida}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("nome", help="nome do cliente (linha principal)")
    p.add_argument("--linha2", help="segunda linha menor, ex.: IMÓVEIS")
    p.add_argument("-o", "--saida", required=True, help="arquivo PNG de saída")
    a = p.parse_args()
    gerar(a.nome, a.linha2, a.saida)
