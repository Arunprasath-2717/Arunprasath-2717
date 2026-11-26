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
def hero(data):
 # A folded spectral ribbon, sampled as a smooth ruled surface. Each strip has
 # a different material color; shading is determined by local surface curvature.
 # The art is fixed in space, with light moving over it rather than a camera zoom.
 b=surface(960,350,PEACH)
 b+='<defs><clipPath id="art"><rect x="422" y="4" width="536" height="245" rx="14"/></clipPath><linearGradient id="light"><stop stop-color="#fff9ed" stop-opacity="0"/><stop offset=".5" stop-color="#fff9ed" stop-opacity=".36"/><stop offset="1" stop-color="#fff9ed" stop-opacity="0"/></linearGradient></defs>'
 def pt(u,v):
  theta=u*math.tau*.88-1.2
  # Twisted ribbon orbit with a deliberately asymmetric profile.
  x=716+165*math.cos(theta)+v*54*math.cos(theta*.5+1)
  y=126+76*math.sin(theta)+v*44*math.sin(theta*.5+1)
  return x,y
 strips=20;steps=72
 palette=[CORAL,'#ffc09a',CITRUS,'#fff4bf',MINT]
 # Draw strips from far end to near; path overlap creates a folded textile.
 ribbon=''
 for j in range(strips):
  v0=-1+2*j/strips;v1=-1+2*(j+1)/strips
  z=(j/(strips-1))*(len(palette)-1);k=min(int(z),len(palette)-2)
  base=blend(palette[k],palette[k+1],z-k)
  for i in range(steps):
   u=i/steps;un=(i+1)/steps
   shade=.70+.30*(.5+.5*math.sin(u*math.tau*1.7+j*.075))
   col=blend('#41302d',base,shade)
   ribbon+=polygon([pt(u,v0),pt(un,v0),pt(un,v1),pt(u,v1)],col,'stroke="'+col+'" stroke-width=".45"')
 # Continuous edge lines make the object crisp, not a scatterplot.
 for v in (-1,1):
  d='M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in [pt(i/192,v) for i in range(193)])
  ribbon+=p(d,'#fff5dc',.9,'opacity=".66"')
 # Light reflection is clipped exactly to the ribbon silhouette.
 outline=[pt(i/192,-1) for i in range(193)]+[pt(i/192,1) for i in range(192,-1,-1)]
 b+='<g clip-path="url(#art)"><g class="ribbon">'+ribbon+'<defs><clipPath id="silk">'+polygon(outline,'white')+'</clipPath></defs><g clip-path="url(#silk)">'+r(405,-25,100,340,'url(#light)','class="shine" transform="skewX(-12)"')+'</g></g></g>'
 b+=t(29,39,'AP / 2717',13,PEACH,700,font=MONO,extra='letter-spacing="3"')
 b+=t(27,110,'Arun Prasath',59,WHITE,700)
 b+=t(30,153,'Backend engineering',24,WHITE,500)
 b+=t(30,185,'Applied AI · MLOps',24,WHITE,500)
 b+=t(30,228,'Computer science student · India',15,DIM)
 b+=p('M30 255H930','#696262',.8,'opacity=".65"')
 weeks=data['weeks'];peak=max([x['count'] for x in weeks]+[1]);total=sum(x['count'] for x in weeks)
 b+=t(30,279,'BUILD RECORD',11,PEACH,700,font=MONO,extra='letter-spacing="1.7"')
 b+=t(30,316,str(total),33,WHITE,750,font=MONO)
 b+=t(136,310,'GitHub contributions',13,DIM)
 for i,w in enumerate(weeks):
  x=335+i*11.15;n=w['count'];h=3+34*n/peak
  col=blend('#555458',PEACH,.25+.75*n/peak) if n else '#4a4a50'
  b+=f'<g><title>Week of {esc(w["date"])}: {n} contributions</title>'+r(round(x,2),round(316-h,2),7.5,round(h,2),col,'rx="2"')+'</g>'
 b+=t(930,338,data['as_of']+' UTC · weekly counts',10,DIM,400,'end',MONO)
 css='.ribbon{animation:ribbon 9s ease-in-out infinite;transform-origin:716px 126px}.shine{animation:shine 6s ease-in-out infinite}@keyframes ribbon{50%{transform:rotate(-3deg) translate(0,-4px)}}@keyframes shine{0%,15%{transform:translateX(-80px) skewX(-12deg);opacity:0}30%{opacity:.8}80%,100%{transform:translateX(550px) skewX(-12deg);opacity:0}}'
 svg('spectrum-hero.svg',960,350,'Arun Prasath','Original folded spectrum artwork. Backend engineering, applied AI and MLOps. The lower chart shows actual weekly GitHub counts.',b,css)
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
 hero(data);verifai();atlox();cane();skills();nav()
