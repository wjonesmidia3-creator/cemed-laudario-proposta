# Sites do Grupo Opera

Dois sites estáticos, cada um num único `index.html` (HTML, CSS e JS no mesmo arquivo, sem build e sem dependências além das fontes do Google).

| Pasta | Site | O que tem |
|---|---|---|
| `grupo-opera/` | **Grupo Opera · Aceleradora B2B** | Hero com a tese da bolha, diagnóstico e quatro princípios, pré-diagnóstico interativo (9 perguntas → nota, até 3 sintomas, alavancas e mensagem pronta no WhatsApp; abre em "Empresa B2B"), partitura dos 90 dias, 9 frentes, programas (Aceleração B2B em destaque, Saúde 360, Negócio Local), "Como medimos" (funil até a receita), modelo de relatório mensal, combinados, FAQ |
| `go-influ/` | **GO influ.**, a unidade de influenciadores | Enxuto e focado em escala: o gargalo de conteúdo de 2026 (time da marca x elenco de creators), como creators fazem a marca escalar, como funciona (4 passos + filtro de publi), calculadora "Monte seu elenco" com peças de conteúdo por mês, cadastro de creators via WhatsApp, FAQ |
| `FONTES.md` | Fontes | De onde vem cada número e cada regra citada, com os pontos a confirmar |

**Sem dados de clientes.** Nenhum dos dois sites cita nome, cidade, número ou resultado de cliente. Os números que aparecem são de pesquisas de mercado, com fonte, ou valores de referência do próprio Grupo Opera.

As prévias privadas antigas no claude.ai ([Grupo Opera](https://claude.ai/artifact/Avz8taGi7gpTS4fPugNjqD) · [GO influ.](https://claude.ai/artifact/FACixUukritqeqkfwMu6kM)) ainda mostram a versão anterior, com dados de clientes. Não compartilhe esses links até atualizá-los.

## Antes de publicar

1. **WhatsApp**: abra cada `index.html`, procure `CONFIG` no fim do arquivo e preencha `whatsapp` só com dígitos, com DDI e DDD (ex.: `5517999999999`). Enquanto estiver vazio, os botões abrem o WhatsApp sem destinatário.
2. **Links entre os sites**: em `CONFIG`, `goInfluUrl` (no site do Grupo Opera) e `operaUrl` (no GO influ.) apontam para a pasta vizinha (`../go-influ/`, `../grupo-opera/`). Se cada site tiver domínio próprio, troque pelos endereços finais.
3. **Clientes**: os sites não mostram dados de clientes, por decisão. Se um dia quiser incluir um caso, só com autorização por escrito do cliente.
4. **Filtro de publi**: peça uma revisão jurídica ou do CRO/CRM do "Filtro GO influ." e do resumo de regras do GO influ. Eles já estão marcados como resumo informativo.
5. **Domínio e @**: `grupoopera.com.br` pertence à Feira Ópera e `@grupo.opera` a uma consultoria mexicana. Verifique alternativas no Registro.br e no Instagram. Para a GO influ., verifique `goinflu.com.br` e `@goinflu` e registre a marca mista no INPI (classes 35 e 41).
6. **Rastreamento (opcional)**: cole o Meta Pixel e a tag do Google (GA4/Google Ads) dentro do `<head>` de cada arquivo. Se fizer isso, publique também uma política de privacidade (LGPD) e linke no rodapé.

## Como publicar

Qualquer hospedagem de site estático serve. Três caminhos simples:

- **Netlify Drop**: arraste a pasta `grupo-opera` (ou `go-influ`) para app.netlify.com/drop e depois conecte o domínio.
- **Vercel**: importe o repositório e defina a pasta do site como *Root Directory*.
- **Hostinger, Locaweb e similares**: envie o `index.html` para a pasta `public_html` do domínio.

Para ver localmente: `npx serve sites` e abra `/grupo-opera/` e `/go-influ/`.

## Por que "GO influ."

Três avaliadores independentes compararam 21 nomes (GO Influ, GO Match, GO Publi, Elenco Opera, Coxia, Camarim, Holofote e outros). "GO influ." venceu em dois dos três:

- **GO** são as iniciais do Grupo Opera (o NPS do grupo já usa a marca "GO.") e soa como "bora";
- **influ** é como os próprios creators falam, e o dono de clínica entende na hora;
- passa no teste do WhatsApp: quem ouve uma vez consegue escrever.

Escrita sempre como **GO influ.**, com o GO em negrito e o ponto laranja, para ninguém ler "goin-flu". Dois nomes finalistas viraram partes da marca: **Elenco** é a base de creators ("faça parte do elenco") e **Coxia** é o bastidor ("a gente cuida da coxia"). Se o INPI ou o @ travarem o nome, o plano B é Coxia.
