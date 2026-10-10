# Sites do Grupo Opera

Dois sites estáticos, cada um num único `index.html` (HTML, CSS e JS no mesmo arquivo, sem build e sem dependências além das fontes do Google).

| Pasta | Site | O que tem |
|---|---|---|
| `grupo-opera/` | **Grupo Opera**, a agência | Diagnóstico, pré-diagnóstico interativo (9 perguntas → nota, 3 sintomas, alavancas e mensagem pronta no WhatsApp), partitura dos 90 dias, 9 frentes, programas (Saúde 360, Negócio Local, Aceleração B2B), resultados com fonte e período, exemplo de update mensal, combinados, FAQ |
| `go-influ/` | **GO influ.**, a unidade de influenciadores | Tese e pirâmide de verba, como funciona (6 passos), formatos, calculadora "Monte seu elenco", regras de publi (CONAR, CFM, CFO, LGPD) com filtro, medição em conversas, cadastro de creators via WhatsApp, FAQ |
| `FONTES.md` | Fontes | De onde vem cada número e cada regra citada, com os pontos a confirmar |

## Antes de publicar

1. **WhatsApp**: abra cada `index.html`, procure `CONFIG` no fim do arquivo e preencha `whatsapp` só com dígitos, com DDI e DDD (ex.: `5517999999999`). Enquanto estiver vazio, os botões abrem o WhatsApp sem destinatário.
2. **Links entre os sites**: em `CONFIG`, `goInfluUrl` (no site do Grupo Opera) e `operaUrl` (no GO influ.) apontam para a pasta vizinha (`../go-influ/`, `../grupo-opera/`). Se cada site tiver domínio próprio, troque pelos endereços finais.
3. **Clientes**: confirme com cada cliente o uso do nome e dos números, e desde quando o Grupo Opera opera cada conta (os comparativos "antes/depois" dependem disso). Detalhes em `FONTES.md`.
4. **Regras de publi**: peça uma revisão jurídica ou do CRO/CRM da seção "Regras de publi" do GO influ. Ela já está marcada como resumo informativo.
5. **Domínio e @**: `grupoopera.com.br` pertence à Feira Ópera e `@grupo.opera` a uma consultoria mexicana. Verifique alternativas no Registro.br e no Instagram. Para a GO influ., verifique `goinflu.com.br` e `@goinflu` e registre a marca mista no INPI (classes 35 e 41).
6. **Rastreamento (opcional)**: cole o Meta Pixel e a tag do Google (GA4/Google Ads) dentro do `<head>` de cada arquivo.

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
