"""Empacota o HTML autônomo e PNGs finais; não gera nem redesenha ilustrações."""
from pathlib import Path
from PIL import Image
import json, shutil, zipfile, hashlib

root = Path(__file__).resolve().parents[1]
state_path = root/'imagens/ESTADO.json'
state = json.loads(state_path.read_text())
assert len(state) == 104 and all(x['inserida'] and x['conferida'] for x in state.values())
aliases = {57:53,58:56,68:56,72:56,75:56,79:56,83:56,86:53,94:64,95:85,96:69,99:85,103:85}
for n, source in aliases.items():
    state[str(n)]['reutilizada_de'] = f'MX-F{source:03}'
    state[str(n)]['motivo_reutilizacao'] = 'Mesmo conteúdo visual e conexões; contexto da página conferido. Exportação nas dimensões próprias.'
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2)+'\n')

manifest = {}
for x in state.values():
    code=x['codigo']; p=root/'imagens/originais_gpt'/f'{code}.png'
    with Image.open(p) as im: size=list(im.size)
    assert hashlib.sha256(p.read_bytes()).hexdigest()==x['original_sha256']
    manifest[code] = {'origem':x['origem'], 'original':str(p.relative_to(root)), 'original_sha256':x['original_sha256'], 'original_dimensoes':size, 'final':f'imagens/{code}.png', 'final_sha256':x['final_sha256'], 'estado':'imagens/ESTADO.json'}
(root/'imagens/originais_gpt/ORIGEM.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

pages_dir = root/'conferencias/paginas'; pages_dir.mkdir(exist_ok=True)
for page in sorted({x['pagina'] for x in state.values()}):
    src=Path(f'/tmp/ebook-pagina-{page}.png'); assert src.exists(),src
    shutil.copy2(src,pages_dir/f'{page:03}.png')
lines=['# Galeria — GPT Image','', '104 PNGs finais sem numeração de figura dentro das imagens. Clique na imagem ou na página para ampliar no GitHub. Para ler o ebook completo, baixe o ZIP indicado no [README](README.md).','', '| Código | Página do ebook | PNG final | Página montada |','|---|---:|---|---|']
for x in state.values():
    code=x['codigo']; page=x['pagina']
    lines.append(f'| {code} | {page} | [Abrir PNG](imagens/{code}.png) | [Ver página](conferencias/paginas/{page:03}.png) |')
(root/'GALERIA.md').write_text('\n'.join(lines)+'\n')
for name in ['bloco_001_005.png','bloco_001_005_gpt_image.png']:
    shutil.copy2(root/'conferencias/paginas_001_005_1.png',root/'conferencias'/name)

archive=root/'Ebook_Mexico_GPT_Image.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name in ['Ebook_Mexico_inserir_imagens.html','PROGRESSO.md','README.md','GALERIA.md','conferencias/RELATORIO.md','imagens/ESTADO.json']:
        z.write(root/name,name)
    for x in state.values():
        name=f"imagens/{x['codigo']}.png";z.write(root/name,name)
    for p in pages_dir.glob('*.png'):z.write(p,str(p.relative_to(root)))
    assert z.testzip() is None
print('Entrega:', archive.name, round(archive.stat().st_size/1024**2,1),'MiB; HTML autônomo, 104 PNGs e prévias de páginas.')
