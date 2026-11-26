"""Original continuous-motion skill and MLOps modules for the floating-mountain profile.
All animation is illustrative; no invented uptime, proficiency scores, or service metrics.
"""
import math
from cinema import THEMES, T, R, P, L, C, G, write, MONO, SERIF

CSS = '''.current{animation:current 3s linear infinite}.hover{animation:hover 6s ease-in-out infinite}.pulse{animation:pulse 4s ease-in-out infinite}.orbit{animation:orbit 12s linear infinite}.glint{animation:glint 7s ease-in-out infinite}@keyframes current{to{stroke-dashoffset:-64}}@keyframes hover{50%{transform:translateY(-7px)}}@keyframes pulse{50%{opacity:.3}}@keyframes orbit{to{stroke-dashoffset:-120}}@keyframes glint{0%,100%{opacity:.35}50%{opacity:1}}'''

def colors(theme):
    c=dict(THEMES[theme]); c.update({'stone':'#43594c','face':'#263d32','gold':'#d9bb79'} if theme=='dark' else {'stone':'#b9c9b9','face':'#90a79a','gold':'#865b27'});return c

def label(x,y,s,c):return T(x,y,s,11,c['accent'],700,font=MONO,extra='letter-spacing="1.2"')
def current(d,c,delay=0,w=2):
    return L(d,c['rule'],w+4,'stroke-linecap="round"')+L(d,c['leaf'],w,f'stroke-linecap="round" stroke-dasharray="7 25" class="current" style="animation-delay:{delay}s"')
def platform(x,y,rx,ry,c):
    # Curved geological mass, not repeating UI boxes.
    return (P(f'M{x-rx} {y}Q{x-rx*.8} {y-ry} {x} {y-ry}Q{x+rx*.85} {y-ry} {x+rx} {y}L{x+rx*.72} {y+ry*1.1}L{x+rx*.25} {y+ry*2.1}L{x-rx*.13} {y+ry*1.65}L{x-rx*.64} {y+ry*1.3}Z',c['face'])
        +P(f'M{x-rx} {y}Q{x-rx*.8} {y-ry} {x} {y-ry}Q{x+rx*.85} {y-ry} {x+rx} {y}Q{x+rx*.35} {y+ry*.66} {x} {y+ry*.66}Q{x-rx*.75} {y+ry*.66} {x-rx} {y}Z',c['stone'])
        +L(f'M{x-rx*.84} {y-3}Q{x} {y-ry*.68} {x+rx*.84} {y-3}',c['leaf'],1.1,'opacity=".7"'))

def toolkit(theme):
    c=colors(theme);fg,dim,gr=c['fg'],c['dim'],c['leaf']
    b=label(30,34,'02 / THE ENGINEERING CONSTELLATION',c)+T(30,78,'The systems behind the summit.',34,fg,700,font=SERIF)
    # Orbital spatial composition: actual skill labels remain stationary while signal pulses orbit.
    b+=P('M23 280Q160 227 314 243T599 238T937 282L937 333H23Z',c['paper'])
    for rx,ry in [(413,105),(329,76),(242,50)]:
        b+=f'<ellipse cx="480" cy="204" rx="{rx}" ry="{ry}" fill="none" stroke="{c["rule"]}" stroke-width="2"/>'
        b+=f'<ellipse cx="480" cy="204" rx="{rx}" ry="{ry}" fill="none" stroke="{gr}" stroke-width="1.6" stroke-dasharray="12 108" class="orbit" opacity=".8"/>'
    b+=platform(480,230,87,23,c)
    b+=G(C(480,187,38,c['paper'],extra=f'stroke="{c["accent"]}" stroke-width="2"')+T(480,197,'AP',27,fg,750,'middle',MONO), 'class="hover"')
    nodes=[(111,204,'Linux','01'),(201,125,'Python','02'),(382,112,'FastAPI','03'),(587,112,'PyTorch','04'),(756,125,'PostgreSQL','05'),(849,204,'Docker','06'),(687,277,'Git / CI','07'),(273,277,'MLOps','08')]
    for i,(x,y,n,num) in enumerate(nodes):
        b+=platform(x,y+12,46,12,c)+C(x,y-10,18,c['paper'],extra=f'stroke="{gr}" stroke-width="1.4"')+T(x,y-6,num,10,gr,700,'middle',MONO)
        b+=T(x,y+42,n,14,fg,700,'middle')
        b+=C(x+23,y-17,3,c['accent'],extra=f'class="pulse" style="animation-delay:{-i*.37}s"')
    b+=T(480,343,'Linux → build → test → package → deploy → serve',13,dim,500,'middle',MONO)
    groups=[('LANGUAGES','Python · Java · TypeScript','JavaScript · C / C++ · SQL'),('BACKEND','FastAPI · Flask · Node.js','REST APIs · SQLAlchemy · JWT'),('APPLIED AI','PyTorch · Transformers · spaCy','scikit-learn · BM25 · OpenCV · Evaluation'),('DATA SYSTEMS','PostgreSQL · PostGIS · Redis','SQLite · MongoDB · Supabase'),('LINUX & DELIVERY','Linux · Docker · Git · GitHub Actions','CI/CD · Pytest · Ruff · Mypy'),('WEB ENGINEERING','React · Next.js · Vite','HTML / CSS · WebSockets')]
    for i,(name,a,d) in enumerate(groups):
        x=30+(i%2)*462;y=374+(i//2)*75
        b+=L(f'M{x} {y}H{x+432}',c['rule'])+label(x,y+19,name,c)+T(x,y+40,a,15,fg,600)+T(x,y+59,d,13,dim)
    b+=T(30,615,'Exploring: Kubernetes · Terraform · AWS · Model registries · Observability',14,dim)
    write('toolchain',theme,640,'Engineering skills constellation','Six skill groups with an animated orbit, illustrating the connection between Linux, backend systems, AI, cloud delivery and MLOps.',b,CSS)

def focus(theme):
    c=colors(theme);fg,dim,gr=c['fg'],c['dim'],c['leaf']
    b=label(30,35,'03 / CURRENT FOCUS',c)+T(30,80,'Three frontiers. One discipline.',35,fg,700,font=SERIF)
    b+=current('M153 190C270 90 325 268 480 190S700 110 807 190',c,0,2)
    for i,x in enumerate([153,480,807]):
        b+=platform(x,220,122,31,c)
        if i==0:
            # Solid layered storage cylinders on the first island.
            for j in range(3):
                y=179-j*22
                b+=R(x-47,y,94,20,c['face'],2)+f'<ellipse cx="{x}" cy="{y}" rx="47" ry="12" fill="{c["stone"]}" stroke="{gr}" stroke-width="1.4"/>'
                b+=C(x+35,y+12,2.8,gr,extra=f'class="pulse" style="animation-delay:{-j*.5}s"')
        elif i==1:
            # Rotating inference/evidence pathways around a stable central artifact.
            b+=G(C(x,162,39,c['paper'],extra=f'stroke="{gr}" stroke-width="1.7"')+T(x,170,'AI',25,fg,750,'middle',MONO),'class="hover"')
            for rx,ry,rot in [(74,25,0),(74,25,60),(74,25,-60)]:
                b+=f'<ellipse cx="{x}" cy="162" rx="{rx}" ry="{ry}" transform="rotate({rot} {x} 162)" fill="none" stroke="{gr}" stroke-width="1.8" stroke-dasharray="9 13" class="orbit" opacity=".8"/>'
        else:
            # A cloud silhouette floats above a serving platform.
            cloud=P(f'M{x-67} 183Q{x-86} 166 {x-67} 148Q{x-54} 136 {x-37} 141Q{x-23} 111 {x+9} 120Q{x+37} 118 {x+44} 148Q{x+72} 143 {x+75} 165Q{x+78} 183 {x+56} 190H{x-49}Q{x-62} 190 {x-67} 183Z',c['stone'],f'stroke="{gr}" stroke-width="1.8"')
            b+=G(cloud+T(x,172,'ML',21,fg,750,'middle',MONO),'class="hover"')
            b+=current(f'M{x} 189V217',c,-.5,1.5)
    details=[('Reliable backends','API contracts · persistence','Validation · testing'),('Applied intelligence','Retrieval · verification','NLP · evaluation'),('ML infrastructure','Reproducibility · serving','Monitoring · cloud study')]
    for i,(head,a,d) in enumerate(details):
        x=153+i*327;b+=T(x,290,head,19,fg,700,'middle')+T(x,315,a,13,dim,400,'middle')+T(x,334,d,13,dim,400,'middle')
    write('focus',theme,358,'Current focus','Three animated floating platforms represent backend reliability, applied intelligence and ML infrastructure learning.',b,CSS)

def lifecycle(theme):
    c=colors(theme);fg,dim,gr=c['fg'],c['dim'],c['leaf']
    b=label(30,35,'04 / MLOPS LEARNING MAP',c)+T(30,79,'From experiment to production.',34,fg,700,font=SERIF)
    # One loop, including evaluation/feedback; moving currents communicate order only.
    stages=[(127,150,'01','Ingest','Data & validation'),(365,150,'02','Train','Version & track'),(603,150,'03','Evaluate','Quality gates'),(841,150,'04','Serve','Container & API'),(603,300,'05','Observe','Logs & metrics'),(365,300,'06','Improve','Feedback loop')]
    for i,d in enumerate(['M187 150H305','M425 150H543','M663 150H781','M841 175V237Q841 300 670 300','M543 300H425','M305 300H160Q127 300 127 175']):b+=current(d,c,-i*.48,2.2)
    for i,(x,y,num,title,detail) in enumerate(stages):
        b+=platform(x,y+24,73,17,c)
        b+=R(x-59,y-23,118,50,c['paper'],6,extra=f'stroke="{c["rule"]}"')
        b+=T(x-48,y-6,num,10,c['accent'],700,font=MONO)+T(x,y+13,title,16,fg,700,'middle')
        b+=C(x+45,y-10,3.4,gr,extra=f'class="pulse" style="animation-delay:{-i*.6}s"')
        b+=T(x,y+67,detail,12,dim,500,'middle')
    b+=T(480,395,'Study roadmap · illustrative lifecycle, not a claim of production infrastructure',12,dim,400,'middle')
    write('lifecycle',theme,419,'MLOps learning map','Animated six-stage learning map: ingest, train, evaluate, serve, observe, improve. It is illustrative, not live infrastructure.',b,CSS)
