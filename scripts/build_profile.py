"""AP/2717 engineering dossier. Native SVG, two themes, measured data only."""
from __future__ import annotations
import argparse, datetime as dt, html, json, os, pathlib, urllib.request
import xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
DATA=ROOT/'data'
LOGIN='Arunprasath-2717'
PALETTES={
    'dark': dict(bg='#141613', panel='#20231e', fg='#f0eee4', dim='#a8afa0', line='#41483b', accent='#ef9a67', green='#b8d68d', muted='#333b30', inverse='#141613'),
    'light':dict(bg='#f3f1e9', panel='#e5e3d8', fg='#22251f', dim='#525b4e', line='#b9bfb0', accent='#9f4321', green='#426729', muted='#d3d8ca', inverse='#f3f1e9')
}
MONO='ui-monospace, SFMono-Regular, Consolas, Liberation Mono, monospace'
SANS='system-ui, -apple-system, Segoe UI, sans-serif'
def esc(s):return html.escape(str(s),quote=True)
def text(x,y,s,size,fill,weight=400,anchor='start',font=SANS,extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-family="{font}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'
def rect(x,y,w,h,fill,rx=0,stroke='none'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'
def line(x,y,X,Y,fill,w=1,extra=''):
    return f'<path d="M{x} {y}L{X} {Y}" fill="none" stroke="{fill}" stroke-width="{w}" {extra}/>'
def svg(name,theme,h,title,desc,body):
    c=PALETTES[theme]
    style='<style>.signal{animation:signal 3s linear infinite}@keyframes signal{to{stroke-dashoffset:-30}}@media(prefers-reduced-motion:reduce){.signal{animation:none}}</style>'
    out=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 {h}" width="960" height="{h}" role="img" aria-labelledby="t d"><title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>{style}{rect(0,0,960,h,c["bg"],10)}{body}</svg>\n'
    ET.fromstring(out)
    p=ASSETS/f'{name}-{theme}.svg'
    p.write_text(out,encoding='utf-8')

def hero(theme,profile):
    c=PALETTES[theme]; fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['green']
    b=rect(24,24,6,140,ac,2)
    b+=text(45,40,'AP / 2717',13,ac,700,font=MONO,extra='letter-spacing="2"')
    b+=text(45,98,profile['name'],57,fg,750)
    b+=text(47,132,'Backend engineering  /  Applied AI  /  MLOps',20,fg,500)
    b+=text(47,159,'Computer science student  ·  India',14,dim)
    # A compact, legible command transcript, not a simulated operational status.
    b+=rect(660,25,274,139,c['panel'],7)
    b+=text(676,49,'$ cat focus.txt',13,ac,700,font=MONO)
    for i,(key,val) in enumerate([('01','Linux & APIs'),('02','Cloud & delivery'),('03','ML lifecycle')]):
        y=77+i*26
        b+=text(676,y,key,12,dim,font=MONO)+text(709,y,val,15,fg,600)
    b+=line(45,184,934,184,c['line'])
    b+=text(45,207,'From noisy input to decisions that can be traced.',15,dim)
    b+=text(934,207,'SYSTEMS / 2026',12,gr,650,'end',MONO)
    svg('identity',theme,228,'Arun Prasath',profile['role']+'. Linux and APIs, cloud delivery and machine learning lifecycle.',b)

def project(theme,p,index):
    c=PALETTES[theme]; fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['green']
    b=rect(22,20,4,135,ac,2)
    b+=text(40,36,f'0{index}  /  {p["category"]}',12,ac,700,font=MONO)
    b+=text(40,73,p['name'],33,fg,730)
    for i,s in enumerate(p['summary']):b+=text(40,99+i*21,s,15,dim)
    b+=text(40,149,p['stack'],12,fg,500,font=MONO)
    b+=rect(475,22,462,136,c['panel'],6)
    b+=text(491,43,'SYSTEM FLOW',11,dim,650,font=MONO,extra='letter-spacing="1"')
    def node(x,y,w,h,label,color):
        return rect(x,y,w,h,c['bg'],4,c['line'])+text(x+w/2,y+h/2+5,label,12,color,650,'middle')
    if p['slug']=='verifai':
        # Claims and evidence meet at independent judges; no claim of factual certainty.
        b+=line(585,82,610,82,ac,2)+line(710,82,746,82,ac,2)
        b+=line(660,111,660,102,gr,1.5,'stroke-dasharray="4 3"')+line(710,123,788,123,gr,1.5)+line(788,123,788,102,gr,1.5)
        b+=line(830,82,852,82,gr,2)
        b+=node(489,62,96,40,'AI answer',fg)+node(610,62,100,40,'Claims',fg)
        b+=node(746,62,84,40,'Judges',ac)+node(852,62,69,40,'Verdict',gr)
        b+=node(610,111,100,24,'Evidence',gr)
        b+=text(921,142,'Unknown is a valid result',11,dim,400,'end')
    else:
        # News sources converge into ingestion, then an NLP pipeline branches to outputs.
        for y,label in [(60,'APIs'),(94,'RSS')]:
            b+=node(489,y,64,26,label,fg)
            b+=line(553,y+13,573,y+13,ac,1.5)+line(573,y+13,573,90,ac,1.5)
        b+=line(573,90,586,90,ac,2)+line(670,90,687,90,ac,2)
        b+=node(586,70,84,40,'Queue',fg)+node(687,70,85,40,'NLP',ac)
        b+=line(772,90,793,90,gr,2)
        for y,label in [(53,'Events'),(85,'Sentiment'),(117,'Entities')]:
            b+=line(793,90,793,y+12,gr,1.5)+line(793,y+12,809,y+12,gr,1.5)
            b+=node(809,y,112,24,label,gr)
        b+=text(489,142,'Deduplicate before analysis',11,dim)
    # A small moving underline signals sequence, not measured runtime.
    b+=line(489,151,921,151,c['line'],1)
    b+=line(489,151,921,151,gr,1.5,'stroke-dasharray="3 27" class="signal"')
    svg(p['slug'],theme,178,p['name'],'. '.join(p['summary'])+'. '+p['caption']+'.',b)

def toolkit(theme):
    c=PALETTES[theme]; fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['green']
    b=text(27,34,'TOOLCHAIN',13,ac,700,font=MONO,extra='letter-spacing="1"')
    b+=text(934,34,'TOOLS I USE / AREAS I STUDY',11,dim,500,'end',MONO)
    cols=[
        ('01','Backend','Python · FastAPI · SQLAlchemy','PostgreSQL · Redis · REST APIs'),
        ('02','Applied AI','PyTorch · Transformers · spaCy','scikit-learn · retrieval · evaluation'),
        ('03','Delivery','Linux · Docker · Git · Actions','Pytest · Ruff · Mypy')
    ]
    for i,(n,title,a,d) in enumerate(cols):
        x=27+i*310
        b+=line(x,51,x+286,51,c['line'])
        b+=text(x,78,n,12,gr,700,font=MONO)
        b+=text(x+29,79,title,23,fg,700)
        b+=text(x,109,a,14,fg)
        b+=text(x,132,d,14,dim)
    b+=rect(27,151,906,42,c['panel'],5)
    b+=text(41,177,'CURRENTLY LEARNING',11,ac,700,font=MONO)
    b+=text(217,178,'Model versioning   /   Kubernetes   /   Terraform   /   Observability',14,fg)
    svg('toolchain',theme,212,'Engineering toolchain','Backend, applied AI, delivery, and current learning topics.',b)

def activity(theme,data):
    c=PALETTES[theme]; fg,dim,ac,gr=c['fg'],c['dim'],c['accent'],c['green']
    weeks=data['weeks']; counts=[w['count'] for w in weeks]; peak=max(counts+[1]); total=sum(counts); active=sum(n>0 for n in counts)
    b=text(26,33,'DEVELOPMENT RECORD',12,ac,700,font=MONO,extra='letter-spacing="1"')
    b+=text(934,33,'GITHUB / WEEKLY CONTRIBUTIONS',11,dim,500,'end',MONO)
    for x,n,label in [(26,total,'Contributions'),(242,active,'Active weeks'),(451,max(counts+[0]),'Peak week')]:
        b+=text(x,83,n,40,fg,730)
        b+=text(x,103,label,13,dim)
    b+=text(934,79,data['as_of']+' UTC',13,fg,600,'end',MONO)
    b+=text(934,102,'Last '+str(len(weeks))+' calendar weeks',12,dim,400,'end')
    # A precise, zero-baseline linear weekly bar chart; no fake telemetry.
    b+=line(26,208,934,208,c['line'])
    b+=line(26,121,934,121,c['line'],1,'stroke-dasharray="3 6"')
    step=908/max(1,len(weeks))
    for i,w in enumerate(weeks):
        x=26+i*step; n=w['count']; h=round(87*n/peak,2)
        color=ac if n==peak and n else gr
        b+=f'<g><title>Week of {esc(w["date"])}: {n} contributions</title>'
        b+=rect(round(x,2),round(208-h,2),round(step-3,2),max(1,h),color if n else c['muted'],1)+'</g>'
    if weeks:
        b+=text(26,231,weeks[0]['date'],11,dim,font=MONO)
        b+=text(934,231,weeks[-1]['date'],11,dim,400,'end',MONO)
    svg('activity',theme,248,'GitHub development record',f'{total} contributions across {len(weeks)} weeks. {active} active weeks. Peak {max(counts+[0])}. Snapshot {data["as_of"]}.',b)

def fetch(token):
    q='query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}'
    req=urllib.request.Request('https://api.github.com/graphql',data=json.dumps({'query':q,'variables':{'login':LOGIN}}).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','User-Agent':'AP2717-profile'})
    with urllib.request.urlopen(req,timeout=30) as r: data=json.load(r)
    if data.get('errors'): raise ValueError('GitHub GraphQL returned errors')
    weeks=data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    out=[{'date':w['contributionDays'][0]['date'],'count':sum(d['contributionCount'] for d in w['contributionDays'])} for w in weeks if w['contributionDays']]
    if not out: raise ValueError('Empty calendar; preserve published snapshot')
    return {'as_of':dt.datetime.now(dt.timezone.utc).date().isoformat(),'weeks':sorted(out,key=lambda w:w['date'])[-53:]}

def validate(data):
    assert 1<=len(data['weeks'])<=53
    dates=[w['date'] for w in data['weeks']]
    assert dates==sorted(set(dates))
    dt.date.fromisoformat(data['as_of'])
    for w in data['weeks']:
        dt.date.fromisoformat(w['date']); assert type(w['count']) is int and w['count']>=0

def main():
    p=argparse.ArgumentParser();p.add_argument('--live',action='store_true');a=p.parse_args()
    profile=json.loads((DATA/'profile.json').read_text())
    source=DATA/'contributions.json'
    if a.live:
        token=os.environ.get('GH_TOKEN')
        if not token: raise SystemExit('GH_TOKEN is required')
        data=fetch(token)
    else: data=json.loads(source.read_text())
    validate(data);ASSETS.mkdir(exist_ok=True)
    for theme in PALETTES:
        hero(theme,profile)
        for i,p in enumerate(profile['projects'],1): project(theme,p,i)
        toolkit(theme);activity(theme,data)
    if a.live: source.write_text(json.dumps(data,indent=2)+'\n')
    print('Generated 10 SVGs;',sum(w['count'] for w in data['weeks']),'contributions')
if __name__=='__main__':main()
