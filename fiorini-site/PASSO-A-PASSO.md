# Fiorini: passo a passo dos ajustes na Hostinger

Use junto com `ferramenta-ajustes.html` (baixe e abra com dois cliques no Chrome do PC).
A ferramenta aplica as 5 trocas de `ALTERACOES.md` no arquivo que está no ar hoje, por isso
pixels e códigos que só existem na versão publicada continuam lá. Se algum trecho não estiver
exatamente igual, ela não gera o arquivo e mostra um relatório para mandar ao Claude.

## A. Baixar os arquivos que estão no ar

1. hPanel → Sites → site da Fiorini → Gerenciador de Arquivos → `public_html`.
2. Botão direito em `index.html` → Download (página principal).
3. Pasta `implantes` → botão direito em `index.html` → Download (o Chrome salva como `index (1).html`).
   Se não houver a pasta, baixe `implantes.html` da raiz.

## B. Ajustar na ferramenta

4. Arraste cada arquivo no quadro certo. Todas as linhas precisam ficar verdes.
5. Clique em "Baixar arquivo ajustado" nos dois quadros: saem
   `index-AJUSTADO-principal.html` e `index-AJUSTADO-implantes.html`.
   Se ficar vermelho: "Copiar relatório" e cole na conversa. Não suba nada.

## C. Backup e upload (faça 7 e 8 em seguida)

6. Em `public_html`: Upload → `index-AJUSTADO-principal.html`.
7. Backup: renomeie `index.html` → `index.backup-2026-11.html`.
8. Renomeie `index-AJUSTADO-principal.html` → `index.html`.
9. Na pasta `implantes`, repita 6 a 8 com `index-AJUSTADO-implantes.html`
   (backup `index.backup-2026-11.html`; se for `implantes.html` na raiz, use `implantes.backup-2026-11.html`).

## D. Conferir

10. Abra o site com `?v=2611` no fim do endereço e aperte Ctrl+Shift+R: menu "Alinhador";
    "CRO-SP 589011" embaixo da Dra. Claudia Fiorini; "CRO-SP 76945" embaixo do Dr. James Fiorini.
11. Ctrl+U → Ctrl+F `100 mil` → 0 resultados.
12. Mesmo teste em `/implantes/?v=2611`. A frase "Implante · Protocolo · Reabilitação · Vargem Grande do Sul-SP" continua.
13. Se aparecer a versão antiga, limpe o cache/CDN do site no hPanel.

## Para desfazer

Na pasta da página: renomeie `index.html` → `index-com-erro.html` e `index.backup-2026-11.html` → `index.html`.
