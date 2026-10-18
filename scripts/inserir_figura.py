"""Incorpora um PNG somente no campo correspondente, preservando os demais bytes."""
from pathlib import Path
from PIL import Image
import base64,re,sys
ROOT=Path(__file__).resolve().parents[1]
code=sys.argv[1]
assert re.fullmatch(r'MX-F\d{3}',code)
path=ROOT/'Ebook_Mexico_inserir_imagens.html'
s=path.read_text();png=ROOT/'imagens'/f'{code}.png'
with Image.open(png) as im:im.verify()
pattern=r'<div class="slot(?: filled)?" id="'+code+r'"[^>]*>.*?</div><img[^>]*>'
m=re.search(pattern,s,re.S)
assert m, f'Campo {code} ausente'
fragment=m.group()
assert not re.search(r'<img[^>]*\bsrc=',fragment), 'Campo já preenchido; revisar antes de substituir'
fragment=fragment.replace('class="slot"','class="slot filled"',1)
fragment=fragment.replace(' tabindex=',f' data-filename="{code}.png" tabindex=',1)
fragment=re.sub(r'(<img\b[^>]*)(>)',lambda m:m[1]+' src="data:image/png;base64,'+base64.b64encode(png.read_bytes()).decode()+'"'+m[2],fragment,count=1)
s=s[:m.start()]+fragment+s[m.end():]
tmp=path.with_suffix('.tmp');tmp.write_text(s);tmp.replace(path)
progress=ROOT/'PROGRESSO.md'
row=f'| {code} | '+{'MX-F001':'4','MX-F002':'9','MX-F003':'10','MX-F004':'10','MX-F005':'12'}[code]+' | sim | sim | sim | não | Sem pendências no bloco. |'
with progress.open('a') as f:f.write(row+'\n')
print(code,'incorporada; progresso salvo')
