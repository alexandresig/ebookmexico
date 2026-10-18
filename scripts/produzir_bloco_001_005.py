"""Desenho determinístico em PNG. Não modifica o HTML; montagem é uma etapa separada."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
ROOT=Path(__file__).resolve().parents[1]
INK='#202A34'; NAVY='#123044'; BLUE='#167C9C'; PALE='#EEF5F7'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
class Fig:
 def __init__(self,n,h,title):
  self.n=n;self.im=Image.new('RGB',(2080,h),'white');self.d=ImageDraw.Draw(self.im)
  self.text(90,65,title,44,True);self.line([(90,135),(1990,135)],BLUE,3)
 def text(self,x,y,s,size=38,bold=False,anchor='lt',color=INK):
  f=ImageFont.truetype(BOLD if bold else FONT,size)
  box=self.d.textbbox((x,y),s,font=f,anchor=anchor)
  assert box[0]>=0 and box[2]<=2080 and box[1]>=0 and box[3]<=self.im.height,(self.n,s,box)
  self.d.text((x,y),s,font=f,fill=NAVY if bold else color,anchor=anchor)
 def line(self,pts,c=INK,w=6):self.d.line(pts,fill=c,width=w,joint='curve')
 def rect(self,box,fill='white',c=INK,w=4):self.d.rectangle(box,fill=fill,outline=c,width=w)
 def circle(self,x,y,r=8,fill=INK):self.d.ellipse((x-r,y-r,x+r,y+r),fill=fill)
 def arrow(self,a,b,c=BLUE,w=6):
  self.line([a,b],c,w);ang=math.atan2(b[1]-a[1],b[0]-a[0]);L=20
  self.d.polygon([b,(b[0]-L*math.cos(ang-.5),b[1]-L*math.sin(ang-.5)),(b[0]-L*math.cos(ang+.5),b[1]-L*math.sin(ang+.5))],fill=c)
 def save(self):
  (ROOT/'imagens').mkdir(exist_ok=True);self.im.save(ROOT/'imagens'/f'MX-F{self.n:03}.png')
 def lamp(self,x,y,r=43):
  self.d.ellipse((x-r,y-r,x+r,y+r),outline=INK,width=6)
  a=int(r*.7);self.line([(x-a,y-a),(x+a,y+a)],w=5);self.line([(x-a,y+a),(x+a,y-a)],w=5)
 def contact(self,x,y,nc=False):
  self.line([(x-22,y-27),(x-22,y+27)]);self.line([(x+22,y-27),(x+22,y+27)])
  if nc:self.line([(x-38,y+38),(x+38,y-38)],w=5)
 def box(self,x,y,w,h,title,subtitle,size=38):
  self.rect((x,y,x+w,y+h),PALE,BLUE,3)
  self.text(x+w/2,y+26,title,size,True,'mt');self.text(x+w/2,y+89,subtitle,38,False,'mt')

def f1():
 f=Fig(1,896,'FIGURA 1 · DOS FUNCIONES DIFERENTES')
 f.text(550,183,'DISTRIBUCIÓN RESIDENCIAL',42,True,'mt');f.text(1550,183,'CONTROL INDUSTRIAL',42,True,'mt')
 f.box(110,285,860,145,'TABLERO DE DISTRIBUCIÓN','Distribuye y protege circuitos',38)
 f.box(1110,285,860,145,'TABLERO DE CONTROL','Protección, maniobra y lógica',38)
 f.arrow((340,430),(340,558));f.arrow((750,430),(750,558));f.arrow((1540,430),(1540,558))
 f.lamp(340,620);f.text(340,692,'LUCES',40,True,'mt');f.text(340,750,'Iluminación',38,anchor='mt')
 f.rect((705,582,795,659));f.line([(730,602),(730,627)]);f.line([(770,602),(770,627)])
 f.text(750,692,'CONTACTOS',40,True,'mt');f.text(750,750,'Tomacorrientes',38,anchor='mt')
 f.d.ellipse((1495,575,1585,665),outline=INK,width=5);f.text(1540,594,'M',42,True,'mt')
 f.text(1540,692,'MOTOR / BOMBA',40,True,'mt');f.text(1540,750,'Arranque y paro',38,anchor='mt')
 f.text(1040,828,'Vista funcional · las flechas expresan funciones, no cableado.',38,anchor='mt');f.save()

def f2():
 f=Fig(2,796,'FIGURA 2 · ANALOGÍA HIDRÁULICA')
 f.text(380,186,'DEPÓSITO',42,True,'mt')
 f.rect((150,270,620,535),PALE);f.rect((156,362,614,530),'#D9EDF3',c='#D9EDF3',w=1)
 f.line([(150,270),(150,535),(620,535),(620,270)])
 f.line([(620,470),(1850,470)],BLUE,20)
 # Restricción regulable sobre la tubería: dos triángulos opuestos y vástago.
 f.d.polygon([(1170,423),(1240,470),(1170,517)],fill='white',outline=INK,width=5)
 f.d.polygon([(1310,423),(1240,470),(1310,517)],fill='white',outline=INK,width=5)
 f.line([(1240,470),(1240,360)]);f.line([(1195,360),(1285,360)])
 f.text(1250,238,'RESTRICCIÓN ↔ RESISTENCIA (Ω)',38,True,'mt')
 f.line([(1240,292),(1240,332)],BLUE,3)
 f.text(110,587,'PRESIÓN ↔ TENSIÓN (V)',38,True)
 f.line([(360,565),(360,495)],BLUE,3)
 f.arrow((1510,560),(1840,560));f.text(1510,597,'CAUDAL ↔',38,True,'mt');f.text(1690,650,'CORRIENTE (A)',38,True,'mt')
 f.text(1040,724,'Modelo intuitivo de un circuito resistivo; no representa un motor.',38,anchor='mt');f.save()

def f3():
 f=Fig(3,700,'FIGURA 3 · SERIE Y PARALELO')
 f.text(530,183,'SERIE',42,True,'mt');f.text(1550,183,'PARALELO',42,True,'mt')
 # Dos terminales de alimentación; único trayecto H1 -> H2.
 f.text(130,318,'+',46,True,'mt');f.text(130,498,'−',46,True,'mt')
 f.line([(185,345),(387,345)]);f.lamp(430,345);f.line([(473,345),(677,345)]);f.lamp(720,345)
 f.line([(763,345),(925,345),(925,525),(185,525)])
 f.text(430,260,'H1',38,True,'mt');f.text(720,260,'H2',38,True,'mt')
 # Buses horizontales +/−, dos ramas con lámparas.
 f.text(1130,268,'+',46,True,'mt');f.text(1130,498,'−',46,True,'mt')
 f.line([(1180,295),(1920,295)]);f.line([(1180,525),(1920,525)])
 for x,label in [(1400,'H1'),(1800,'H2')]:
  f.line([(x,295),(x,367)]);f.lamp(x,410);f.line([(x,453),(x,525)]);f.circle(x,295);f.circle(x,525);f.text(x+72,390,label,38,True)
 f.text(530,605,'Un solo recorrido',40,anchor='mt');f.text(1550,605,'Dos ramas independientes',40,anchor='mt');f.save()

def f4():
 f=Fig(4,725,'FIGURA 4 · LÓGICA DE RETENCIÓN · 24 V C.C.')
 y=320
 f.text(105,236,'+24 V',40,True)
 # Serie obligatoria S0 NC y FR1 NC antes de la bifurcación.
 f.line([(110,y),(348,y)]);f.contact(370,y,True);f.line([(392,y),(658,y)]);f.contact(680,y,True);f.line([(702,y),(900,y)])
 f.text(370,208,'S0 · PARO',38,True,'mt');f.text(370,380,'NC',38,anchor='mt');f.text(680,208,'FR1 · NC',38,True,'mt')
 # S1 y auxiliar KM1 en paralelo solo entre estos dos nodos.
 f.circle(900,y);f.circle(1450,y)
 f.line([(900,y),(1158,y)]);f.contact(1180,y);f.line([(1202,y),(1580,y)])
 f.line([(900,y),(900,500),(1158,500)]);f.contact(1180,500);f.line([(1202,500),(1450,500),(1450,y)])
 f.text(1180,208,'S1 · ARRANQUE',38,True,'mt');f.text(1180,377,'NA',38,anchor='mt')
 f.text(1180,555,'KM1 · 13-14 (NA)',38,True,'mt')
 f.rect((1580,275,1760,365));f.text(1670,297,'KM1',38,True,'mt')
 f.line([(1760,y),(1950,y)]);f.text(1557,215,'A1',38,anchor='mt');f.text(1785,215,'A2',38,anchor='mt');f.text(1900,380,'0 V',40,True,'mt')
 f.text(1040,639,'Contactos sin accionar · bobina desenergizada · control didáctico',38,anchor='mt');f.save()

def f5():
 f=Fig(5,1504,'FIGURA 5 · POTENCIA Y CONTROL EN EL MISMO SISTEMA')
 f.text(555,200,'POTENCIA',44,True,'mt');f.text(1545,200,'CONTROL',44,True,'mt')
 left=[('ALIMENTACIÓN','Ej.: 220 V entre fases'),('DESCONEXIÓN Y PROTECCIÓN','Selección según la aplicación'),('CONTACTOS DE KM1','Conmutan la potencia'),('SOBRECARGA + MOTOR','Protección y carga')]
 right=[('FUENTE DE CONTROL','Ej.: 24 V c.c.'),('PARO Y PERMISIVOS','Interrumpen la orden'),('ARRANQUE / RETENCIÓN','Mantienen la orden'),('BOBINA KM1','Acciona los contactos')]
 for x,items in [(100,left),(1090,right)]:
  for i,(title,sub) in enumerate(items):
   y=295+235*i;f.box(x,y,890,155,title,sub,38)
   if i<3:f.arrow((x+445,y+155),(x+445,y+222))
 # Relación funcional discontinua independiente de las flechas de flujo.
 # La explicación explicita la asociación sin crear una conexión eléctrica.
 f.text(1040,1255,'KM1 identifica la misma bobina',40,True,'mt')
 f.text(1040,1310,'y sus contactos asociados.',40,True,'mt')
 f.text(1040,1390,'Vista funcional · flechas conceptuales, no conexiones eléctricas.',38,anchor='mt');f.save()

if __name__=='__main__':
 for fn in (f1,f2,f3,f4,f5):fn()
