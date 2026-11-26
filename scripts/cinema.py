"""Night shift: original SVG artwork and animated editorial modules.
The scene is fictional; all contribution counts come from GitHub.
"""
import html, math, random
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]/'assets'
THEMES={
'dark':dict(bg='#171b20',fg='#f0f3f1',dim='#b1b9ba',rule='#3d484b',accent='#e3c491',leaf='#70db94',paper='#242c30',black='#171b20'),
'light':dict(bg='#f6f8f6',fg='#1e2724',dim='#4f6058',rule='#c9d3ce',accent='#865b27',leaf='#19743d',paper='#e7ede9',black='#1e2724')}
MONO='ui-monospace, SFMono-Regular, Consolas, Liberation Mono, monospace'
SANS='system-ui, -apple-system, Segoe UI, sans-serif'
SERIF='Georgia, Times New Roman, serif'
def e(s): return html.escape(str(s),quote=True)
def R(x,y,w,h,f,rx=0,extra=''): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" {extra}/>'
def P(d,f,extra=''): return f'<path d="{d}" fill="{f}" {extra}/>'
def L(d,f,w=1,extra=''): return f'<path d="{d}" fill="none" stroke="{f}" stroke-width="{w}" {extra}/>'
def C(x,y,r,f,extra=''): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{f}" {extra}/>'
def T(x,y,s,size,f,weight=400,anchor='start',font=SANS,extra=''): return f'<text x="{x}" y="{y}" font-size="{size}" fill="{f}" font-weight="{weight}" text-anchor="{anchor}" font-family="{font}" {extra}>{e(s)}</text>'
def G(body,extra=''):return f'<g {extra}>{body}</g>'
def write(name,theme,h,title,desc,body,css=''):
    c=THEMES[theme]
    style='<style>'+css+'@media(prefers-reduced-motion:reduce){*{animation:none!important}}</style>'
    out=f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{h}" viewBox="0 0 960 {h}" role="img" aria-labelledby="title desc"><title id="title">{e(title)}</title><desc id="desc">{e(desc)}</desc>{style}{R(0,0,960,h,c["bg"],8)}{body}</svg>\n'
    (OUT/f'{name}-{theme}.svg').write_text(out,encoding='utf-8')

# Perspective surfaces use solid pigments and offset faces, not filters or external imagery.
def slab(x,y,w,h,c,d=13):
    return (P(f'M{x} {y}l{d} {-d}h{w}l{-d} {d}Z',c['rule'])
            +P(f'M{x+w} {y}l{d} {-d}v{h}l{-d} {d}Z',c['black'])
            +R(x,y,w,h,c['paper'],3,extra=f'stroke="{c["rule"]}"'))
def route(d,c,delay=0):
    return L(d,c['rule'],6,'stroke-linecap="round"')+L(d,c['leaf'],2,f'stroke-linecap="round" stroke-dasharray="4 18" class="travel" style="animation-delay:{delay}s"')
MOTION='.travel{animation:travel 2s linear infinite}.float{animation:float 4s ease-in-out infinite}.lamp{animation:lamp 3s ease-in-out infinite}.sweep{animation:sweep 4s ease-in-out infinite}@keyframes travel{to{stroke-dashoffset:-44}}@keyframes float{50%{transform:translateY(-7px)}}@keyframes lamp{50%{opacity:.35}}@keyframes sweep{0%,100%{transform:translateY(0)}50%{transform:translateY(40px)}}'
def project(theme,p,index):
    c=THEMES[theme];fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['leaf']
    b=T(28,33,f'0{index} / {p["category"]}',12,ac,700,font=MONO,extra='letter-spacing="1.3"')
    b+=T(28,91,p['name'],46,fg,750)
    for i,s in enumerate(p['summary']):b+=T(30,125+i*24,s,15,dim)
    b+=T(30,215,p['stack'],12,fg,500,font=MONO)
    b+=T(30,240,'ARCHITECTURE STUDY / 0'+str(index),10,ac,650,font=MONO)
    # A low stage and two receding planes create a coherent physical space.
    b+=P('M491 212L615 53H944L927 208L823 252H491Z',c['paper'])
    b+=P('M491 212H927L823 252H491Z',c['rule'])
    if p['slug']=='verifai':
        # Evidence stack feeding a raised review processor and a verdict display.
        b+=route('M571 154H646V112H693',c)+route('M755 122H805V159H846',c,-.8)
        for i in range(3):
            x=518+i*7;y=130-i*11
            b+=slab(x,y,57,59,c,8)+R(x+8,y+10,38,3,dim,1)+R(x+8,y+19,29,2,c['rule'],1)
        b+=T(547,213,'CLAIMS',10,fg,700,'middle',MONO)
        b+=slab(653,84,113,93,c,15)
        b+=R(664,96,91,63,c['bg'],4)
        b+=T(709,119,'EVIDENCE',12,gr,700,'middle',MONO)+T(709,136,'+ JUDGES',11,fg,600,'middle',MONO)
        b+=R(664,101,91,2,gr,extra='class="sweep" opacity=".6"')
        b+=T(709,192,'REVIEW',10,fg,700,'middle',MONO)
        for i,(label,col) in enumerate([('SUPPORT',gr),('DISPUTE',ac),('UNKNOWN',dim)]):
            y=86+i*42
            b+=slab(814,y,112,30,c,8)+C(825,y+15,3.5,col,extra=f'class="lamp" style="animation-delay:{-i*.7}s"')+T(838,y+19,label,11,col,750,font=MONO)
    elif p['slug']=='atlox':
        # Incoming feeds, stacked ingest processor, distinct event cluster outputs.
        for i,label in enumerate(['RSS','API','FEED']):
            y=77+i*43
            b+=route(f'M569 {y+15}H611L645 139',c,-i*.6)
            b+=slab(507,y,62,28,c,8)+T(538,y+19,label,11,fg,700,'middle',MONO)
        b+=slab(644,91,101,91,c,16)
        b+=R(656,104,77,49,c['bg'],4)+T(694.5,124,'NLP',19,gr,750,'middle',MONO)+T(694.5,140,'CLUSTER',9,fg,700,'middle',MONO)
        for i in range(5):b+=R(657+i*15,163,9,4,gr if i%2 else ac,1,extra=f'class="lamp" style="animation-delay:{-i*.23}s"')
        for i,(label,num) in enumerate([('EVENTS',5),('ENTITIES',4),('SENTIMENT',6)]):
            y=73+i*50
            b+=route(f'M745 136H770V{y+18}H797',c,-i*.7)
            b+=slab(797,y,129,39,c,8)+T(807,y+14,label,10,fg,750,font=MONO)
            for j in range(num):
                b+=R(808+j*17,y+21,13,9,gr if (i+j)%3 else ac,2,extra=f'class="lamp" style="animation-delay:{-j*.21-i*.6}s"')
    else:
        # Message slabs arrive at the context engine and follow separate delivery routes.
        for i,label in enumerate(['Urgent','Routine','Untrusted']):
            y=83+i*41
            b+=route(f'M604 {y+14}H628L655 132',c,-i*.5)
            b+=slab(506,y,98,28,c,8)+T(516,y+19,label,12,fg,600)
        b+=slab(653,93,104,89,c,15)
        b+=R(664,103,82,49,c['bg'],4)+T(705,124,'CONTEXT',12,gr,750,'middle',MONO)+T(705,141,'score + rules',10,dim,400,'middle')
        b+=T(705,167,'ROUTER',10,ac,700,'middle',MONO)
        for i,(label,col) in enumerate([('NOTIFY',gr),('DIGEST',ac),('MUTE',dim)]):
            y=73+i*50
            b+=route(f'M757 135H781V{y+18}H800',c,-i*.7)
            b+=slab(800,y,125,34,c,8)+C(812,y+17,4,col,extra=f'class="lamp" style="animation-delay:{-i*.7}s"')+T(824,y+21,label,12,col,750,font=MONO)
    write(p['slug'],theme,274,p['name'],'. '.join(p['summary'])+'. Isometric conceptual system flow, not live traffic.',b,MOTION)

def toolkit(theme):
    c=THEMES[theme];fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['leaf']
    b=T(28,35,'02 / ENGINEERING TOOLCHAIN',12,ac,700,font=MONO,extra='letter-spacing="1.5"')
    b+=T(28,82,'From source to serving.',36,fg,700,font=SERIF)
    b+=P('M28 203L151 105H933L899 202L819 243H28Z',c['paper'])
    b+=P('M28 203H899L819 243H28Z',c['rule'])
    stages=[('LINUX','Develop'),('GIT / CI','Test'),('DOCKER','Package'),('CLOUD','Deploy'),('ML','Serve')]
    for i,(label,sub) in enumerate(stages):
        x=46+i*181
        if i<4:b+=route(f'M{x+140} 166H{x+181}',c,-i*.3)
        b+=slab(x,137,140,59,c,13)
        b+=T(x+10,153,f'0{i+1}',10,ac,700,font=MONO)
        b+=T(x+10,176,label,15,fg,750,font=MONO)
        b+=C(x+125,150,3.5,gr,extra=f'class="lamp" style="animation-delay:{-i*.4}s"')
        b+=T(x+10,219,sub,12,fg,650)
    groups=[
      ('LANGUAGES','Python · Java · TypeScript','JavaScript · C / C++ · SQL'),
      ('BACKEND','FastAPI · Flask · Node.js','REST APIs · SQLAlchemy · JWT'),
      ('APPLIED AI','PyTorch · Transformers · spaCy','scikit-learn · BM25 · OpenCV · Evaluation'),
      ('DATA SYSTEMS','PostgreSQL · PostGIS · Redis','SQLite · MongoDB · Supabase'),
      ('LINUX & DELIVERY','Linux · Docker · Git · GitHub Actions','CI/CD · Pytest · Ruff · Mypy'),
      ('WEB ENGINEERING','React · Next.js · Vite','HTML / CSS · WebSockets')]
    for i,(label,a,d) in enumerate(groups):
        x=28+(i%2)*460;y=269+(i//2)*93
        b+=slab(x,y,437,72,c,8)
        b+=T(x+12,y+20,label,11,ac,750,font=MONO)
        b+=T(x+12,y+41,a,14,fg,600)
        b+=T(x+12,y+60,d,13,dim)
    b+=R(28,557,904,56,c['paper'],5)
    b+=T(42,577,'CURRENT STUDY / MLOPS',11,ac,750,font=MONO)
    b+=T(42,598,'Kubernetes · Terraform · AWS · Model registries · Experiment tracking · Observability',14,fg)
    write('toolchain',theme,631,'Engineering toolchain','Six skill domains and a conceptual five-stage deployment line. Current study: Kubernetes, Terraform, AWS, model registries, experiment tracking and observability.',b,MOTION)

def focus(theme):
    c=THEMES[theme];fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['leaf']
    b=T(28,35,'03 / CURRENT FOCUS',12,ac,700,font=MONO,extra='letter-spacing="1.5"')
    b+=T(28,80,'The systems I want to master.',35,fg,700,font=SERIF)
    # Three chapters of one architecture; deliberately no progress percentages.
    chapters=[('01','Reliable backends','API contracts · persistence','Validation · tests','FastAPI / PostgreSQL'),('02','Applied intelligence','Retrieval · verification','NLP · evaluation','PyTorch / BM25'),('03','ML infrastructure','Reproducible training','Model serving · monitoring','Studying cloud / MLOps')]
    b+=P('M28 227L159 105H932L910 232L801 275H28Z',c['paper'])
    b+=P('M28 227H910L801 275H28Z',c['rule'])
    for i,(num,title,a,d,tools) in enumerate(chapters):
        x=46+i*300
        if i<2:b+=route(f'M{x+244} 174H{x+300}',c,-i*.7)
        b+=slab(x,129,244,88,c,15)
        b+=T(x+12,148,num,11,ac,750,font=MONO)
        b+=T(x+12,174,title,19,fg,700)
        b+=T(x+12,194,a,12,dim)
        b+=T(x+12,209,d,12,dim)
        b+=C(x+226,143,4,gr,extra=f'class="lamp" style="animation-delay:{-i*.8}s"')
        b+=T(x+3,249,tools,11,fg,600,font=MONO)
    b+=T(28,298,'Learning: Kubernetes · Terraform · AWS · experiment tracking · observability',14,dim)
    write('focus',theme,319,'Current engineering focus','Reliable backend systems, applied intelligence, and ML infrastructure. Cloud and MLOps topics are learning interests.',b,MOTION)
def activity(theme,data):
    c=THEMES[theme];fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['leaf']
    weeks=data['weeks'];counts=[w['count'] for w in weeks];total=sum(counts)
    b=T(28,32,'GITHUB / DEVELOPMENT RECORD',12,ac,700,font=MONO)
    for x,num,label in [(28,total,'Contributions'),(335,sum(n>0 for n in counts),'Active weeks'),(640,max(counts+[0]),'Peak week')]:
        b+=T(x,91,str(num),43,fg,750,font=MONO)+T(x,113,label,13,dim)
    b+=L('M28 132H932',c['rule'])
    b+=T(28,153,f'{len(weeks)} calendar weeks · actual GitHub data',12,dim)
    b+=T(932,153,data['as_of']+' UTC',12,dim,400,'end',MONO)
    # Preserve machine-readable weekly values even though the snake displays the daily grid.
    for w in weeks:
        b+=G(f'<title>Week of {e(w["date"])}: {w["count"]} contributions</title>')
    write('activity',theme,172,'GitHub development record',f'{total} contributions over {len(weeks)} weeks. Updated {data["as_of"]}.',b)
