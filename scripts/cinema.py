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

def project(theme,p,index):
    c=THEMES[theme];fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['leaf']
    b=T(29,32,'0'+str(index)+'  /  '+p['category'],12,ac,700,font=MONO,extra='letter-spacing="1.4"')
    b+=T(28,79,p['name'],41,fg,750)
    for i,s in enumerate(p['summary']):b+=T(30,108+i*22,s,15,dim)
    b+=T(30,177,p['stack'],12,fg,500,font=MONO)
    b+=R(484,18,450,174,c['paper'],5)
    if p['slug']=='verifai':
        # Three evidence slips physically enter a review tray. Explicit unknown stays visible.
        b+=T(502,39,'EVIDENCE REVIEW',11,dim,700,font=MONO)
        for i,(title,detail,mark,col) in enumerate([('Claim 01','Evidence found','SUPPORT',gr),('Claim 02','Source conflict','DISPUTE',ac),('Claim 03','Insufficient data','UNKNOWN',dim)]):
            y=52+i*43
            q=R(502,y,410,35,c['bg'],3)+R(502,y,4,35,col,1)+T(514,y+14,title,12,fg,650)+T(514,y+27,detail,10,dim)+T(898,y+22,mark,11,col,700,'end',MONO)
            b+=G(q,f'class="review" style="animation-delay:{-i*1.2}s"')
        b+=R(502,183,410,2,c['rule'])
        b+=R(502,183,75,2,gr,extra='class="scanner"')
    elif p['slug']=='cane':
        # Example messages enter a deterministic router and land in three distinct trays.
        b+=T(502,39,'CONTEXT-AWARE ROUTER',11,dim,700,font=MONO)
        b+=R(502,54,108,118,c['bg'],4)+T(515,73,'INBOX',10,dim,700,font=MONO)
        for i,(label,detail) in enumerate([('Message','Urgent'),('Message','Routine'),('Message','Untrusted')]):
            y=82+i*27
            b+=R(511,y,90,23,c['paper'],3)+T(517,y+15,detail,10,fg,600)
        b+=R(635,87,92,52,c['bg'],5)+T(681,109,'CONTEXT',12,ac,750,'middle',MONO)+T(681,125,'score + rules',10,dim,400,'middle')
        b+=L('M610 113H635',c['rule'],3)+L('M727 113H751',c['rule'],3)
        for i,(label,color) in enumerate([('NOTIFY',gr),('DIGEST',ac),('MUTE',dim)]):
            y=59+i*42
            b+=L(f'M751 113V{y+15}H769',c['rule'],2)
            b+=R(769,y,145,31,c['bg'],4)+R(769,y,5,31,color,2)
            b+=T(783,y+20,label,12,color,750,font=MONO)
            b+=C(900,y+15,3.7,color,extra=f'class="packetlight" style="animation-delay:{-i*1.1}s"')
        b+=T(502,184,'Example routing · same inputs, same outputs',10,dim)
    else:
        # News packets enter an editorial stream and resolve into event clusters.
        b+=T(502,39,'STREAM PROCESSING',11,dim,700,font=MONO)
        for i,label in enumerate(['RSS','API','FEED']):
            y=58+i*37
            b+=R(502,y,74,28,c['bg'],3)+T(539,y+19,label,11,fg,700,'middle',MONO)
            b+=L(f'M576 {y+14}H601L628 108',c['rule'],2)
            b+=G(C(0,0,3.5,ac),f'class="packet p{i}" transform="translate(576 {y+14})"')
        b+=R(628,75,90,66,c['bg'],4)+T(673,103,'NLP',17,ac,750,'middle')+T(673,123,'cluster',11,dim,400,'middle')
        for i,(label,n) in enumerate([('EVENTS',5),('ENTITIES',4),('SENTIMENT',6)]):
            y=56+i*44
            b+=L(f'M718 108L746 {y+13}H761',c['rule'],2)+T(772,y+12,label,10,fg,650,font=MONO)
            for j in range(n):b+=R(773+j*18,y+18,13,9,gr if (j+i)%3 else ac,2,extra=f'class="packetlight" style="animation-delay:{-j*.3-i*.7}s"')
    css='.review{animation:review 6s ease-in-out infinite}.scanner{animation:scan 6s ease-in-out infinite}.packet{animation:packet 3.5s linear infinite}.p1{animation-delay:-1.2s}.p2{animation-delay:-2.4s}.packetlight{animation:led 3s ease-in-out infinite}@keyframes review{0%,100%{opacity:.72}25%,55%{opacity:1}}@keyframes scan{0%{transform:translateX(0)}50%{transform:translateX(335px)}100%{transform:translateX(0)}}@keyframes packet{0%{opacity:0;translate:0 0}20%{opacity:1}70%{opacity:1;translate:28px 0}100%{opacity:0;translate:52px 0}}@keyframes led{50%{opacity:.35}}'
    write(p['slug'],theme,210,p['name'],'. '.join(p['summary'])+'. Conceptual animation, not live service telemetry.',b,css)

def toolkit(theme):
    c=THEMES[theme];fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['leaf']
    b=T(28,35,'02 / ENGINEERING TOOLCHAIN',12,ac,700,font=MONO,extra='letter-spacing="1.5"')
    b+=T(28,80,'From source to serving.',37,fg,700,font=SERIF)
    b+=T(930,35,'AP / 2717',11,dim,600,'end',MONO)
    # A small connected deployment sequence. Stages are interests, not measured infrastructure.
    b+=R(28,101,904,100,c['paper'],6)
    stages=[('01','LINUX','Develop'),('02','GIT / CI','Test & build'),('03','DOCKER','Package'),('04','CLOUD','Deploy'),('05','ML','Serve & evaluate')]
    for i,(num,label,sub) in enumerate(stages):
        x=45+i*179
        if i<4:
            b+=L(f'M{x+143} 144H{x+178}',c['rule'],3)
            b+=L(f'M{x+143} 144H{x+178}',gr,2,'stroke-dasharray="5 15" class="flow"')
        b+=R(x,115,143,57,c['bg'],5)
        b+=T(x+10,132,num,10,ac,700,font=MONO)
        b+=T(x+10,152,label,15,fg,750,font=MONO)
        b+=T(x+4,188,sub,12,dim)
    groups=[
      ('01','LANGUAGES',['Python','Java','TypeScript','JavaScript','C / C++','SQL']),
      ('02','BACKEND',['FastAPI','Flask','Node.js','REST APIs','SQLAlchemy','JWT']),
      ('03','APPLIED AI',['PyTorch','Transformers','spaCy','scikit-learn','BM25','OpenCV','Evaluation']),
      ('04','DATA SYSTEMS',['PostgreSQL','PostGIS','Redis','SQLite','MongoDB','Supabase']),
      ('05','LINUX & DELIVERY',['Linux','Docker','Git','GitHub Actions','CI/CD','Pytest','Ruff','Mypy']),
      ('06','WEB ENGINEERING',['React','Next.js','Vite','HTML / CSS','WebSockets'])
    ]
    # Type-led groups with small filled labels, rather than fake proficiency gauges.
    for i,(num,label,skills) in enumerate(groups):
        x=28+(i%2)*460;y=225+(i//2)*105
        b+=L(f'M{x} {y}H{x+442}',c['rule'])
        b+=R(x,y+12,27,24,ac,3)+T(x+13.5,y+29,num,11,c['black'] if theme=='dark' else '#ffffff',750,'middle',MONO)
        b+=T(x+39,y+29,label,14,fg,750,font=MONO)
        cx=x;cy=y+43
        for j,skill in enumerate(skills):
            w=15+len(skill)*7.4
            if cx+w>x+442:cx=x;cy+=29
            b+=R(round(cx,1),cy,round(w,1),23,c['paper'],4)
            b+=T(round(cx+7,1),cy+15,skill,12,fg,550)
            cx+=w+6
    b+=R(28,551,904,65,c['paper'],6)
    b+=T(42,571,'CURRENT STUDY / MLOPS',11,ac,750,font=MONO)
    b+=T(42,593,'Kubernetes · Terraform · AWS · Model registries · Experiment tracking · Observability',14,fg)
    write('toolchain',theme,633,'Engineering toolchain','Six skill domains and a Linux to model-serving delivery sequence. Kubernetes, Terraform, AWS and MLOps topics are current learning interests.',b,'.flow{animation:flow 2.2s linear infinite}@keyframes flow{to{stroke-dashoffset:-40}}')

def focus(theme):
    c=THEMES[theme];fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['leaf']
    b=T(28,34,'03 / CURRENT FOCUS',12,ac,700,font=MONO,extra='letter-spacing="1.5"')
    b+=T(28,78,'Build it. Ship it. Understand it.',35,fg,700,font=SERIF)
    rows=[
        ('01','Reliable backends','API contracts, validation, persistence and tests.','FastAPI / PostgreSQL / Redis'),
        ('02','Applied intelligence','Retrieval, claim-level evidence, NLP and evaluation.','PyTorch / Transformers / BM25'),
        ('03','ML infrastructure','Reproducible training, serving and monitoring.','Studying Kubernetes / Terraform / AWS')
    ]
    for i,(num,title,detail,tools) in enumerate(rows):
        y=104+i*78
        b+=R(28,y,904,66,c['paper'],5)
        b+=R(28,y,5,66,gr if i!=2 else ac,2)
        b+=T(46,y+23,num,12,gr,700,font=MONO)+T(85,y+25,title,19,fg,700)
        b+=T(85,y+48,detail,13,dim)
        b+=T(913,y+25,tools,12,ac,600,'end',MONO)
        b+=C(911,y+46,3.5,gr,extra=f'class="beacon" style="animation-delay:{-i*.8}s"')
    write('focus',theme,352,'Current engineering focus','Reliable backend systems, applied AI and ML infrastructure. Kubernetes, Terraform and AWS are learning interests.',b,'.beacon{animation:beacon 4s ease-in-out infinite}@keyframes beacon{50%{opacity:.35}}')

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
