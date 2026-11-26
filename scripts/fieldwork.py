"""Original, GitHub-safe motion cards. CrystalizedBall-inspired optics, no React/WebGL."""
import base64, html, json, math, random, pathlib, xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]; OUT=ROOT/'assets'
BG='#191c20'; FG='#f3f1eb'; DIM='#bcc1c2'; GOLD='#d7bd96'; SAGE='#c9c7bd'; LINE='#414143'
FONT='Arial, Helvetica, sans-serif'; MONO='Consolas, Liberation Mono, monospace'
def e(s):return html.escape(str(s),quote=True)
def t(x,y,s,size,color=FG,weight=400,anchor='start',font=FONT,extra=''):
 return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" font-family="{font}" {extra}>{e(s)}</text>'
def r(x,y,w,h,fill,extra=''):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" {extra}/>'
def c(x,y,rad,fill,extra=''):return f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{fill}" {extra}/>'
def p(d,stroke,w=1,extra=''):return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{w}" {extra}/>'
def write(name,w,h,title,desc,body,css=''):
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{e(title)}</title><desc id="desc">{e(desc)}</desc><style>{css}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>{body}</svg>\n'
 ET.fromstring(svg); (OUT/name).write_text(svg,encoding='utf-8')
def shell(w,h,accent=GOLD):
 return f'<defs><linearGradient id="surface" x2="1" y2="1"><stop stop-color="#24282c"/><stop offset="1" stop-color="#181b1e"/></linearGradient><radialGradient id="ambient"><stop stop-color="{accent}" stop-opacity=".13"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient><linearGradient id="edge"><stop stop-color="{accent}" stop-opacity=".45"/><stop offset="1" stop-color="#777d80" stop-opacity=".12"/></linearGradient><clipPath id="frame"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="13"/></clipPath></defs>'+r(1,1,w-2,h-2,'url(#surface)','rx="13" stroke="url(#edge)"')
CSS='.drift{animation:drift 8s ease-in-out infinite}.orbit{animation:orbit 18s linear infinite;transform-origin:0 0}.twinkle{animation:twinkle 4s ease-in-out infinite}.flow{animation:flow 3s linear infinite}.pulse{animation:pulse 5s ease-in-out infinite}@keyframes drift{50%{transform:translate(0,-5px)}}@keyframes orbit{to{transform:rotate(360deg)}}@keyframes twinkle{50%{opacity:.28}}@keyframes flow{to{stroke-dashoffset:-36}}@keyframes pulse{50%{opacity:.45}}'
def heading(num,name,category,lines,stack):
 b=t(28,33,num+'  /  '+category,12,GOLD,700,font=MONO,extra='letter-spacing="1.2"')
 b+=t(27,83,name,42,FG,700)
 for i,s in enumerate(lines):b+=t(29,117+i*25,s,17,DIM)
 b+=p('M29 182H478',LINE)
 b+=t(29,209,stack,13,SAGE,600,font=MONO)
 return b
def crystal():
 b=shell(960,236)+heading('01','VerifAI','AI VERIFICATION',['Separate claims from supporting evidence.','Independent review with an explicit unknown state.'],'PYTHON / FASTAPI / POSTGRESQL / BM25')
 b+=c(736,113,133,'url(#ambient)')
 b+='<defs><radialGradient id="glass" cx=".34" cy=".27" r=".79"><stop stop-color="#e6dac5" stop-opacity=".25"/><stop offset=".44" stop-color="#797267" stop-opacity=".08"/><stop offset=".88" stop-color="#232322" stop-opacity=".25"/><stop offset="1" stop-color="#e2d1b6" stop-opacity=".57"/></radialGradient><clipPath id="crystal"><circle cx="736" cy="110" r="77"/></clipPath></defs>'
 b+=c(736,110,77,'url(#glass)','stroke="#cfc6b8" stroke-opacity=".72" stroke-width="1.4"')
 rng=random.Random(2717); dust=[]
 for i in range(330):
  ang=rng.random()*math.tau;rad=72*math.sqrt(rng.random());x=736+math.cos(ang)*rad;y=110+math.sin(ang)*rad
  if y<90 and rng.random()<.6:continue
  dust.append(c(round(x,2),round(y,2),round(rng.uniform(.32,1.1),2),rng.choice([SAGE,GOLD,'#fff6df']),f'opacity="{rng.uniform(.15,.75):.2f}"'))
 b+='<g clip-path="url(#crystal)"><g class="drift">'+''.join(dust)+'</g></g>'
 for k in range(4):
  pts=[]
  for i in range(181):
   a=i*math.tau/180;rad=77+1.6*math.sin(a*(11+k)+k)+.7*math.sin(a*31+k*1.7)
   pts.append(f'{math.cos(a)*rad:.2f} {math.sin(a)*rad:.2f}')
  b+=f'<g transform="translate(736 110)"><g class="orbit" style="animation-duration:{18+k*7}s;animation-direction:{"reverse" if k%2 else "normal"}">{p("M"+"L".join(pts)+"Z",SAGE if k%2 else "#f9ead0",.55+k*.13,"opacity=\".55\"")}</g></g>'
 b+=p('M695 48Q719 36 744 40','#fff6df',2,'stroke-linecap="round" opacity=".7"')
 b+=t(736,112,'EVIDENCE',13,FG,700,'middle',MONO)+t(736,132,'REVIEW',10,DIM,500,'middle',MONO)
 b+=t(736,218,'CLAIMS  →  EVIDENCE  →  VERDICT',11,DIM,600,'middle',MONO)
 write('project-verifai.svg',960,236,'VerifAI','AI answer verification using claim extraction, retrieved evidence and independent review. Animated crystal is conceptual.',b,CSS)
def clusters():
 b=shell(960,236,SAGE)+heading('02','Atlox AI','NEWS INTELLIGENCE',['Turn fragmented reporting into related events.','Deduplication, entity extraction and clustering.'],'PYTHON / FASTAPI / NLP / REDIS')
 b+=c(737,111,132,'url(#ambient)')
 rng=random.Random(1207)
 for i,(x,y,col,lab) in enumerate([(649,87,GOLD,'EVENT A'),(803,83,SAGE,'EVENT B'),(746,161,'#d4d4cd','EVENT C')]):
  b+=c(x,y,38,'none',f'stroke="{col}" stroke-opacity=".22"')
  for j in range(42):
   a=rng.random()*math.tau;rad=34*math.sqrt(rng.random());xx=x+rad*math.cos(a);yy=y+rad*math.sin(a)
   b+=c(round(xx,2),round(yy,2),round(rng.uniform(.6,2),2),col,f'opacity="{rng.uniform(.28,.85):.2f}" class="twinkle" style="animation-delay:-{rng.uniform(0,5):.2f}s"')
  b+=c(x,y,6,col,'opacity=".85"')+t(x,y-45,lab,10,col,600,'middle',MONO)
 for i,d in enumerate(['M535 52Q587 42 649 87','M545 116Q588 135 649 87','M537 177Q617 177 746 161','M900 52Q855 40 803 83','M907 153Q855 155 803 83']):
  b+=p(d,'#7b8683',1,'opacity=".45"')+p(d,SAGE,1.6,f'stroke-dasharray="3 33" stroke-linecap="round" class="flow" style="animation-delay:-{i*.6}s"')
 b+=t(736,218,'ILLUSTRATIVE EVENT CLUSTERS',11,DIM,600,'middle',MONO)
 write('project-atlox.svg',960,236,'Atlox AI','Illustrative related news fragments grouped into events. This is not live news traffic.',b,CSS)
def cane():
 data=json.loads((ROOT/'data'/'cane-routing.json').read_text())['counts'];n=sum(data.values())
 b=shell(960,236,GOLD)+heading('03','CANE','CONTEXT-AWARE ROUTING',['Prioritize multimodal messages by context.','Deterministic decisions with explanations.'],'PYTHON / TF-IDF / RAPIDFUZZ / RULES')
 b+=t(528,38,str(n)+' checked-in predictions',16,FG,700)
 b+=t(928,38,'OUTPUT.CSV',10,DIM,600,'end',MONO)
 # Measured results as thin translucent tracks; no giant solid slabs.
 for i,(k,col) in enumerate([('notify',SAGE),('digest',GOLD),('mute','#bfc4c8')]):
  y=72+i*47;val=data[k]
  b+=t(528,y,k.capitalize(),15,DIM,600)+t(928,y,str(val),20,FG,700,'end',MONO)
  b+=r(528,y+9,400,7,'#34393c','rx="3.5"')
  b+=r(528,y+9,round(400*val/n,2),7,col,'rx="3.5" opacity=".75"')
  b+=c(round(528+400*val/n,2),y+12.5,4.5,col,f'class="pulse" style="animation-delay:-{i}s"')
 b+=t(528,218,'DECISION COUNTS, NOT ACCURACY',11,DIM,600,font=MONO)
 write('field-cane.svg',960,236,'CANE',f'{n} checked-in predictions: '+', '.join(f'{k}: {v}' for k,v in data.items())+'. Not accuracy.',b,CSS)
def contacts():
 icons=['M7 17L17 7M8 7H17V16','M5 9V19M5 5V6M10 19V9M10 13Q13 6 18 12V19','M14 4L6 12L14 20M8 12H20','M3 6H21V18H3ZM3 6L12 13L21 6']
 for i,(slug,title,detail) in enumerate([('portfolio','Portfolio','Projects & case studies'),('linkedin','LinkedIn','Professional profile'),('leetcode','LeetCode','Problem solving'),('email','Email','Get in touch')]):
  b=shell(450,91,SAGE)+c(43,45,23,'#353433','stroke="#77716a" stroke-opacity=".45"')
  b+=f'<g transform="translate(31 33)">{p(icons[i],SAGE,1.6,"stroke-linecap=\"round\" stroke-linejoin=\"round\"")}</g>'
  b+=t(79,37,title,22,FG,700)+t(80,61,detail,15,DIM)+p('M417 32L427 42L417 52',GOLD,1.6,'stroke-linecap="round"')
  write('contact-'+slug+'.svg',450,91,title,detail,b)
def skills():
 import foundry
 foundry.OUT=OUT
 foundry.skills()
def actions():
 for slug,label in [('case','Case study'),('app','Application'),('data','Prediction data')]:
  b=r(1,1,182,36,'#22262a','rx="8" stroke="#525b5b"')+t(15,24,label,15,FG,600)+p('M157 13H169V25M169 13L157 25',SAGE,1.4,'stroke-linecap="round"')
  write('action-'+slug+'.svg',184,38,label,label,b)
def build():
 crystal();clusters();cane();contacts();skills();actions()
if __name__=='__main__':build()
