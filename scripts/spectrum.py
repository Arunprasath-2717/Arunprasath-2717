"""AP/2717 original chromatic visual system. No borrowed artwork or runtime JS."""
import html, json, math, pathlib, xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'
INK='#17191d'; WHITE='#fff5e8'; DIM='#c6c5c2'; CORAL='#ff987d'; CITRUS='#ffe291'; MINT='#a5e7d0'; PEACH='#ffc3a2'
SANS='Arial, Helvetica, sans-serif'; MONO='Consolas, Liberation Mono, monospace'
def esc(s):return html.escape(str(s),quote=True)
def t(x,y,s,size,fill=WHITE,weight=400,anchor='start',font=SANS,extra=''):
 return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'
def r(x,y,w,h,fill,extra=''):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" {extra}/>'
def c(x,y,rad,fill,extra=''):return f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{fill}" {extra}/>'
def p(d,stroke,w=1,extra=''):return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{w}" {extra}/>'
def polygon(points,fill,extra=''):return '<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+'" fill="'+fill+'" '+extra+'/>'
def svg(name,w,h,title,desc,b,css=''):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc><style>{css}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>{b}</svg>\n'
 ET.fromstring(s);(OUT/name).write_text(s,encoding='utf-8')
def surface(w,h,accent=CORAL):
 return f'''<defs><linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#27272b"/><stop offset=".62" stop-color="#1b1d21"/><stop offset="1" stop-color="#17191d"/></linearGradient><radialGradient id="wash"><stop stop-color="{accent}" stop-opacity=".20"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient><clipPath id="panel"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="15"/></clipPath></defs><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="15" fill="url(#paper)" stroke="{accent}" stroke-opacity=".28"/><g clip-path="url(#panel)"><ellipse cx="{w*.82}" cy="{h*.24}" rx="{w*.38}" ry="{h*.8}" fill="url(#wash)"/></g>'''
def blend(a,b,u):
 a=tuple(int(a[k:k+2],16) for k in (1,3,5));b=tuple(int(b[k:k+2],16) for k in (1,3,5))
 return '#'+''.join(f'{max(0,min(255,round(x+(y-x)*u))):02x}' for x,y in zip(a,b))
def heading(num,name,tag,desc,stack,accent):
 b=t(27,32,num+' / '+tag,12,accent,700,font=MONO,extra='letter-spacing="1.3"')
 b+=t(25,79,name,40,WHITE,700)
 for i,s in enumerate(desc):b+=t(27,112+i*24,s,16,DIM)
 b+=t(27,214,stack,12,accent,600,font=MONO)
 return b
def verifai():
 b=surface(960,240,CORAL)+heading('01','VerifAI','EVIDENCE & RETRIEVAL',['Compare AI answers against checkable sources.','Keep uncertainty when evidence is insufficient.'],'PYTHON · FASTAPI · POSTGRESQL · BM25',CORAL)
 b+=t(27,177,'Independent review · local BM25 fallback',13,CORAL,500)
 # Compact editorial evidence specimen. Animated highlight stays over exact words.
 b+=r(522,22,410,184,'#f4e8d8','rx="10"')
 b+=t(538,44,'EVIDENCE REVIEW / EXAMPLE',10,'#775749',700,font=MONO)
 b+=t(538,67,'CLAIM',10,'#765b50',700,font=MONO)
 b+=t(538,88,'“Library closed Sunday.”',19,'#362d29',700)
 b+=p('M538 99H916','#cdb5a1')
 b+=t(538,119,'RETRIEVED SOURCE',10,'#765b50',700,font=MONO)
 b+=r(537,126,202,25,'#ffd08b','rx="3" opacity=".7" class="mark"')
 b+=t(538,145,'Sunday: 10:00–16:00',18,'#362d29',600)
 b+=p('M538 155H916','#cdb5a1')
 b+=t(538,180,'VERDICT',10,'#765b50',700,font=MONO)+t(916,182,'Dispute',21,'#9c4233',750,'end',extra='class="verdict"')
 b+=c(902,44,4,'#b35340','class="mark"')
 b+=t(932,223,'ILLUSTRATIVE CASE · NOT LIVE TRAFFIC',10,DIM,400,'end',MONO)
 svg('spectrum-verifai.svg',960,240,'VerifAI','AI verification, example claim conflicts with Sunday opening hours. Evidence is highlighted; not a real evaluation result.',b,'.mark{animation:mark 5s ease-in-out infinite}.verdict{animation:verdict 5s ease-in-out infinite}@keyframes mark{0%,15%,100%{opacity:.25}40%,75%{opacity:1}}@keyframes verdict{0%,35%,100%{opacity:.58}55%,85%{opacity:1}}')
def atlox():
 b=surface(960,240,MINT)+heading('02','Atlox AI','NEWS INTELLIGENCE',['Merge related news coverage into events.','Deduplication, NLP and density-based clustering.'],'PYTHON · FASTAPI · REDIS · NLP',MINT)
 b+=t(27,177,'Redis processing · local in-memory fallback',13,MINT,500)
 # Two separate newspaper fragments converge on a single event, not a fake UI.
 for i,(x,y,head,sub) in enumerate([(526,27,'Rail line opens','REPORT A'),(552,103,'First trains run','REPORT B')]):
  b+=f'<g class="sheet s{i}">'+r(x,y,199,71,'#dbe7dc','rx="6" stroke="#afc1b3"')+t(x+13,y+20,sub,10,'#52695f',700,font=MONO)+t(x+13,y+46,head,18,'#253c32',700)+r(x+13,y+58,146,3,'#82998d','rx="1.5"')+'</g>'
 b+=r(766,102,163,81,'#253832','rx="7" stroke="#a5e7d0" stroke-opacity=".65"')
 b+=t(778,123,'EVENT CLUSTER',10,MINT,700,font=MONO)+t(778,149,'Rail opening',18,WHITE,700)+t(778,168,'2 related reports',13,DIM)
 b+=p('M725 63Q752 63 765 119M751 139H765',MINT,1.4,'stroke-dasharray="3 4" class="join" opacity=".8"')
 b+=t(932,223,'ILLUSTRATIVE CLUSTER · NOT LIVE NEWS',10,DIM,400,'end',MONO)
 svg('spectrum-atlox.svg',960,240,'Atlox AI','Illustrative grouping of two related railway news reports into one event.',b,'.sheet{animation:sheet 5s ease-in-out infinite}.s1{animation-delay:-2s}.join{animation:join 1.5s linear infinite}@keyframes sheet{50%{transform:translate(3px,0)}}@keyframes join{to{stroke-dashoffset:-14}}')
def cane():
 d=json.loads((ROOT/'data'/'cane-routing.json').read_text())['counts'];n=sum(d.values())
 b=surface(960,240,CITRUS)+heading('03','CANE','CONTEXT-AWARE ROUTING',['Prioritize messages through context and retrieval.','Deterministic decisions, with explanations.'],'PYTHON · TF-IDF · RAPIDFUZZ · RULES',CITRUS)
 b+=t(27,177,'No external LLM in the core inference pipeline',13,CITRUS,500)
 b+=t(530,34,str(n)+' recorded predictions',17,WHITE,700)
 # One individual tile per real prediction; no fabricated accuracy statistic.
 i=0
 for key,col in [('notify',MINT),('digest',CITRUS),('mute','#9b9aa1')]:
  for j in range(d[key]):
   x=530+(i%22)*18;y=55+(i//22)*18
   b+=r(x,y,13,13,col,f'rx="3" opacity=".82" class="tile" style="animation-delay:-{(i%17)*.18:.2f}s"');i+=1
 for x,key,col in [(530,'notify',MINT),(667,'digest',CITRUS),(801,'mute','#b7b6bd')]:
  b+=c(x+5,165,4,col)+t(x+16,170,key.capitalize(),12,DIM)+t(x,197,str(d[key]),23,col,750,font=MONO)
 b+=t(932,223,'OUTPUT.CSV · COUNTS, NOT ACCURACY',10,DIM,400,'end',MONO)
 svg('spectrum-cane.svg',960,240,'CANE',f'{n} checked-in predictions: '+', '.join(f'{k} {v}' for k,v in d.items())+'. Each tile is one prediction.',b,'.tile{animation:tile 5.4s ease-in-out infinite}@keyframes tile{50%{opacity:.43}}')
def skills():
 b=surface(960,350,PEACH)
 b+=t(28,40,'Engineering toolkit',32,WHITE,700)+t(932,38,'BUILD / TEST / SHIP',12,PEACH,600,'end',MONO)
 rows=[('Languages','Python · Java · TypeScript','JavaScript · C/C++ · SQL',CORAL),('Backend','FastAPI · Flask · Node.js','REST · SQLAlchemy · JWT',PEACH),('Applied AI','PyTorch · Transformers · spaCy','scikit-learn · OpenCV · BM25',CITRUS),('Data systems','PostgreSQL · PostGIS · Redis','SQLite · MongoDB · Supabase',MINT),('Linux & delivery','Linux · Docker · Git · Actions','CI/CD · Pytest · Ruff · Mypy',PEACH),('Web engineering','React · Next.js · Vite','HTML/CSS · WebSockets',CORAL)]
 for i,(head,l1,l2,col) in enumerate(rows):
  x=28+(i%2)*468;y=67+(i//2)*92
  b+=p(f'M{x} {y}H{x+432}',col,1,'opacity=".26"')
  b+=r(x,y+14,4,57,col,'rx="2" opacity=".8"')
  b+=t(x+16,y+31,head,20,col,700)+t(x+16,y+53,l1,15,WHITE)+t(x+16,y+73,l2,15,DIM)
 # Deliberately no looping progress gauge or moving skill text.
 svg('spectrum-skills.svg',960,350,'Engineering toolkit','Six skill domains, languages, backend, applied AI, data systems, Linux delivery and web engineering.',b)
def nav():
 items=[('portfolio','Portfolio','Projects & case studies',CORAL),('linkedin','LinkedIn','Professional profile',PEACH),('leetcode','LeetCode','Problem solving',CITRUS),('email','Email','Get in touch',MINT)]
 for slug,label,detail,col in items:
  b=surface(450,76,col)+r(1,11,3,54,col,'rx="1.5"')+t(20,30,label,21,col,700)+t(20,52,detail,14,DIM)+p('M408 29H428V49M428 29L408 49',col,1.5,'stroke-linecap="round"')
  svg('spectrum-contact-'+slug+'.svg',450,76,label,detail,b)
 for slug,label,col in [('case','Case study',PEACH),('app','Application',MINT),('data','Prediction data',CITRUS)]:
  b=r(1,1,180,34,'#28292e','rx="8" stroke="'+col+'" stroke-opacity=".45"')+t(12,23,label,14,col,600)+p('M156 12H168V24M168 12L156 24',col,1.4)
  svg('spectrum-action-'+slug+'.svg',182,36,label,label,b)
def build(data):
 verifai();atlox();cane();skills();nav()
