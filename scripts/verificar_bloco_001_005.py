from pathlib import Path
from lxml import html
from PIL import Image
from playwright.sync_api import sync_playwright
import zipfile,base64,re
root=Path(__file__).resolve().parents[1];p=root/'Ebook_Mexico_inserir_imagens.html'
with zipfile.ZipFile(root/'Ebook_Codex_corrigido.zip') as z:original=z.read(p.name).decode()
s=p.read_text();a=html.fromstring(original);b=html.fromstring(s)
assert len(b.xpath('//*[@class="page"]'))==160
assert a.xpath('//img[@class="base"]/@src')==b.xpath('//img[@class="base"]/@src')
assert a.xpath('//script/text()')==b.xpath('//script/text()')
assert a.xpath('//style/text()')==b.xpath('//style/text()')
pattern=r'<div class="slot(?: filled)?" id="MX-F00[1-5]"[^>]*>.*?</div><img[^>]*>'
assert re.sub(pattern,'FIELD',original,flags=re.S)==re.sub(pattern,'FIELD',s,flags=re.S)
sizes=[(2080,896),(2080,796),(2080,700),(2080,725),(2080,1504)]
for n,size in enumerate(sizes,1):
 code=f'MX-F{n:03}';e=b.get_element_by_id(code);src=e.xpath('./img/@src')[0]
 assert base64.b64decode(src.split(',')[1])==(root/'imagens'/f'{code}.png').read_bytes()
 with Image.open(root/'imagens'/f'{code}.png') as im:assert im.size==size and im.mode=='RGB'
print('PASS estrutural: 160 páginas, bases/scripts/CSS intactos, bytes externos aos cinco campos intactos, PNGs idênticos e dimensões corretas.')
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1300,'height':1600},accept_downloads=True);errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8765/'+p.name,wait_until='load')
 assert page.locator('.page').count()==160 and page.locator('.slot').count()==104
 assert page.locator('.slot.filled').count()==5
 assert page.locator('#counter').inner_text()=='5 de 104 imagens inseridas'
 for n,size in enumerate(sizes,1):
  im=page.locator(f'#MX-F{n:03} > img');assert im.evaluate('(e)=>[e.naturalWidth,e.naturalHeight]')==list(size)
 # Capturas das quatro páginas alteradas, sem barra flutuante sobreposta.
 page.add_style_tag(content='.toolbar{visibility:hidden!important}')
 for n in [4,9,10,12]:page.locator('.page').nth(n-1).screenshot(path=f'/tmp/montada-{n}.png')
 # Referências, substituição, importação em lote, salvamento e gancho de impressão.
 page.locator('#MX-F001').hover();page.locator('#MX-F001 [data-action="reference"]').click()
 assert page.locator('#reference').evaluate('(e)=>e.open')
 assert 'MX-F001' in page.locator('#refTitle').inner_text();page.locator('#closeRef').click()
 page.locator('#MX-F001').click()
 page.locator('#oneFile').set_input_files(str(root/'imagens/MX-F001.png'))
 page.wait_for_function("document.getElementById('MX-F001').dataset.filename==='MX-F001.png'")
 page.locator('#manyFiles').set_input_files([str(root/'imagens'/f'MX-F{n:03}.png') for n in range(1,6)])
 page.wait_for_function("document.querySelector('.toast').textContent.includes('5 imagens inseridas')")
 page.evaluate("window.print=()=>{window.__printCalled=true};document.getElementById('print').click()")
 assert page.evaluate('window.__printCalled')
 with page.expect_download() as d:page.evaluate("document.getElementById('save').click()")
 d.value.save_as('/tmp/ebook-bloco-salvamento.html')
 saved=html.parse('/tmp/ebook-bloco-salvamento.html')
 assert len(saved.xpath('//*[contains(concat(" ",@class," ")," filled ")]'))==5
 assert not errors,errors
 browser.close()
print('PASS navegador: 5/104 imagens carregadas; referências, substituição, lote, download e acionamento da impressão; sem erros JavaScript. PDF não gerado.')
c=Image.new('RGB',(2000,710),'white')
for j,n in enumerate([4,9,10,12]):
 im=Image.open(f'/tmp/montada-{n}.png');im.thumbnail((500,710));c.paste(im,(j*500,0))
c.save('/tmp/paginas-montadas.png')
