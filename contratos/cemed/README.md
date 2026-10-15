# Contrato Grupo Opera × CEMED

| Arquivo | O que é |
|---|---|
| `Contrato_Grupo_Opera_CEMED.pdf` | Contrato pronto para assinatura eletrônica |
| `contrato.html` | Fonte do contrato. Os dados variáveis ficam no `CONFIG`, no fim do arquivo |
| `gerar-pdf.js` | Gera o PDF a partir do HTML |
| `ASAAS_CEMED.md` | Dados da CEMED para o cadastro e a assinatura no Asaas |

## Base

Condições comerciais iguais às do contrato que a CEMED assinou com a OZ Performance (25/06/2026): Meta Ads e Google Ads com criação de peças, R$ 2.650,00 por mês, 6 meses de permanência mínima com renovação automática, aviso de 30 dias e multa de uma mensalidade na saída antecipada sem justa causa.

O que mudou em relação ao contrato da OZ:

- pagamento por boleto ou Pix do Asaas em nome do CNPJ do Grupo Opera (no anterior era Pix para pessoa física);
- multa de atraso de 2% e juros de 1% ao mês, com suspensão após 10 dias e rescisão após 30 (no anterior, uma mensalidade inteira de multa);
- combinados do Grupo Opera no escopo: gestor dedicado, painel aberto, checagem de publicidade médica (CFM 2.336/2023), resposta no mesmo dia útil, pesquisa semestral;
- cláusulas de publicidade médica, LGPD (CEMED controladora, Grupo Opera operadora), acesso por permissão de parceiro em vez de senha e uso de resultados agregados no portfólio, com opção de recusa;
- correções do modelo anterior: referência "item xx" sem número e foro "Cidade/UF" sem preencher.

## Antes de enviar para assinatura

1. Preencha no `CONFIG` de `contrato.html` os dados do Grupo Opera que ficam em laranja no PDF: razão social, endereço, representante legal e e-mail de notificações.
2. Confirme o foro (Mirassol/SP) e, se quiser data fixa de início ou dia fixo de vencimento, preencha `dataInicio`, `diaVencimento` e `primeiroVencimento`.
3. Gere o PDF de novo:

```bash
NODE_PATH="$(npm root -g)" node contratos/cemed/gerar-pdf.js
```

O script lista no terminal os campos que ainda estão vazios.
