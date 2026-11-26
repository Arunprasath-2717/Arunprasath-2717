#!/usr/bin/env python3
"""AP/2717 profile renderer. Stdlib only; public GitHub data, no secrets in SVGs."""
from __future__ import annotations
import argparse, datetime as dt, hashlib, html, json, os, pathlib, sys, urllib.request, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
LOGIN = 'Arunprasath-2717'
C = '#50f5e5'; M = '#fa72c9'; Y = '#f9cd78'; T = '#e8f3fa'; S = '#98afc6'; BG = '#080e19'; LINE = '#26394a'
MONO = 'ui-monospace, SFMono-Regular, Consolas, Liberation Mono, monospace'
SANS = 'system-ui, -apple-system, Segoe UI, sans-serif'

def esc(s): return html.escape(str(s), quote=True)
def txt(x,y,s,size=15,color=T,weight=400,anchor='start',family=MONO,extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-family="{family}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'
def line(x,y,X,Y,col=LINE,sw=1,extra=''):
    return f'<path d="M{x} {y}L{X} {Y}" fill="none" stroke="{col}" stroke-width="{sw}" {extra}/>'
def rect(x,y,w,h,fill='none',stroke='none',rx=0,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" {extra}/>'
def circle(x,y,r,fill='none',stroke='none',extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" {extra}/>'
def poly(d,fill='none',stroke=C,extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-linejoin="round" {extra}/>'
def cut(s,n): return s if len(s)<=n else s[:n-1]+'…'
def svg(name,w,h,title,desc,body):
    defs = '''<defs><linearGradient id="surface" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#101e30"/><stop offset=".48" stop-color="#080e19"/><stop offset="1" stop-color="#181026"/></linearGradient><linearGradient id="beam"><stop stop-color="#50f5e5" stop-opacity="0"/><stop offset=".5" stop-color="#50f5e5"/><stop offset="1" stop-color="#fa72c9" stop-opacity="0"/></linearGradient><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#5d9aaa" stroke-opacity=".08"/></pattern><radialGradient id="core"><stop stop-color="#50f5e5" stop-opacity=".25"/><stop offset="1" stop-color="#50f5e5" stop-opacity="0"/></radialGradient></defs><style>.orbit{transform-box:fill-box;transform-origin:center;animation:orbit 28s linear infinite}.pulse{animation:pulse 3.8s ease-in-out infinite}.scan{animation:scan 7s linear infinite}@keyframes orbit{to{transform:rotate(360deg)}}@keyframes pulse{50%{opacity:.28}}@keyframes scan{0%{opacity:0;transform:translateY(0)}15%{opacity:.5}85%{opacity:.5}100%{opacity:0;transform:translateY(115px)}}@media(prefers-reduced-motion:reduce){.orbit,.pulse,.scan{animation:none}}</style>'''
    if w==960:
        bg=rect(0,0,w,h,BG)+poly(f'M1 1H{w-23}L{w-1} 23V{h-1}H23L1 {h-23}Z','url(#surface)',LINE)+rect(2,2,w-4,h-4,'url(#grid)')+poly(f'M2 36V2H82 M{w-82} {h-2}H{w-2}V{h-36}', 'none', C, 'stroke-width="2"')
    else: bg=rect(0,0,w,h,BG,LINE,9)
    out=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title><desc id="desc">{esc(desc)}</desc>{defs}{bg}{body}</svg>\n'
    ASSETS.mkdir(parents=True,exist_ok=True)
    (ASSETS/name).write_text(out,encoding='utf-8')

def section(k,label,sub):
    return txt(32,34,k,15,C,700)+txt(86,35,label,23,T,750,family=SANS)+txt(928,34,sub,12,S,anchor='end')+line(32,49,928,49)

def hero():
    b=txt(34,38,'AP / 2717     IDENTITY INTERFACE',14,C,700)+txt(925,38,'SYSTEM DESIGN / INDIA',12,S,anchor='end')+line(34,54,925,54)
    b+=txt(37,91,'HELLO, WORLD. I AM',17,M,700)+txt(33,154,'ARUN PRASATH',61,T,800,family=SANS)+rect(36,168,570,2,'url(#beam)')
    b+=txt(37,200,'MLOps  /  AI SYSTEMS  /  BACKEND',23,C,700)+txt(38,229,'Engineering intelligence that can be shipped.',18,T,family=SANS)+txt(38,254,'From experiments to reliable services.',17,S,family=SANS)
    b+=rect(34,277,590,42,'#0d1929',LINE,5)+circle(52,298,5,C,extra='class="pulse"')+txt(67,303,'CSE STUDENT  //  BUILD • DEPLOY • OBSERVE',14,T,600)
    # One-of-a-kind angular AP mark, orbital neural paths and 2717 fingerprint
    b+=circle(779,180,133,'url(#core)')+circle(779,180,112,'none',LINE)+circle(779,180,91,'none','#40606e',extra='stroke-dasharray="3 9"')
    b+='<g class="orbit">'+circle(779,180,121,'none',C,extra='stroke-dasharray="42 718" stroke-width="2"')+circle(779,180,103,'none',M,extra='stroke-dasharray="22 46 8 571" stroke-width="2"')+'</g>'
    b+=poly('M706 212L743 130L778 212M723 179H760M786 212V130H827L848 151L827 174H786','none',T,'stroke-width="8" stroke-linecap="square"')+poly('M700 229H843L860 211M700 229L684 212','none',C,'stroke-width="2"')
    for a,x,y in [('01',687,107),('10',860,110),('11',867,246),('00',691,252)]: b+=circle(x,y,3,M)+txt(x+8,y-7,a,10,S)
    b+=txt(779,278,'AP-2717',15,Y,700,'middle')+txt(779,302,'SIGNATURE NODE',11,S,400,'middle')
    bits=hashlib.sha256(LOGIN.encode()).hexdigest()[:32]
    for i,k in enumerate(bits): b+=rect(36+i*27,338,4+(int(k,16)%5)*3,8,C if i%5 else M,extra='opacity=".65"')
    svg('identity.svg',960,362,'Arun Prasath — AP/2717','Computer Science and Engineering student focused on MLOps, AI systems and backend. Custom AP monogram and neon circuit identity.',b)

def pipeline():
    b=section('01','THE INTELLIGENCE PIPELINE','ARCHITECTURE / LEARNING FOCUS')
    nodes=[('01','INGEST','Data + validation'),('02','TRAIN','ML + evaluation'),('03','REGISTER','Version + track'),('04','SERVE','API + container'),('05','OBSERVE','Metrics + feedback')]
    for i,(n,title,sub) in enumerate(nodes):
        x=32+i*181
        b+=rect(x,81,165,106,'#101d2d',LINE,7)+rect(x,81,165,3,C if i%2==0 else M)+txt(x+12,108,n,12,C,700)+txt(x+12,140,title,17,T,700)+txt(x+12,163,sub,12,S)
        if i<4: b+=poly(f'M{x+168} 134h10m-4 -4l4 4-4 4','none',C)
    b+=poly('M839 188V217H113V190M109 195L113 190L117 195','none',M,'stroke-dasharray="5 5" stroke-width="1.5"')+rect(346,206,268,22,BG)+txt(480,221,'CONTINUOUS IMPROVEMENT',12,M,700,'middle')
    b+=txt(33,261,'OPERATING PRINCIPLES',12,Y,700)+txt(33,289,'Reproducibility   /   Automation   /   Observability   /   Reliability',17,T,600)
    svg('pipeline.svg',960,316,'MLOps engineering lifecycle','Ingest, train, register, serve, observe, and use feedback to improve. Focus on reproducibility, automation, observability and reliability.',b)

def stack():
    b=section('02','ENGINEERING MODULES','TOOLKIT / TECHNICAL INTERESTS')
    groups=[('01','AI / MODELING',['PyTorch','OpenCV','scikit-learn','Hugging Face'],C),('02','MLOPS / DELIVERY',['Docker','Kubernetes','GitHub Actions','Jenkins'],M),('03','BACKEND / DATA',['FastAPI','Flask','PostgreSQL','MySQL','MongoDB'],Y),('04','CLOUD / SYSTEMS',['AWS','Terraform','Linux'],C),('05','LANGUAGES',['Python','Java','C++','JavaScript','TypeScript'],M),('06','INTERFACES',['React','API design','Data visualization'],Y)]
    for i,(n,title,items,color) in enumerate(groups):
        x=32+(i%2)*454; y=68+(i//2)*116
        b+=rect(x,y,442,104,'#0e1929',LINE,6)+rect(x,y,4,104,color,rx=2)+txt(x+15,y+25,n,12,color,700)+txt(x+47,y+25,title,17,T,700)
        xx=x+15; yy=y+38
        for item in items:
            w=16+len(item)*8
            if xx+w>x+429: xx=x+15; yy+=27
            b+=rect(xx,yy,w,23,'#152638','#2a4351',3)+txt(xx+8,yy+16,item,13,T); xx+=w+7
    svg('stack.svg',960,426,'Engineering toolkit','Existing profile skills and interests grouped into AI, MLOps, backend, cloud, languages, and interfaces.',b)

PROJECTS=[('VOILORACLE','AI / NEWS INTELLIGENCE','Multi-source news, sentiment and event intelligence.',C),('VerifAI','AI / VERIFICATION','Multi-model answers, claim-level evidence and audit trails.',M),('NexusCloud-Orchestra','CLOUD / ORCHESTRATION','Unified multi-cloud storage routing and API layer.',Y),('CadastraVision','BACKEND / GEOSPATIAL','Parcel validation, PostGIS records and tamper-evident audits.',C),('Projexa','WEB / WORKFLOW','Academic project submission, tracking and evaluation.',M),('Portfolio','TYPESCRIPT / WEBSITE','Personal site, engineering work and technical interests.',Y)]

def projects():
    b=section('03','PROJECT TRANSMISSIONS','SELECTED PUBLIC WORK')
    for i,(name,tag,desc,color) in enumerate(PROJECTS):
        y=67+i*76
        b+=rect(32,y,896,66,'#0e1929',LINE,5)+rect(32,y,4,66,color)+txt(49,y+23,f'{i+1:02}',13,color,700)+txt(84,y+27,name,23,T,700,family=SANS)+txt(85,y+50,desc,15,S,family=SANS)+txt(914,y+26,tag,12,color,700,'end')
        b+=poly(f'M899 {y+42}h15v15m0 -15l-15 15','none',color,'stroke-width="1.5"')
    svg('projects.svg',960,536,'Selected projects','VOILORACLE, VerifAI, NexusCloud-Orchestra, CadastraVision, Projexa and Portfolio. Repository and deployment links are below.',b)

def button(name,label,sub,color):
    b=rect(4,4,284,56,'#111d2e',LINE,5)+rect(4,4,4,56,color,rx=2)+txt(18,25,label,15,T,700)+txt(18,43,sub,11,S)+poly('M252 22H271V41M271 22L252 41','none',color,'stroke-width="2"')
    svg(name,292,64,label,sub,b)

def contact():
    b=section('05','OPEN A CHANNEL','COLLABORATION / OPPORTUNITIES')
    b+=txt(32,87,'Engineer the pipeline. Automate the process.',25,T,750,family=SANS)+txt(32,122,'Make the system reliable.',25,C,750,family=SANS)+txt(32,155,'Open to software engineering, AI/MLOps, cloud and open-source collaboration.',16,S,family=SANS)
    svg('contact.svg',960,181,'Connect with Arun Prasath','Open to software engineering opportunities, AI and MLOps projects, cloud and open-source collaboration.',b)
    button('link-portfolio.svg','PORTFOLIO','arunprasath.me',C); button('link-linkedin.svg','LINKEDIN','Connect professionally',M); button('link-github.svg','GITHUB','Explore public code',Y)

def request(path, payload=None):
    url='https://api.github.com'+path
    headers={'Accept':'application/vnd.github+json','User-Agent':'AP2717-profile-renderer','X-GitHub-Api-Version':'2022-11-28'}
    token=os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
    if token: headers['Authorization']='Bearer '+token
    if payload is not None: headers['Content-Type']='application/json'
    req=urllib.request.Request(url,data=json.dumps(payload).encode() if payload is not None else None,headers=headers)
    with urllib.request.urlopen(req,timeout=30) as resp: return json.load(resp)

def fetch_live():
    repos=[]
    for p in range(1,101):
        page=request(f'/users/{LOGIN}/repos?type=owner&per_page=100&page={p}&sort=pushed&direction=desc')
        if not isinstance(page,list): raise ValueError('Expected a repository list')
        repos.extend(r for r in page if not r.get('private') and not r.get('fork') and r.get('name','').lower()!=LOGIN.lower())
        if len(page)<100: break
    else: raise ValueError('Repository page limit reached')
    # Keep the complete fetched public-owned, non-fork list; exclude this profile repo.
    fields=('name','language','stargazers_count','forks_count','pushed_at','archived')
    cleaned=[{k:r.get(k) for k in fields} for r in repos]
    today=dt.datetime.now(dt.timezone.utc)
    result={'scope':'public','as_of':today.isoformat(timespec='seconds'),'repos':cleaned,'calendar':None}
    try:
        start=today-dt.timedelta(days=364)
        data=request('/graphql',{'query':'''query($login:String!, $from:DateTime!, $to:DateTime!) { user(login:$login) { contributionsCollection(from:$from,to:$to) { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } } } }''','variables':{'login':LOGIN,'from':start.isoformat(),'to':today.isoformat()}})
        cal=data['data']['user']['contributionsCollection']['contributionCalendar']
        if data.get('errors'): raise ValueError('GraphQL returned errors')
        # Contribution calendar visibility follows GitHub's profile visibility/token rules.
        result['calendar']=cal
    except Exception as e:
        print('Contribution calendar unavailable:',type(e).__name__,file=sys.stderr)
    return result

def telemetry(data):
    repos=data['repos']; sample=data['scope']!='public'; ts=data['as_of'][:10]; cal=data.get('calendar')
    b=section('04','SIGNAL / GITHUB TELEMETRY','SCHEDULED PUBLIC DATA' if not sample else 'INITIAL VERIFIED SAMPLE')
    metrics=[('REPOSITORIES',len(repos)),('STARS',sum(r.get('stargazers_count') or 0 for r in repos)),('FORKS',sum(r.get('forks_count') or 0 for r in repos)),('LANGUAGES',len({r['language'] for r in repos if r.get('language')}))]
    for i,(label,value) in enumerate(metrics):
        x=32+i*226; color=[C,M,Y,C][i]; b+=rect(x,68,218,83,'#111e2e',LINE,5)+txt(x+13,92,label,12,S,700)+txt(x+13,133,str(value),35,color,750)+rect(x+13,142,192,2,color,extra='opacity=".35"')
    b+=txt(32,176,'SELECTED REPO SAMPLE • Not account totals' if sample else 'Public owned non-fork repositories • Profile repository excluded',13,S)+txt(928,176,'SNAPSHOT '+ts+' UTC',12,S,anchor='end')
    # Contribution grid uses exactly returned values; never fabricates counts.
    b+=rect(32,194,896,198,'#0c1725',LINE,6)+txt(48,219,'CONTRIBUTION SIGNAL',17,T,700)
    if cal:
        weeks=cal.get('weeks',[])[-53:]; all_days=[d['contributionCount'] for w in weeks for d in w['contributionDays']]; high=max(all_days or [1]) or 1
        b+=txt(912,219,f"{cal['totalContributions']} contributions / queried 365 days",12,C,700,'end')
        for i,w in enumerate(weeks):
            for day in w['contributionDays']:
                weekday=(dt.date.fromisoformat(day['date']).weekday()+1)%7; n=day['contributionCount']; col='#1c2c3a' if not n else ['#174e57','#217e82','#33b8b3',C][min(3,int(n/high*4))]
                b+=rect(83+i*15,242+weekday*15,12,12,col,rx=2)
        for row,label in [(1,'MON'),(3,'WED'),(5,'FRI')]: b+=txt(48,252+row*15,label,10,S)
        b+=txt(48,372,'GitHub contribution calendar • profile visibility applies',12,S)
        for i,col in enumerate(['#1c2c3a','#174e57','#217e82','#33b8b3',C]): b+=rect(814+i*17,360,13,13,col,rx=2)
    else:
        b+=poly('M48 265H912','none',LINE,'stroke-dasharray="3 6"')+txt(48,300,'CALENDAR AWAITING GITHUB DATA' if sample else 'CONTRIBUTION CALENDAR UNAVAILABLE',19,Y,700)+txt(48,328,'No invented activity. Repository metrics are still available.',15,S,family=SANS)+txt(48,366,'The next successful GraphQL refresh will populate this panel.',13,S)
    b+=rect(32,409,355,181,'#0c1725',LINE,6)+txt(48,435,'LANGUAGE DISTRIBUTION',16,T,700)+txt(48,454,'Primary language by repository count',11,S)
    langs=collections.Counter(r['language'] for r in repos if r.get('language')); top=langs.most_common(4); total=sum(langs.values()) or 1
    for i,(lang,count) in enumerate(top):
        y=476+i*26; b+=txt(48,y+9,cut(lang,14),12,T)+rect(173,y,155,10,'#253748',rx=2)+rect(173,y,max(1,155*count/total),10,[C,M,Y,'#8fa9fd'][i],rx=2)+txt(369,y+9,str(count),12,S,anchor='end')
    if not top: b+=txt(48,490,'No languages reported',13,S)
    b+=rect(401,409,527,181,'#0c1725',LINE,6)+txt(417,435,'RECENT REPOSITORY PUSHES',16,T,700)+txt(912,435,'UTC',11,S,anchor='end')
    for i,r in enumerate(sorted(repos,key=lambda r:r.get('pushed_at') or '',reverse=True)[:4]):
        y=460+i*30; b+=circle(421,y-4,3,C if i==0 else M)+txt(432,y,cut(r['name'],31),14,T,600)+txt(912,y,(r.get('pushed_at') or 'Unknown')[:10],12,S,anchor='end')+line(417,y+10,912,y+10)
    b+=txt(32,618,'REFRESH / 6 HOURS VIA GITHUB ACTIONS • CACHED BY GITHUB • NO THIRD-PARTY CARDS',11,S)
    svg('telemetry.svg',960,636,'GitHub telemetry',f'{"Initial verified sample" if sample else "Public repository snapshot"} as of {ts}. {len(repos)} repositories. Stars, forks, language distribution, recent pushes, and contribution calendar when available.',b)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--snapshot',type=pathlib.Path); p.add_argument('--live',action='store_true'); a=p.parse_args()
    if a.live==bool(a.snapshot): p.error('Choose exactly one: --live or --snapshot')
    data=fetch_live() if a.live else json.loads(a.snapshot.read_text())
    hero(); pipeline(); stack(); projects(); contact(); telemetry(data)
    import neural_grid
    neural_grid.r.ASSETS = ASSETS
    neural_grid.render(data)
    # Fail before publishing malformed output.
    import xml.etree.ElementTree as ET
    for f in ASSETS.glob('*.svg'): ET.parse(f)
    print(f'Rendered {len(list(ASSETS.glob("*.svg")))} SVG assets')

if __name__=='__main__': main()
