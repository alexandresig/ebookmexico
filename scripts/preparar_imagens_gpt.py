"""Somente resolução, margens e incorporação. A arte vem de GPT Image.

Não redesenha componentes, textos ou fios. Originais gerados ficam preservados.
Não executar produzir_bloco_001_005.py para a versão atual (é a versão antiga).
"""
from pathlib import Path
from PIL import Image,ImageOps
import base64,re
root=Path(__file__).resolve().parents[1]
path=root/'Ebook_Mexico_inserir_imagens.html'
sizes=[(2080,896),(2080,796),(2080,700),(2080,725),(2080,1504)]
for n,(w,h) in enumerate(sizes,1):
 code=f'MX-F{n:03}'
 source=root/'imagens/originais_gpt'/f'{code}.png'
 # Ajuste uniforme, sem deformação ou corte; margens brancas adicionais.
 with Image.open(source) as im:
  content=ImageOps.contain(im.convert('RGB'),(w-100,h-60),Image.Resampling.LANCZOS)
  out=Image.new('RGB',(w,h),'white');out.paste(content,((w-content.width)//2,(h-content.height)//2))
  target=root/'imagens'/f'{code}.png';out.save(target)
 s=path.read_text()
 pattern=r'(<div class="slot filled" id="'+code+r'"[^>]*>.*?</div><img[^>]*\bsrc=")([^"]*)(")'
 s,count=re.subn(pattern,lambda m:m[1]+'data:image/png;base64,'+base64.b64encode(target.read_bytes()).decode()+m[3],s,count=1,flags=re.S)
 assert count==1,code
 tmp=path.with_suffix('.tmp');tmp.write_text(s);tmp.replace(path)
 progress=root/'PROGRESSO.md'
 with progress.open('a') as f:f.write(f'| {code} | '+['4','9','10','10','12'][n-1]+' | GPT Image | sim | sim | sim | não |\n')
 print(code,'arte GPT preservada; dimensões',w,h,'incorporada e progresso salvo')
