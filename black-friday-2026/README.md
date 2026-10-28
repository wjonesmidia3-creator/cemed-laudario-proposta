# Roteiros Black Friday 2026 · Odontologia

Roteiros de vídeo para a Black Friday dos cinco clientes de odontologia do Grupo Opera. São cinco roteiros por clínica, montados a partir dos dados de campanhas e conteúdos de agosto a outubro de 2026 (Reportei).

| Cliente | PDF | Foco dos roteiros |
|---|---|---|
| EGO Odontologia | [Roteiros_BlackFriday_2026_EGO.pdf](Roteiros_BlackFriday_2026_EGO.pdf) | Implante, prótese e protocolo; depoimento da Dona Dalva |
| Trait Odontologia (Guarapuava) | [Roteiros_BlackFriday_2026_Trait.pdf](Roteiros_BlackFriday_2026_Trait.pdf) | Protocolo, implantes, bate-bola e vídeo com a equipe |
| D'Placido (Dra. Luciana) | [Roteiros_BlackFriday_2026_DPlacido.pdf](Roteiros_BlackFriday_2026_DPlacido.pdf) | Protocolo, sedação, Invisalign e reativação da base antiga |
| Instituto Sanrire (Brasília) | [Roteiros_BlackFriday_2026_Sanrire.pdf](Roteiros_BlackFriday_2026_Sanrire.pdf) | YouTube (bumper e in-stream): prótese, lentes e facetas, institucional |
| Fiorini Odonto & Estética | [Roteiros_BlackFriday_2026_Fiorini.pdf](Roteiros_BlackFriday_2026_Fiorini.pdf) | Protocolo, sedação consciente, lentes e Invisalign |

Todos os roteiros em texto, para copiar no teleprompter: [ROTEIROS.md](ROTEIROS.md).

## Como a campanha funciona

1. **Aquecimento (09 a 20/11):** Lista VIP. O vídeo pede para mandar BLACK no WhatsApp.
2. **Esquenta (23 a 26/11):** vídeo que tira dúvidas do tratamento principal da clínica.
3. **Black Friday (27/11):** abertura. A condição especial passa a valer.
4. **Última chamada (28 a 30/11):** prazo real até segunda, 30/11.

Antes de gravar, cada clínica precisa definir a condição de Black Friday (para quais tratamentos, qual regra, até quando) **até 05/11**, para a recepção falar a mesma coisa que os vídeos. Gravação até **06/11**.

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
