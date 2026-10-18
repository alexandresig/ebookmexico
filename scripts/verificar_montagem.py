from pathlib import Path
from lxml import html
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
import re,zipfile,json,base64,sys
root=Path(__file__).resolve().parents[1];state=json.loads((root/'imagens/ESTADO.json').read_text());s=(root/'Ebook_Mexico_inserir_imagens.html').read_text()
with zipfile.ZipFile(root/'Ebook_Codex_corrigido.zip') as z:original=z.read('Ebook_Mexico_inserir_imagens.html').decode()
pattern=r'<div class="slot(?: filled)?" id="MX-F\d{3}"[^>]*>.*?</div><img[^>]*>'
assert len(re.findall(pattern,s,re.S))==104
assert re.sub(pattern,'SLOT',s,flags=re.S)==re.sub(pattern,'SLOT',original,flags=re.S),'Mudança fora dos campos'
r=html.fromstring(s);assert len(r.xpath('//*[@class="page"]'))==160
active=[x for x in state.values() if x['inserida']]
for x in active:
 p=root/'imagens'/f"{x['codigo']}.png";src=r.get_element_by_id(x['codigo']).xpath('./img/@src')[0]
 assert base64.b64decode(src.split(',')[1])==p.read_bytes()
 with Image.open(p) as im:assert list(im.size)==x['dimensoes'];im.verify()
print(f'PASS estrutural: {len(active)}/104 inseridas; 160 páginas; bytes fora dos campos preservados.',flush=True)
start=int(sys.argv[1]) if len(sys.argv)>1 else 1;end=int(sys.argv[2]) if len(sys.argv)>2 else len(active)
selected=[x for x in active if start<=int(x['codigo'][-3:])<=end];pages=sorted(set(x['pagina'] for x in selected));screens=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1300,'height':1650},accept_downloads=True);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8765/Ebook_Mexico_inserir_imagens.html',wait_until='load')
 assert page.locator('.page').count()==160 and page.locator('.slot').count()==104
 assert page.locator('.slot.filled').count()==len(active)
 assert page.locator('#counter').inner_text()==f'{len(active)} de 104 imagens inseridas'
 for x in active:assert page.locator('#'+x['codigo']+' > img').evaluate('(e)=>[e.naturalWidth,e.naturalHeight]')==x['dimensoes']
 page.add_style_tag(content='.toolbar{visibility:hidden!important}')
 for n in pages:
  dest=f'/tmp/ebook-pagina-{n}.png';page.locator('.page').nth(n-1).screenshot(path=dest);screens.append(dest)
 first=selected[0]['codigo']
 page.locator('#'+first).hover();page.locator('#'+first+' [data-action="reference"]').click();assert page.locator('#reference').evaluate('(e)=>e.open');page.locator('#closeRef').click()
 page.evaluate("window.print=()=>{window.__printCalled=true};document.getElementById('print').click()")
 assert page.evaluate('window.__printCalled')
 assert not errors,errors
 b.close()
for offset in range(0,len(screens),5):
 chunk=screens[offset:offset+5];canvas=Image.new('RGB',(500*len(chunk),710),'white')
 for j,p in enumerate(chunk):
  im=Image.open(p);im.thumbnail((500,710));canvas.paste(im,(j*500,0))
 dst=root/'conferencias'/f'paginas_{start:03}_{end:03}_{offset//5+1}.png';canvas.save(dst);print('CAPTURA',dst,flush=True)
print('PASS navegador: imagens carregadas, contador, referências, impressão e ausência de erros JS. PDF não gerado.',flush=True)
