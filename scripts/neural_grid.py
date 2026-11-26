"""AP/2717: a contribution-driven isometric compute fabric.
Conceptual infrastructure artwork, not an operational cluster status monitor.
"""
import math
import render_profile as r

CY, MAG, GOLD, INK, MUT = r.C, r.M, r.Y, r.BG, r.S
def text(x,y,s,size=14,color=r.T,weight=400,anchor='start'):
    return r.txt(x,y,s,size,color,weight,anchor)
def path(d,fill='none',stroke=CY,extra=''):
    return r.poly(d,fill,stroke,extra)
def wire(d,color=CY,delay=0):
    return path(d,'none','#294b60','stroke-width="2"')+path(d,'none',color,f'stroke-width="2" stroke-dasharray="5 19" class="flow" style="animation-delay:{delay}s"')
STYLE = '''<style>
.flow{animation:transit 2.4s linear infinite}
.beacon{animation:beacon 3.2s ease-in-out infinite}
@keyframes transit{to{stroke-dashoffset:-48}}
@keyframes beacon{50%{opacity:.28}}
@media(prefers-reduced-motion:reduce){.flow,.beacon{animation:none!important}}
</style>'''

def weekly(data):
    cal=data.get('calendar')
    if not cal: return []
    return [(w['contributionDays'][0]['date'],sum(d['contributionCount'] for d in w['contributionDays']))
            for w in cal.get('weeks',[]) if w.get('contributionDays')][-53:]

def city(data):
    weeks=weekly(data); peak=max([n for _,n in weeks]+[1])
    b=STYLE+r.section('00','NEURAL GRID / AP-2717','GENERATIVE CONTRIBUTION FABRIC')
    b+=text(34,81,'ONE WEEK. ONE COMPUTE NODE.',16,CY,700)
    b+=text(34,104,'A digital twin of my GitHub contribution rhythm.',13,MUT)
    b+=text(926,81,f'{sum(n for _,n in weeks)} CONTRIBUTIONS' if weeks else 'AWAITING CALENDAR',16,GOLD,700,'end')
    b+=text(926,104,f'{len(weeks)} WEEK NODES / UTC {data["as_of"][:10]}' if weeks else 'NO SYNTHETIC COUNTS',12,MUT,400,'end')
    def iso(c,j): return 482+(c-j)*48, 256+(c+j)*19
    def pt(c,j): return '%g %g'%iso(c,j)
    b+=path('M'+pt(-.7,-.7)+'L'+pt(7.7,-.7)+'L'+pt(7.7,6.7)+'L'+pt(-.7,6.7)+'Z','#0a1726','#39576a','stroke-width="2"')
    for c in range(9):
        b+=path('M'+pt(c-.5,-.5)+'L'+pt(c-.5,6.5),'none','#1f3546')
    for j in range(8):
        b+=path('M'+pt(-.5,j-.5)+'L'+pt(7.5,j-.5),'none','#1f3546')
    # Isometric routes have constant animation speed; they are symbolic, not live traffic.
    b+=wire('M'+pt(-.45,1.5)+'L'+pt(7.45,1.5),MAG)
    b+=wire('M'+pt(3.5,-.45)+'L'+pt(3.5,6.45),CY,-1)
    b+=wire('M'+pt(-.45,4.5)+'L'+pt(7.45,4.5),GOLD,-.7)
    for i,(date,n) in sorted(enumerate(weeks),key=lambda t:(t[0]%8+t[0]//8,t[0]%8)):
        c,j=i%8,i//8; x,y=iso(c,j); h=8+round(112*math.sqrt(n/peak))
        color=CY if n else '#476273'
        if n==peak and n>0: color=GOLD
        elif n>=peak*.65 and n>0: color=MAG
        # Four faces and horizontal rack lights in perspective.
        b+=f'<g><title>Week of {r.esc(date)}: {n} contributions</title>'
        b+=path(f'M{x-19} {y-8}l19 8v{-h}l-19 -8Z','#142d43',color,'stroke-width=".7"')
        b+=path(f'M{x} {y}l19 -8v{-h}l-19 8Z','#0d1c30',color,'stroke-width=".7"')
        b+=path(f'M{x} {y-h-16}l19 8 -19 8 -19 -8Z','#235066' if n else '#1a2c3b',color,'stroke-width=".9"')
        for z in range(13,h,13):
            b+=path(f'M{x-15} {y-z-6}l11 5','none',color,'opacity=".8" stroke-width="1.2"')
        if n:
            b+=r.circle(x,y-h-8,2.4,color,extra=f'class="beacon" style="animation-delay:{-i*.13:.2f}s"')
        b+='</g>'
    if not weeks:
        b+=text(482,315,'CALENDAR DATA NOT AVAILABLE',17,GOLD,700,'middle')
        b+=text(482,342,'The grid populates after a successful GitHub refresh.',13,MUT,400,'middle')
    b+=text(34,153,'01 / GRID',12,CY,700)+text(34,173,'8 nodes per row',12,MUT)
    b+=text(926,431,'02 / SCALE',12,MAG,700,'end')+text(926,451,'Weekly counts',12,MUT,400,'end')
    b+=r.line(32,520,928,520)
    for x,color,label in [(34,'#476273','Zero activity'),(224,CY,'Active week'),(414,MAG,'High activity'),(624,GOLD,'Peak week')]:
        b+=r.rect(x,540,11,11,color,rx=2)+text(x+19,550,label,12,MUT)
    b+=text(34,580,'Height = normalized weekly contributions (square-root scale). Animated routes are conceptual.',12,MUT)
    r.svg('neural-grid.svg',960,600,'AP/2717 neural compute fabric',
          'Isometric server nodes encode weekly GitHub contributions; height maps to contribution count. No synthetic activity.',b)

def node(x,y,w,h,label,color=CY,sub=''):
    b=r.rect(x,y,w,h,'#101e30',color,5)+text(x+w/2,y+24,label,13,color,700,'middle')
    if sub: b+=text(x+w/2,y+42,sub,10,MUT,400,'middle')
    return b

def card(slug,number,title,subtitle,description,stack,color,art):
    b=STYLE+text(32,32,f'AP / 2717   //   SYSTEM {number}',12,color,700)
    b+=text(32,74,title,34,r.T,750)+text(34,106,subtitle,15,color,700)
    for i,line in enumerate(description): b+=text(34,142+i*23,line,15,MUT)
    b+=text(34,228,stack,12,r.T,600)+text(928,228,'REPOSITORY  ↗',12,color,700,'end')
    b+=r.line(510,31,510,205)+art
    r.svg(slug+'.svg',960,250,title,subtitle+'. '+' '.join(description)+' Diagram is conceptual.',b)

def projects():
    # Each composition expresses the actual project's public README, not an invented benchmark.
    a=wire('M621 67H658V112H691',CY)+wire('M621 115H691',CY,-.6)+wire('M621 164H658V112H691',CY,-1.2)+wire('M789 112H817',MAG)
    for y,label in [(46,'FEEDS'),(94,'EVENTS'),(143,'SIGNALS')]: a+=node(534,y,87,41,label,CY)
    a+=node(691,84,98,56,'NLP',MAG,'analyze')+node(817,84,111,56,'INSIGHTS',GOLD,'correlate')
    card('system-voiloracle','01','VOILORACLE','NEWS INTELLIGENCE',['Transform multi-source news into','searchable event and sentiment insights.'],'PYTHON  /  NLP  /  DATA PIPELINES',CY,a)
    a=wire('M628 111H660',MAG)+wire('M770 111H803V65H825',CY)+wire('M770 111H825',CY,-.6)+wire('M770 111H803V164H825',GOLD,-1)
    a+=node(534,85,94,54,'MODELS',MAG,'answers')+node(660,85,110,54,'CLAIMS',CY,'extract')
    for y,t,c in [(44,'EVIDENCE',CY),(91,'CONFLICT',MAG),(143,'AUDIT',GOLD)]: a+=node(825,y,103,41,t,c)
    card('system-verifai','02','VerifAI','EVIDENCE-FIRST AI',['Compare model answers, inspect claims','and retain a verification audit trail.'],'FASTAPI  /  REACT  /  POSTGRESQL',MAG,a)
    a=wire('M627 112H656',GOLD)+wire('M756 112H786V58H810',CY)+wire('M756 112H810',MAG,-.8)+wire('M756 112H786V166H810',GOLD,-1.2)
    a+=node(534,85,93,54,'CLIENT',GOLD,'storage API')+node(656,85,100,54,'ROUTER',CY,'select')
    for y,t,c in [(37,'CLOUD A',CY),(91,'CLOUD B',MAG),(145,'CLOUD C',GOLD)]: a+=node(810,y,118,42,t,c)
    card('system-nexus','03','NexusCloud-Orchestra','MULTI-CLOUD STORAGE',['Unified API and storage routing across','multiple cloud providers.'],'FASTAPI  /  REDIS  /  POSTGRESQL',GOLD,a)
    a=wire('M664 106H699',CY)+wire('M805 106H824V64H835',MAG)+wire('M805 106H824V158H835',GOLD,-1)
    for d in ['M535 64L585 49L610 86L558 108Z','M585 49L649 61L640 108L610 86Z','M558 108L610 86L640 108L602 160L542 145Z','M640 108L664 151L602 160Z']:
        a+=path(d,'#123046',CY,'stroke-width="1.5"')
    a+=node(699,79,106,55,'POSTGIS',CY,'validate')+node(835,43,93,42,'AUDIT',MAG)+node(835,137,93,42,'EXPORT',GOLD)
    card('system-cadastra','04','CadastraVision','GEOSPATIAL SYSTEMS',['Parcel validation, spatial records,','tamper-evident audits and exports.'],'FASTAPI  /  POSTGIS  /  REACT',CY,a)
    a=wire('M642 112H672',MAG)+wire('M782 112H814',CY)
    a+=node(534,85,108,55,'SUBMIT',MAG,'students')+node(672,85,110,55,'REVIEW',CY,'staff')+node(814,85,114,55,'RECORD',GOLD,'evaluate')
    card('system-projexa','05','Projexa','ACADEMIC WORKFLOW',['Project submissions, periodic updates','and staff evaluation workflows.'],'WEB APPLICATION  /  DATA WORKFLOWS',MAG,a)
    a=wire('M620 69H668V112H702',CY)+wire('M620 158H668V112H702',MAG,-1)+wire('M808 112H835',GOLD)
    a+=node(534,48,86,42,'CODE',CY)+node(534,137,86,42,'WORK',MAG)+node(702,85,106,55,'BUILD',CY,'web interface')+node(835,85,93,55,'SITE',GOLD,'portfolio')
    card('system-portfolio','06','Portfolio','ENGINEERING IDENTITY',['Technical work, project narratives','and the personal engineering website.'],'TYPESCRIPT  /  WEB ENGINEERING',GOLD,a)

def render(data):
    city(data)
    projects()
