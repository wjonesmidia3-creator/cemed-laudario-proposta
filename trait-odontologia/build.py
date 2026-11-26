"""Gera Trait_Proposta_Redesign.html: um arquivo único, com as imagens embutidas.
Uso: python3 build.py  (a partir desta pasta)"""
import base64, json, os, re
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'index.html'), encoding='utf-8').read()
keys = sorted(set(re.findall(r'data-k="([^"]+)"', src)))
imgs = {}
for k in keys:
    with open(os.path.join(here, 'img', k + '.webp'), 'rb') as f:
        imgs[k] = 'data:image/webp;base64,' + base64.b64encode(f.read()).decode()
tag = '<script>window.__IMG=' + json.dumps(imgs, separators=(',', ':')) + ';</script>'
out = src.replace('<!--IMG-->', tag, 1)
dst = os.path.join(here, 'Trait_Proposta_Redesign.html')
open(dst, 'w', encoding='utf-8').write(out)
print(len(keys), 'imagens,', round(os.path.getsize(dst) / 1024 / 1024, 2), 'MB ->', dst)
