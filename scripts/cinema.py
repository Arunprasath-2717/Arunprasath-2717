"""Night shift: original SVG artwork and animated editorial modules.
The scene is fictional; all contribution counts come from GitHub.
"""
import html, math, random
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]/'assets'
THEMES={
'dark':dict(bg='#151714',fg='#f1ebdb',dim='#b1b4a4',rule='#3b4338',accent='#edb273',leaf='#c1d99b',paper='#252c22',black='#111410'),
'light':dict(bg='#f6f3e9',fg='#252a21',dim='#555e50',rule='#c9cebe',accent='#92471f',leaf='#38642d',paper='#e4e8d9',black='#252a21')}
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

def hero(theme):
    # A deliberately asymmetric, low-key film frame: foreground operator, midground
    # machines, distant server corridor. No simulated statistics or random data.
    c=THEMES[theme]
    b=R(0,0,960,410,'#171a15',8)
    b+=P('M438 0H960V410H438Z','#20251d')
    b+=P('M441 0H960V252L794 202H551Z','#272d23')
    b+=P('M438 410V276L688 186L960 265V410Z','#30372b')
    b+=P('M467 410L688 186L960 336V410Z','#3b4333')
    # industrial aperture with deep perspective and warm backlight
    b+=R(672,44,253,251,'#111710',3)+R(683,55,231,231,'#62614a',2)+R(692,64,213,213,'#373e2e')
    b+=P('M692 64L777 127H829L905 64Z','#7d7958')
    b+=P('M692 277L777 197H829L905 277Z','#4b5039')
    b+=R(777,127,52,70,'#b89c62')
    b+=R(785,135,36,54,'#f0d29a')
    # distant door, rows of server equipment drawn with actual depth
    for side in [0,1]:
        for i,(x,y,w,h) in enumerate([(701,79,54,183),(752,105,31,132),(779,125,13,90)]):
            if side:x=1600-x-w
            b+=R(x,y,w,h,'#161d17')+R(x+3,y+3,w-6,h-6,'#333b2c')
            for j in range(7):
                yy=y+7+j*(h-13)/7
                b+=R(x+5,round(yy,1),w-10,max(4,(h-13)/7-3),'#20291f')
                if w>20:
                    b+=R(x+8,round(yy+2,1),w-21,2,'#555b42')
                    b+=R(x+w-9,round(yy+2,1),3,3,'#d5e1a1',extra=f'class="led" style="animation-delay:{-i*.8-j*.23-side*.4:.2f}s"')
    # steel window mullions, foreground industrial frame
    b+=R(791,55,7,230,'#292e24')+R(684,166,231,6,'#252b23')
    b+=R(664,33,269,13,'#3c4334')+R(664,288,269,11,'#171c16')
    for x in [674,920]:
        b+=R(x,46,8,242,'#444937')
    # ceiling service ducts / lamp. Soft falloff is made of flat translucent layers.
    b+=R(459,16,196,12,'#30362a')+R(459,28,196,5,'#10140f')
    for x in range(469,649,20):b+=R(x,18,2,7,'#777258')
    b+=P('M561 40H646L678 46L655 52H550Z','#77735a')
    b+=R(568,45,77,4,'#f5d6a1')
    b+=P('M568 49H645L693 275H493Z','#d0a86d','opacity=".055"')
    b+=P('M578 49H633L667 275H518Z','#e5bf82','opacity=".085"')
    # wall and equipment details, intentional restrained texture.
    for y in [77,126,175,224]:
        b+=L(f'M445 {y}H663','#31392c',1)
    b+=R(935,0,25,410,'#0e130e')
    # Desk, large terminal, side monitor, warm faces and shadow.
    b+=P('M456 295L612 255L918 283L818 329L456 328Z','#857459')
    b+=P('M456 295L818 307L918 283V301L819 341L456 321Z','#282c22')
    b+=P('M803 332H822L812 410H795Z','#10150f')
    b+=P('M481 322H502L493 410H476Z','#10150f')
    b+=P('M556 140L650 130L670 146V251L650 264L556 255Z','#10150f')
    b+=P('M556 140L650 130L668 143L575 153Z','#777359')
    b+=P('M650 130L670 146V251L650 264Z','#272e23')
    b+=R(556,143,95,112,'#68684f',5)+R(563,151,81,84,'#131d14',4)
    b+=R(567,155,73,76,'#26382a',2)
    b+=T(573,168,'arun@linux',8,'#bad19c',650,font=MONO)
    for i,s in enumerate(['$ python -m','  pytest','collecting ...','tests complete']):
        b+=T(573,181+i*10,s,7.4,'#d1ddb7',font=MONO,extra=f'class="term t{i}"')
    b+=R(573,224,5,2,'#e3cf8a',extra='class="cursor"')
    b+=R(567,241,35,3,'#2d3528')+C(638,245,2.7,'#cbd196',extra='class="led"')
    b+=P('M594 256H618L622 276H588Z','#232b21')+P('M577 276H631L641 282H567Z','#4d5240')
    # second terminal laid obliquely, rack of hardware beside it
    b+=P('M690 173L766 185V263L690 250Z','#151b14')
    b+=P('M695 177L760 188V253L695 242Z','#424c36')
    b+=P('M700 184L753 193V245L700 236Z','#202e20')
    for i in range(6):
        b+=L(f'M705 {191+i*7}l{20+(i*11)%25} 4','#809e6a',1.5)
    b+=P('M715 251L731 254L733 274L707 271Z','#252c21')
    b+=P('M650 282L724 291L696 310L618 299Z','#9a9370')
    for i in range(4):
        for j in range(11):
            x=650+j*5-i*6;y=286+j*.6+i*3
            b+=P(f'M{x:.1f} {y:.1f}l4 .5 -4 2 -4 -.5Z','#292f23')
    # mouse, cable and desk mug, all objects with physical silhouettes.
    b+=P('M743 294q12 -5 17 5l-8 9q-12 2 -15 -5Z','#252d22')+L('M749 293Q746 284 757 279','#1a2018',2)
    b+=R(854,258,19,25,'#a17e50',3)+L('M873 262q17 -1 7 13h-7','#a17e50',3)
    b+=R(858,260,11,3,'#30251b')
    # backlit seated operator, hand on keyboard; intentionally anonymous silhouette.
    b+=P('M768 410L748 376L756 347L789 336L838 348L859 385L856 410Z','#0d120e')
    b+=P('M778 324Q766 305 771 285L785 269L813 268L829 284L831 310L818 331Z','#141a13')
    b+=P('M780 272L797 265L815 273L822 291L812 302L814 316L794 327L778 312L774 292Z','#242c21')
    b+=P('M776 280Q782 265 801 265Q823 268 829 286L820 295L805 287L787 289L777 302Z','#101710')
    b+=P('M780 323L795 329L817 322L830 346L852 377L837 410H752L749 374Z','#1b231a')
    b+=P('M780 328L754 344L737 367L704 356L693 344L680 350L687 366L741 387L768 369L789 347Z','#222b1e')
    b+=P('M693 344L682 340L669 343L668 348L683 355L691 354Z','#77684a')
    b+=P('M792 335L817 330L832 345L846 380L840 407H792Z','#374333')
    b+=P('M823 337L840 348L854 387L851 410H837L831 369Z','#404b34')
    # foreground chair, frame, and a few drifting dust motes.
    b+=P('M755 377Q783 365 829 376L841 410H764Z','#10170f')
    b+=L('M765 387Q796 374 827 387','#3a4431',3)
    rng=random.Random(2717)
    for i in range(24):
        x=rng.randrange(482,933);y=rng.randrange(49,277)
        b+=C(x,y,.9 if i%3 else 1.5,'#dec18a',extra=f'opacity=".20" class="dust" style="animation-delay:{-i*.63:.2f}s"')
    # title is independent of scene, so it stays legible at GitHub image width.
    b+=P('M0 0H432V410H0Z','#171a15')
    b+=P('M432 0H449L435 410H432Z','#303a2a')
    b+=R(34,36,8,8,'#f0b777')+T(52,44,'AP / 2717',13,'#f0b777',700,font=MONO,extra='letter-spacing="3"')
    b+=T(34,91,'N I G H T   S H I F T',13,'#b8c7a4',600,font=MONO)
    b+=T(31,158,'Arun',67,'#f3ecda',700,font=SERIF)
    b+=T(31,222,'Prasath',67,'#f3ecda',700,font=SERIF)
    b+=R(35,245,42,3,'#d5a269')
    b+=T(35,281,'Backend engineering',23,'#f3ecda',550)
    b+=T(35,310,'Applied AI / MLOps',23,'#f3ecda',550)
    b+=T(35,344,'Linux · Cloud · ML lifecycle',14,'#b9c5ac',font=MONO)
    b+=T(35,379,'CSE student  /  India',13,'#9aa793',font=MONO)
    css='.led{animation:led 3.1s ease-in-out infinite}.cursor{animation:blink 1.2s step-end infinite}.dust{animation:dust 8s ease-in-out infinite}.term{animation:terminal 10s infinite}.t0{animation-delay:-2s}.t1{animation-delay:-1s}.t2{animation-delay:0s}.t3{animation-delay:1s}@keyframes led{0%,100%{opacity:1}35%{opacity:.24}65%{opacity:.9}}@keyframes blink{50%{opacity:0}}@keyframes dust{50%{transform:translate(3px,-7px);opacity:.55}}@keyframes terminal{0%,12%{opacity:.25}25%,90%{opacity:1}100%{opacity:.25}}'
    write('identity',theme,410,'Arun Prasath — Night Shift','An illustrated night-shift computer lab with a seated engineer, Linux terminal and server corridor. Fictional scene; terminal output is illustrative. Backend, AI and MLOps.',b,css)

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
    b=T(30,36,'THE TOOLCHAIN',13,ac,700,font=MONO,extra='letter-spacing="2"')
    b+=T(30,83,'From shell to service.',38,fg,700,font=SERIF)
    b+=T(930,36,'CAPABILITIES / 2717',11,dim,600,'end',MONO)
    groups=[
        ('01','Languages','Python · TypeScript · Java','JavaScript · C / C++ · SQL'),
        ('02','Backend','FastAPI · Flask · Node.js','REST APIs · SQLAlchemy · JWT'),
        ('03','Applied AI','PyTorch · Transformers · spaCy','scikit-learn · BM25 · evaluation'),
        ('04','Data systems','PostgreSQL · PostGIS · Redis','SQLite · MongoDB · Supabase'),
        ('05','Linux & delivery','Linux · Docker · Git · Actions','CI/CD · Pytest · Ruff · Mypy'),
        ('06','Frontend','React · Next.js · Vite','HTML / CSS · WebSockets')]
    for i,(n,title,a,d) in enumerate(groups):
        x=30+(i%2)*460;y=112+(i//2)*91
        b+=L(f'M{x} {y}H{x+440}',c['rule'])
        b+=T(x,y+24,n,12,gr,700,font=MONO)+T(x+35,y+25,title,21,fg,700)
        b+=T(x+35,y+50,a,15,fg)+T(x+35,y+70,d,14,dim)
    b+=R(30,390,900,59,c['paper'],5)
    b+=T(45,411,'LEARNING NEXT',11,ac,700,font=MONO)
    b+=T(45,432,'Kubernetes · Terraform · Model registry · Experiment tracking · Observability',15,fg)
    b+=R(30,464,900,2,c['rule'])+R(30,464,54,2,gr,extra='class="trace"')
    write('toolchain',theme,485,'Engineering skills','Languages, backend, applied AI, data systems, Linux and delivery, and frontend. Learning next: Kubernetes, Terraform, model registry, experiment tracking and observability.',b,'.trace{animation:trace 14s ease-in-out infinite}@keyframes trace{0%,100%{transform:translateX(0)}50%{transform:translateX(846px)}}')

def timeline(theme):
    c=THEMES[theme];fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['leaf']
    b=T(30,37,'THE JOURNEY',13,ac,700,font=MONO,extra='letter-spacing="2"')
    b+=T(30,79,'Learning by building.',34,fg,700,font=SERIF)
    b+=L('M65 113V282',c['rule'],3)
    records=[('2024–28','B.E. Computer Science & Engineering','Sri Shakthi Institute of Engineering and Technology'),('2025','Three internships','Ascentz Technologies · Pluto Academy · Thiranex'),('2026','Code Rush — 2nd place','Kanam 2K26, NGP College'),('2026','Render Rush — event lead','Kalam 2026')]
    for i,(year,heading,detail) in enumerate(records):
        y=119+i*54
        b+=C(65,y,6,gr)+T(85,y+4,year,13,ac,700,font=MONO)+T(209,y+3,heading,18,fg,650)+T(209,y+24,detail,13,dim)
    b+=T(30,338,'OPEN TO SOFTWARE ENGINEERING INTERNSHIPS',12,gr,650,font=MONO)
    write('journey',theme,362,'Education and experience','B.E. CSE 2024–2028. Three internships in 2025. Code Rush second place and Render Rush event lead in 2026.',b)

def activity(theme,data):
    c=THEMES[theme];fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['leaf']
    weeks=data['weeks'];counts=[w['count'] for w in weeks];peak=max(counts+[1]);total=sum(counts)
    b=T(30,35,'THE DEVELOPMENT RECORD',13,ac,700,font=MONO,extra='letter-spacing="1.4"')
    b+=T(30,92,str(total),52,fg,750)+T(30,113,'GitHub contributions',13,dim)
    b+=T(276,92,str(sum(n>0 for n in counts)),44,fg,700)+T(276,113,'Active weeks',13,dim)
    b+=T(455,92,str(max(counts+[0])),44,fg,700)+T(455,113,'Peak week',13,dim)
    b+=T(930,76,data['as_of']+' UTC',13,fg,650,'end',MONO)+T(930,101,'Last '+str(len(weeks))+' calendar weeks',12,dim,400,'end')
    b+=R(30,136,900,112,c['paper'],3)
    for i in range(5):b+=L(f'M42 {154+i*21}H918',c['rule'],.7)
    step=876/max(1,len(weeks))
    for i,w in enumerate(weeks):
        x=42+i*step;n=w['count'];h=round(81*n/peak,2)
        b+=G(f'<title>Week of {e(w["date"])}: {n} contributions</title>'+R(round(x,2),round(237-h,2),round(step-4,2),max(1,h),ac if n==peak and n else gr if n else c['rule'],1,extra='class="latest"' if i==len(weeks)-1 else ''))
    if weeks:
        b+=T(30,272,weeks[0]['date'],11,dim,font=MONO)+T(930,272,weeks[-1]['date'],11,dim,400,'end',MONO)
    b+=T(480,297,'Actual weekly counts · linear scale · refreshed every six hours',12,dim,400,'middle')
    write('activity',theme,316,'GitHub development record',f'{total} contributions over {len(weeks)} weeks. Updated {data["as_of"]}.',b,'.latest{animation:latest 4s ease-in-out infinite}@keyframes latest{50%{opacity:.5}}')
