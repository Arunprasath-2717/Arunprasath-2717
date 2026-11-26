"""Compact fieldwork visuals, self-contained SVGs, authentic checked-in CANE output."""
import base64, html, json, math, pathlib, xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'
FG='#f3f4e9'; DIM='#c4d0c4'; GREEN='#b6e3aa'; GOLD='#e7c78d'; BG='#141e19'
FONT='system-ui, -apple-system, Segoe UI, sans-serif'
MONO='Consolas, Liberation Mono, monospace'
def e(s):return html.escape(str(s),quote=True)
def t(x,y,s,size,color=FG,weight=400,anchor='start',font=FONT,extra=''):
 return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" font-family="{font}" text-anchor="{anchor}" {extra}>{e(s)}</text>'
def rect(x,y,w,h,color,extra=''):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" {extra}/>'
def circle(x,y,r,color,extra=''):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" {extra}/>'
def write(name,h,title,desc,body,css=''):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="960" height="{h}" viewBox="0 0 960 {h}" role="img" aria-labelledby="title desc"><title id="title">{e(title)}</title><desc id="desc">{e(desc)}</desc><style>{css}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>{rect(0,0,960,h,BG)}{body}</svg>\n'
 ET.fromstring(s);(OUT/name).write_text(s,encoding='utf-8')
def skills():
 # The landscape is the right half of a readable, single composition, not a separate filler image.
 src=base64.b64encode((ROOT/'assets'/'river-landscape.webp').read_bytes()).decode()
 b=f'''<defs><clipPath id="land"><rect x="490" y="0" width="470" height="510"/></clipPath><linearGradient id="blend"><stop stop-color="#141e19"/><stop offset=".55" stop-color="#141e19" stop-opacity=".72"/><stop offset="1" stop-color="#141e19" stop-opacity="0"/></linearGradient><linearGradient id="bottom" x2="0" y2="1"><stop stop-color="#141e19" stop-opacity="0"/><stop offset="1" stop-color="#141e19" stop-opacity=".85"/></linearGradient></defs>
 <g clip-path="url(#land)"><image x="490" y="0" width="470" height="510" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/webp;base64,{src}"/><rect x="490" y="0" width="470" height="510" fill="url(#blend)"/><rect x="490" y="350" width="470" height="160" fill="url(#bottom)"/></g>'''
 b+=t(29,38,'THE ENGINEERING TOOLKIT',13,GOLD,750,font=MONO,extra='letter-spacing="2"')
 b+=t(28,80,'From code to running systems.',33,FG,700)
 groups=[
 ('01','Languages','Python · Java · TypeScript · JavaScript · C/C++ · SQL'),
 ('02','Backend','FastAPI · Flask · Node.js · REST · SQLAlchemy · JWT'),
 ('03','Applied AI','PyTorch · Transformers · spaCy · scikit-learn · OpenCV'),
 ('04','Data systems','PostgreSQL · PostGIS · Redis · SQLite · MongoDB · Supabase'),
 ('05','Linux & delivery','Linux · Docker · Git · GitHub Actions · CI/CD · Pytest'),
 ('06','Web engineering','React · Next.js · Vite · HTML/CSS · WebSockets · Ruff · Mypy')]
 for i,(num,title,detail) in enumerate(groups):
  y=115+i*62
  b+=t(29,y,num,11,GREEN,700,font=MONO)+t(64,y,title,20,FG,700)
  b+=t(64,y+24,detail,14,DIM,450)
  if i<5:b+=rect(64,y+38,420,1,'#3d5145')
 # Low-key atmospheric particles remain restricted to the landscape.
 for i in range(26):
  x=680+(i*71)%269;y=25+(i*47)%450
  b+=circle(x,y,1.2+(i%3)*.35,'#f3d9a4',f'opacity=".55" class="mote" style="animation-delay:-{i*.67:.2f}s"')
 b+=t(933,479,'LINUX / CLOUD / ML',12,FG,750,'end',MONO)
 b+=rect(28,484,445,2,'#506b50')
 b+=rect(28,484,70,2,GREEN,'class="signal"')
 write('field-skills.svg',510,'Engineering toolkit','Six skill areas: languages, backend, applied AI, data systems, Linux and delivery, web engineering. A landscape of ancient ruins accompanies the skills.',b,'.mote{animation:mote 7s ease-in-out infinite}.signal{animation:signal 12s ease-in-out infinite}@keyframes mote{50%{transform:translate(11px,-16px);opacity:.15}}@keyframes signal{50%{transform:translateX(375px)}}')
def cane():
 data=json.loads((ROOT/'data'/'cane-routing.json').read_text());counts=data['counts'];n=sum(counts.values())
 # An actual dataset, not simulated live activity. The block positions and bar lengths encode counts.
 b=t(28,36,'CANE / ROUTING RESULTS',12,GOLD,700,font=MONO,extra='letter-spacing="1.5"')
 b+=t(28,83,str(n),45,FG,750,font=MONO)+t(28,108,'checked-in predictions',16,DIM)
 b+=t(28,134,'Deterministic scoring · evidence-backed decisions',12,DIM)
 b+=t(932,35,'DATASET / OUTPUT.CSV',11,DIM,600,'end',MONO)
 colors={'notify':'#9edb9e','digest':'#d7ba80','mute':'#7f9386'}
 x0=352; width=580;start=x0
 for i,(action,count) in enumerate(counts.items()):
  w=width*count/n
  b+=rect(round(start,2),63,round(w-3,2),60,colors[action],'rx="2"')
  b+=t(round(start+w/2,2),101,str(count),26,'#142119',750,'middle',MONO)
  b+=t(round(start+w/2,2),144,action.upper(),12,colors[action],700,'middle',MONO)
  start+=w
 # Sweeping emphasis reveals the distribution without changing any measured value.
 b+=f'<defs><clipPath id="bar"><rect x="{x0}" y="63" width="{width}" height="60"/></clipPath></defs>'
 b+='<g clip-path="url(#bar)"><rect x="352" y="63" width="3" height="60" fill="#ffffff" opacity=".3" class="scan"/></g>'
 b+=rect(28,165,904,1,'#405247')+t(28,188,'Source: CANE dataset/output.csv · counts are not accuracy or live traffic.',12,DIM)
 write('field-cane.svg',206,'CANE prediction distribution',f"{n} checked-in predictions: "+', '.join(f"{k}: {v}" for k,v in counts.items())+'. Not a performance measure.',b,'.scan{animation:scan 7s linear infinite}@keyframes scan{0%{transform:translateX(0);opacity:0}10%,90%{opacity:.4}100%{transform:translateX(580px);opacity:0}}')
if __name__=='__main__':skills();cane()
