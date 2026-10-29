# Roteiros Black Friday 2026 · Odontologia

Campanhas de Black Friday dos cinco clientes de odontologia do Grupo Opera. Cada clínica recebe uma entrega única, sem datas de publicação: de 5 a 6 filmes, e cada um é a releitura de um anúncio ou conteúdo que já trouxe resultado para ela (dados da Reportei, junho a outubro de 2026).

| Cliente | PDF | Filme principal | Releituras |
|---|---|---|---|
| EGO Odontologia | [Roteiros_BlackFriday_2026_EGO.pdf](Roteiros_BlackFriday_2026_EGO.pdf) | "O que faz falta": a Dona Dalva fala de Black Friday | Dente perdido, prótese, implante, acolhimento |
| Trait Odontologia (Guarapuava) | [Roteiros_BlackFriday_2026_Trait.pdf](Roteiros_BlackFriday_2026_Trait.pdf) | "Fala, Guarapuava": enquete na rua sobre o que cada um vai comprar | Homem do estático, atendimento, implante unitário, depoimentos |
| D'Placido (Dra. Luciana) | [Roteiros_BlackFriday_2026_DPlacido.pdf](Roteiros_BlackFriday_2026_DPlacido.pdf) | "O copo": a prótese no copo enquanto chegam as ofertas | Sedação, depoimentos, alinhador, a história da Dra. |
| Instituto Sanrire (Brasília) | [Roteiros_BlackFriday_2026_Sanrire.pdf](Roteiros_BlackFriday_2026_Sanrire.pdf) | "A pesquisa da Black": gravação de tela com a busca que a pessoa adia | Institucional, canal, lentes, experiência |
| Fiorini Odonto & Estética | [Roteiros_BlackFriday_2026_Fiorini.pdf](Roteiros_BlackFriday_2026_Fiorini.pdf) | "Na mesa": a prótese que quebra no almoço de família | Homem, Vargem Grande, carga imediata, depoimentos, sedação |

Todos os roteiros em texto, para copiar no teleprompter: [ROTEIROS.md](ROTEIROS.md).

## Como a entrega funciona

- **Filme principal com duas opções.** A Opção A tem gente ou cena (paciente, enquete na rua, dramatização ou gravação de tela). A Opção B é gravada só com a Dra. ou o dentista, no consultório, em cerca de uma hora: sem elenco nem locação.
- **Gancho de consumo.** Todos os filmes partem da mesma pergunta: na Black Friday a gente troca a TV, o celular, a air fryer… e o sorriso?
- **Um único chamado.** Todo filme termina pedindo para mandar BLACK no WhatsApp, e a condição especial é apresentada na conversa individual e na avaliação.
- **Sem a marca Invisalign.** Os filmes de alinhador falam em "alinhador transparente", porque marcas costumam ter regras próprias para campanhas com condição especial.

Antes de gravar, cada clínica precisa definir a condição de Black Friday (para quais tratamentos e com qual regra), para a recepção falar a mesma coisa que os vídeos.

## Por que nenhum vídeo fala de preço

O Código de Ética Odontológica proíbe anunciar preço, serviço gratuito e forma de pagamento. A Resolução CFO 271/2025 tirou o desconto em si da lista de infrações, mas campanhas de Black Friday em massa ainda estão em discussão na Justiça (TRF5). Por isso os roteiros falam em "condição especial" e deixam valores, percentuais e formas de pagamento para a conversa individual. Cada PDF traz o checklist completo; o responsável técnico de cada clínica valida antes de publicar.

Referências:
- [Resolução CFO 271/2025](https://sistemas.cfo.org.br/visualizar/atos/RESOLU%C3%87%C3%83O/SEC/2025/271)
- [Nota Técnica nº 14/2025 (CADE e CFO)](https://website.cfo.org.br/wp-content/uploads/2025/03/Nota-Tecnica-no-14-2025-CADE-CFO.pdf)
- [Publicidade odontológica e Black Friday: decisão do TRF5 (Âmbito Jurídico)](https://ambitojuridico.com.br/publicidade-odontologica-e-competencia-regulatoria-os-limites-do-marketing-comercial-em-massa-frente-ao-codigo-de-etica-e-a-livre-concorrencia/)

## Como editar

O conteúdo fica em `_fonte/conteudo.mjs`. Depois de editar, gere os PDFs e o `ROTEIROS.md` de novo:

```bash
cd black-friday-2026/_fonte && node build.mjs
```

Para gerar só um cliente: `node build.mjs EGO` (os nomes são `EGO`, `Trait`, `DPlacido`, `Sanrire` e `Fiorini`). O build avisa se algum texto passar do tamanho da página.
