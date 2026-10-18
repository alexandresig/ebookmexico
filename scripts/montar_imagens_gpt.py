"""Incorpora imagens já geradas e revisadas; não desenha seu conteúdo.
Uso: python scripts/montar_imagens_gpt.py /tmp/selecionadas.json
JSON: {"6": "/workspace/generated_images/....png"}. Cada entrada é revisão aprovada.
"""
from pathlib import Path
from PIL import Image,ImageOps
from lxml import html
import json,re,base64,sys,shutil,hashlib
ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/'Ebook_Mexico_inserir_imagens.html'
STATE=ROOT/'imagens/ESTADO.json'
state=json.loads((STATE if STATE.exists() else Path('/tmp/ebook-especificacoes.json')).read_text())

def progresso():
 total=sum(bool(x['inserida']) for x in state.values());blocked=[x for x in state.values() if x['bloqueada']]
 nexts=[x['codigo'] for x in state.values() if not x['inserida'] and not x['bloqueada']]
 lines=['# Progresso do ebook — GPT Image','',f'**{total}/104 imagens inseridas.** Próxima pendente: '+(nexts[0] if nexts else 'nenhuma')+'.','',
 'Orientação vigente: GPT Image, sem título geral ou numeração de figura dentro das imagens. Rótulos funcionais e notas didáticas preservados. PNGs finais em `imagens/`; gerações originais em `imagens/originais_gpt/`.','',
 'As versões anteriores permanecem no histórico Git (`9d45c02`: desenhos por código; `15ddd93`: primeiro bloco GPT com títulos). Não executar os scripts antigos de produção para sobrescrever esta versão.','',
 'O processamento local somente exporta PNG no tamanho do prompt, ajusta margens e paleta de cores para conter o tamanho do HTML; não desenha textos, equipamentos ou fios. Originais GPT sem esse processamento preservados.','',
 'Fonte: Ebook_Codex_corrigido.zip; ZIP antigo corrompido ignorado. Cada inserção preserva todos os bytes fora de seu campo. Conferência visual didática; sem certificação de instalação, simulação elétrica ou ensaio de hardware.','',
 '| Código | Página | Criada | Conferida | Inserida | Bloqueada | Pendência |','|---|---:|---|---|---|---|---|']
 for k,x in state.items():
  yes=lambda key:'sim' if x[key] else 'não'
  lines.append(f"| {x['codigo']} | {x['pagina']} | {yes('criada')} | {yes('conferida')} | {yes('inserida')} | {yes('bloqueada')} | {x.get('pendencia','')} |")
 lines+=['','Detalhes da origem, hashes e conferências em `imagens/ESTADO.json`. As páginas e os controles serão verificados no Chromium a cada bloco; ver `conferencias/`.']
 (ROOT/'PROGRESSO.md').write_text('\n'.join(lines)+'\n')

for key,source in json.loads(Path(sys.argv[1]).read_text()).items():
 x=state[key];code=x['codigo'];original=ROOT/'imagens/originais_gpt'/f'{code}.png';original.parent.mkdir(parents=True,exist_ok=True)
 if Path(source).resolve()!=original.resolve():shutil.copy2(source,original)
 w,h=x['dimensoes']
 with Image.open(original) as im:
  fitted=ImageOps.contain(im.convert('RGB'),(w-100,h-60),Image.Resampling.LANCZOS)
  out=Image.new('RGB',(w,h),'white');out.paste(fitted,((w-fitted.width)//2,(h-fitted.height)//2))
  # Paleta de exportação; imagem original íntegra permanece acima.
  out=out.quantize(colors=256,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
  dest=ROOT/'imagens'/f'{code}.png';out.save(dest,optimize=True)
 s=HTML.read_text();pattern=r'<div class="slot(?: filled)?" id="'+code+r'"[^>]*>.*?</div><img[^>]*>'
 m=re.search(pattern,s,re.S);assert m,code
 frag=m.group();frag=frag.replace('class="slot"','class="slot filled"',1)
 if 'data-filename=' not in frag:frag=frag.replace(' tabindex=',f' data-filename="{code}.png" tabindex=',1)
 frag=re.sub(r'\s+src="[^"]*"','',frag)
 data=base64.b64encode(dest.read_bytes()).decode()
 frag=re.sub(r'(<img\b[^>]*)(>)',lambda m:m[1]+' src="data:image/png;base64,'+data+'"'+m[2],frag,count=1)
 temp=HTML.with_suffix('.tmp');temp.write_text(s[:m.start()]+frag+s[m.end():]);temp.replace(HTML)
 x.update(criada=True,conferida=True,inserida=True,bloqueada=False,sem_titulo=True,origem='GPT Image via image_gen',original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),final_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),pendencia='')
 STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');progresso()
 print(code,'salva; HTML',round(HTML.stat().st_size/1024**2,2),'MiB',flush=True)
