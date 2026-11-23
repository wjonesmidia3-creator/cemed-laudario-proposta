# Fiorini Odonto & Estética: ajustes para subir na Hostinger

Arquivos prontos, já com os ajustes:

- `index.html`: página principal (vai na raiz do `public_html`)
- `implantes/index.html`: página de Implantes (vai em `/implantes`)

Atenção: se a versão que está na Hostinger tiver algo que não está aqui (por exemplo, os códigos do pixel do Meta ou do Google Ads), trocar o arquivo inteiro apaga isso. O mais seguro é fazer as trocas abaixo direto no editor do Gerenciador de Arquivos da Hostinger e fazer backup antes.

## Trocas na página principal (`index.html`)

| # | Procurar (exato) | Trocar por |
|---|---|---|
| 1 | `<a href="#invisalign">Invisalign</a>` | `<a href="#invisalign">Alinhador</a>` |
| 2 | `<span>Ortodontia · Harmonização · Invisalign Doctor</span>` | `<span>CRO-SP 589011</span>` |
| 3 | `<span>Implante · Protocolo · Reabilitação</span>` | `<span>CRO-SP 76945</span>` |
| 4 | `<div class="stat-div"></div><div class="stat-big"><b>+ 100 mil</b><span>vidas transformadas</span></div>` | *(apagar)* |
| 5 | ` · + de 100 mil vidas transformadas` (aparece 2 vezes) | *(apagar)* |

## Trocas na página de Implantes

Só os itens 4 e 5. A frase "Implante · Protocolo · Reabilitação · Vargem Grande do Sul-SP" fica, porque descreve a clínica, não um médico.

## Conferência depois de subir

- O menu de cima mostra "Alinhador" no lugar de "Invisalign".
- Embaixo de "Dra. Claudia Fiorini" aparece "CRO-SP 589011", e embaixo de "Dr. James Fiorini" aparece "CRO-SP 76945".
- Não sobrou nenhum "100 mil" em nenhuma das duas páginas.
