# Podcast Dr. Cesar · Roteiro de gravação

Deck do roteiro do episódio com o Dr. Cesar (cardiologia, Santo André e ABC), no padrão visual do Grupo Opera. Tudo fica num único `index.html` (HTML, CSS e JS no mesmo arquivo, sem build). A única dependência externa são as fontes do Google.

| Arquivo | O que é |
|---|---|
| `index.html` | O deck: 29 slides, para abrir no navegador ou hospedar numa URL |
| `Roteiro_Podcast_Dr_Cesar.pdf` | O mesmo deck em PDF 16:9, para mandar ao Dr. Cesar e ao host antes da gravação |
| `FONTES.md` | De onde vem cada número e cada regra citada, e o que ainda falta confirmar |

## Abrir no computador

Dê dois cliques no `index.html`. Funciona offline; só as fontes precisam de internet (sem ela, o navegador usa uma fonte parecida).

| Tecla | Ação |
|---|---|
| `←` `→`, espaço | Navegar |
| `I` ou clique no contador | Índice com todos os slides |
| `T` / `Shift+T` | Cronômetro da gravação: inicia ou pausa / zera (também dá para clicar; duplo clique zera) |
| `F` | Tela cheia |
| `E` | Modo edição: clique num texto e altere |
| `Home` / `End` | Primeiro / último slide |

No celular, deslize para os lados. O endereço termina com `#número` do slide, então dá para mandar o link direto de um bloco (ex.: `.../#19` abre o bloco 08).

**Sobre o modo edição:** o que você altera com `E` fica salvo **só no seu navegador**. Quem abrir a URL hospedada vê o texto original. Para mudar de vez, edite o `index.html` (os textos editáveis têm o atributo `data-edit`) e suba o arquivo de novo. As marcações do checklist também ficam salvas só no navegador.

## Hospedar numa URL

Qualquer hospedagem de site estático serve:

- **Netlify Drop:** arraste a pasta `podcast-dr-cesar` para app.netlify.com/drop. A URL sai na hora.
- **Vercel:** importe o repositório e defina `podcast-dr-cesar` como *Root Directory*.
- **Hostinger, Locaweb e similares:** envie o `index.html` (e o PDF, se quiser o link para download) para uma subpasta do `public_html`, por exemplo `public_html/podcast-dr-cesar/`.

O deck tem `<meta name="robots" content="noindex, nofollow">` porque é um material interno de gravação: o Google não indexa, mas qualquer pessoa com o link abre. Se for divulgar como página pública, tire essa linha.

## Gerar o PDF de novo

Depois de editar o `index.html`: abra no Chrome, `Ctrl+P` (ou `Cmd+P`), destino "Salvar como PDF", margens "Nenhuma" e "Gráficos de plano de fundo" ligado. O deck já vem com o layout de impressão, um slide por página.

## O que o deck acrescentou ao roteiro original

- **Escaleta com tempos** (cerca de 62 min) e links para cada bloco, na ordem recomendada: obesidade como gancho, autoridade logo depois, tirzepatida de volta no bloco 08.
- **Direção de gravação**: retomar o tema na resposta para o corte fazer sentido sozinho, pausa nas frases ★, pensar no vertical, citar remédio pelo princípio ativo.
- **Cold open** com a frase mais forte do bloco 01.
- **Perguntas extras** em cada bloco (barriga x balança, apneia, anabolizantes, recado para os filhos, efeito rebote da caneta etc.).
- **Dado validado**: “mais de 400 mil mortes” confirmado no Cardiômetro da SBC (417.550 em 2024; uma morte a cada 72 segundos em 2026). A pergunta do bloco 03 foi atualizada com o número e a fonte.
- **Base científica da tirzepatida** para o Dr. Cesar consultar: SURMOUNT-1, SUMMIT, SURPASS-CVOT e SURMOUNT-MMO, com “como dizer no ar” e o que evitar.
- **Novos blocos**: bate-bola “Mito ou verdade” (8 frases), “Sinais que não esperam a consulta” (com o SAMU para AVC e o 192) e “Pílulas do público” (8 perguntas para gravar depois, uma por short).
- **16 frases de impacto** (4 novas), **13 cortes com gancho dos 3 primeiros segundos** e **plano de distribuição em 4 semanas**, com a medição por mensagem pronta no WhatsApp.
- **Checklist** antes de gravar e de publicar, incluindo a identificação exigida pela Resolução CFM nº 2.336/2023 (nome, CRM, “médico”, especialidade com RQE).
- A pergunta do bloco 02 foi encurtada para não repetir a lista de instituições que o host já leu na abertura.

## Antes de gravar

Confira o checklist do slide 28 com o Dr. Cesar. Os pontos em aberto estão em `FONTES.md`: tempo de carreira, nomes oficiais das instituições (“Rede América” ou “Rede Américas”?), convênios aceitos, endereço e canal de agendamento, CRM e RQE. No slide 22 há campos `[preencher]` para endereço, convênios e agendamento.
