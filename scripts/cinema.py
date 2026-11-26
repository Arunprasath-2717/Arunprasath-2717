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

def timeline(theme):
    c=THEMES[theme];fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['leaf']
    b=T(28,35,'03 / ENGINEERING JOURNEY',12,ac,700,font=MONO,extra='letter-spacing="1.5"')
    b+=T(28,80,'The work behind the work.',36,fg,700,font=SERIF)
    # Three horizontal chapters with clear hierarchy and chronological order.
    chapters=[
      (28,'2024–28','FOUNDATIONS',[('B.E. Computer Science','Sri Shakthi Institute of','Engineering and Technology')]),
      (334,'2025','EXPERIENCE',[('Ascentz Technologies','Full-stack web development',''),('Pluto Academy','AI & machine learning',''),('Thiranex','Full-stack web development','')]),
      (640,'2026','MILESTONES',[('Code Rush · 2nd place','Kanam 2K26, NGP College',''),('Render Rush · event lead','Kalam 2026','')])
    ]
    b+=L('M48 122H910',c['rule'],3)
    for i,(x,year,heading,records) in enumerate(chapters):
        b+=C(x+18,122,8,ac if i==2 else gr)
        b+=C(x+18,122,13,'none',extra=f'stroke="{gr}" stroke-width="1.5" class="halo" style="animation-delay:{-i*.9}s"')
        b+=T(x,151,year,19,fg,750,font=MONO)+T(x,174,heading,11,ac,700,font=MONO,extra='letter-spacing="1"')
        for j,(title,a,d) in enumerate(records):
            y=191+j*64
            b+=R(x,y,282,56,c['paper'],4)
            b+=T(x+11,y+19,title,14,fg,700)
            b+=T(x+11,y+36,a,12,dim)
            if d:b+=T(x+11,y+50,d,12,dim)
    b+=R(28,397,894,41,c['paper'],5)
    b+=C(43,417,4,gr,extra='class="halo"')
    b+=T(57,422,'OPEN TO SOFTWARE ENGINEERING INTERNSHIPS',12,fg,700,font=MONO)
    b+=T(908,422,'BACKEND / PLATFORM / AI',11,dim,500,'end',MONO)
    write('journey',theme,455,'Engineering journey','B.E. CSE 2024–2028. Three internships in 2025. Code Rush second place and Render Rush event lead in 2026.',b,'.halo{animation:halo 5s ease-in-out infinite}@keyframes halo{50%{opacity:.32}}')

def activity(theme,data):
    c=THEMES[theme];fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['leaf']
    weeks=data['weeks'];counts=[w['count'] for w in weeks];peak=max(counts+[1]);total=sum(counts)
    b=T(28,35,'04 / BUILD HISTORY',12,ac,700,font=MONO,extra='letter-spacing="1.5"')
    b+=T(28,84,'The signal of steady work.',35,fg,700,font=SERIF)
    b+=T(932,35,data['as_of']+' UTC',12,dim,500,'end',MONO)
    for x,num,label in [(28,total,'Contributions'),(338,sum(n>0 for n in counts),'Active weeks'),(640,max(counts+[0]),'Peak week')]:
        b+=T(x,145,str(num),41,fg,750,font=MONO)+T(x,167,label,13,dim)
    # Real weekly data rendered as an illuminated equipment array. Each channel
    # has a linear bar behind a matte rack grille; no artificial events.
    b+=R(28,185,904,135,c['paper'],6)
    baseline=298;step=872/max(1,len(weeks))
    for j in range(5):
        y=baseline-j*23
        b+=L(f'M44 {y}H916',c['rule'],.8)
    for i,w in enumerate(weeks):
        x=44+i*step;n=w['count'];h=round(92*n/peak,2);bw=max(2,step-4)
        bar=R(round(x,2),203,round(bw,2),95,c['bg'],2)
        if n:bar+=R(round(x,2),round(baseline-h,2),round(bw,2),h,ac if n==peak else gr,1)
        else:bar+=R(round(x,2),baseline-1,round(bw,2),1,c['rule'])
        # Small header LED only marks latest calendar week, not fabricated live traffic.
        if i==len(weeks)-1:bar+=C(round(x+bw/2,2),195,3,ac,extra='class="last"')
        b+=G(f'<title>Week of {e(w["date"])}: {n} contributions</title>'+bar)
    b+=T(44,314,'OLDEST',9,dim,650,font=MONO)+T(916,314,'LATEST',9,dim,650,'end',MONO)
    if weeks:
        b+=T(28,343,weeks[0]['date'],11,dim,font=MONO)+T(932,343,weeks[-1]['date'],11,dim,400,'end',MONO)
    b+=T(480,366,'Weekly GitHub counts · linear height · latest week marked · six-hour refresh',12,dim,400,'middle')
    write('activity',theme,385,'GitHub build history',f'{total} contributions over {len(weeks)} weeks. Updated {data["as_of"]}. Each channel represents an actual weekly count.',b,'.last{animation:last 3s ease-in-out infinite}@keyframes last{50%{opacity:.25}}')
