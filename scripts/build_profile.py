"""AP/2717: an illustrated computing workshop, generated entirely as SVG.
Only the punched telemetry strip encodes measured data. Machinery is illustrative.
"""
from __future__ import annotations
import argparse, datetime as dt, html, json, math, os, pathlib, re, urllib.request
import xml.etree.ElementTree as ET

ROOT=pathlib.Path(__file__).resolve().parents[1]
ASSET=ROOT/'assets'/'workshop.svg'
LOGIN='Arunprasath-2717'
W,H=960,508
INK='#171612'; PAPER='#f0e3c8'; PAPER2='#dfcfad'; BLACK='#211e17'
GOLD='#c7a063'; COPPER='#b66e40'; DARK='#332e24'; MID='#514738'
SAND='#82715a'; CREAM='#fff2d6'; OLIVE='#58604a'; GREEN='#9dba78'
BROWN='#694c36'; SHADOW='#baaa89'
SERIF='Georgia, Times New Roman, serif'; MONO='ui-monospace, Consolas, monospace'

def e(s): return html.escape(str(s),quote=True)
def path(d,f='none',s='none',w=1,extra=''):
    return f'<path d="{d}" fill="{f}" stroke="{s}" stroke-width="{w}" {extra}/>'
def rect(x,y,w,h,f,s='none',rx=0,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" stroke="{s}" {extra}/>'
def circle(x,y,r,f,s='none',extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{f}" stroke="{s}" {extra}/>'
def txt(x,y,s,size=14,f=INK,anchor='start',family=MONO,weight=400,extra=''):
    return f'<text x="{x}" y="{y}" fill="{f}" font-size="{size}" text-anchor="{anchor}" font-family="{family}" font-weight="{weight}" {extra}>{e(s)}</text>'
def poly(points,f,s='none'):
    return f'<polygon points="{points}" fill="{f}" stroke="{s}"/>'

def calendar(token):
    query='query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}'
    request=urllib.request.Request('https://api.github.com/graphql',data=json.dumps({'query':query,'variables':{'login':LOGIN}}).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','User-Agent':'AP2717-workshop'})
    with urllib.request.urlopen(request,timeout=30) as response: data=json.load(response)
    if data.get('errors'): raise ValueError('GitHub returned GraphQL errors')
    weeks=data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
    return sorted((w['contributionDays'][0]['date'],sum(d['contributionCount'] for d in w['contributionDays'])) for w in weeks if w['contributionDays'])[-53:]

def migrate():
    for p in [ASSET,ROOT/'assets'/'forge.svg',ROOT/'assets'/'neural-grid.svg']:
        if p.exists():
            s=p.read_text()
            weeks=sorted((d,int(n)) for d,n in re.findall(r'<title>Week of (\d{4}-\d{2}-\d{2}): (\d+) contributions</title>',s))
            if weeks: return weeks[-53:]
    return []

def cabinet(x,y,w,h,depth=27):
    # Solid three-face construction; front is readable at README scale.
    return (poly(f'{x},{y} {x+depth},{y-18} {x+w+depth},{y-18} {x+w},{y}',SAND)
          +poly(f'{x+w},{y} {x+w+depth},{y-18} {x+w+depth},{y+h-18} {x+w},{y+h}',DARK)
          +rect(x,y,w,h,MID,BLACK,3)+rect(x+5,y+5,w-10,h-10,BLACK,INK,2))

def render(weeks,date):
    b=[rect(0,0,W,H,PAPER),rect(12,12,936,484,'none',SHADOW)]
    # Editorial title, understated engraved maker mark.
    b += [txt(34,42,'FIELD NOTES   /   2717',12,BROWN,weight=700,extra='letter-spacing="2"'),
          txt(34,106,'Arun Prasath',54,INK,family=SERIF,weight=700),
          txt(37,132,'LINUX  /  CLOUD  /  MLOPS',14,BROWN,weight=700,extra='letter-spacing="1.5"'),
          txt(926,43,'SYSTEMS ENGINEERING',12,BROWN,'end',weight=700),
          txt(926,63,'AI · BACKEND · INFRASTRUCTURE',10,MID,'end'),
          path('M34 149H926','none',BROWN,1)]
    # Scene framed as a single cutaway illustration, not separate cards.
    b += [rect(34,164,892,256,INK,rx=3),
          '<g transform="translate(0 48)">',
          path('M34 298L197 204H794L926 286V372H34Z','#28251d'),
          circle(670,226,58,'#594331'),
          path('M35 320L190 256L302 275L401 236L541 252L695 214L925 296V371H35Z','#3c3327'),
          path('M35 343L192 294L286 309L410 282L567 296L701 263L925 324V371H35Z','#514534'),
          # integrated platform with deep side and cast shadows
          poly('69,329 230,252 873,252 917,329 760,356 111,356', '#6d5940'),
          poly('69,329 111,356 760,356 917,329 917,340 762,368 111,368 69,343', '#30281e'),
          poly('104,325 235,260 861,260 900,324 758,349 124,349', '#857052')]
    # A single copper service conduit visually connects the three machines.
    conduit='M170 328C236 349 271 324 308 322S374 337 412 322S501 337 535 321S624 345 676 323S743 325 801 311'
    b += [path(conduit,'none',BLACK,13,extra='stroke-linecap="round"'),
          path(conduit,'none',COPPER,7,extra='stroke-linecap="round"'),
          path(conduit,'none',GOLD,2,extra='stroke-linecap="round" stroke-dasharray="6 13" class="signal"')]
    # Chapter I: physical Linux terminal, large CRT, keyboard, chassis.
    b += [poly('94,326 238,326 276,344 133,350', '#43382b'),
          cabinet(116,211,142,100,30),
          rect(126,221,122,73,'#867355',BLACK,7),
          rect(133,228,108,56,'#22291e',BLACK,6),
          rect(140,234,94,43,'#30392a',rx=2),
          txt(147,249,'$ whoami',10,GREEN,weight=700),
          txt(147,262,'arun',11,CREAM),
          txt(147,274,'$ _',10,GREEN),
          circle(239,301,3,GOLD),
          rect(133,301,37,3,BLACK),
          rect(174,311,34,10,DARK,BLACK,2),
          poly('150,321 221,321 248,331 124,331',SAND,BLACK),
          poly('128,333 248,333 242,341 124,341',DARK),
          poly('136,333 229,333 239,337 130,337',PAPER2)]
    for row in range(2):
        for i in range(12):
            b.append(rect(136+i*7.5-row*2,332+row*4,5.4,2.4,MID,rx=.5))
    # Chapter II: cloud rack, a real-looking enclosed rack with equipment shelves.
    b += [poly('349,326 493,326 533,342 391,348','#423528'),
          cabinet(361,184,132,145,38)]
    for i in range(5):
        y=195+i*25
        b += [rect(370,y,114,20,'#625341',BLACK,2),
              rect(376,y+4,66,12,DARK,BLACK,1)]
        for j in range(8): b.append(rect(380+j*7,y+7,4,5,'#987b54',rx=.6))
        b += [circle(453,y+10,2.7,GREEN),circle(463,y+10,2.7,GOLD),
              rect(474,y+3,4,14,BLACK)]
    b += [rect(360,325,134,6,BLACK),rect(374,331,13,7,DARK),rect(470,331,13,7,DARK),
          rect(506,209,16,80,BLACK,rx=2)]
    for i in range(9): b.append(rect(510,215+i*8,8,3,SAND,rx=1))
    # Chapter III: model-serving machine. A solid bronze casing, tiled inference board,
    # paper output tray; the moving light on the conduit is a metaphor, not runtime data.
    b += [poly('626,329 804,329 851,347 661,350','#41362a'),
          cabinet(643,219,158,111,44),
          rect(652,228,140,71,'#967247',BLACK,3),
          rect(660,235,124,58,'#3c4733',BLACK,3),
          rect(671,244,39,39,DARK,GOLD,2),
          rect(678,251,25,25,COPPER,BLACK,2),
          txt(690.5,267,'ML',12,CREAM,'middle',weight=700)]
    for i in range(5):
        y=246+i*7
        b += [path(f'M710 {y}H725L733 {y+4}H747','none',GOLD,1.5),
              rect(749,y,24,6,'#b7a271',BLACK,1)]
    for i in range(4):
        b += [circle(665+i*9,302,2.8,GREEN if i==0 else GOLD),
              rect(748+i*8,300,5,5,DARK,rx=1)]
    b += [rect(660,310,119,7,BLACK,rx=2),
          poly('676,317 764,317 790,333 653,333',PAPER2,BLACK),
          poly('681,321 758,321 772,330 667,330',CREAM)]
    for i in range(3): b.append(path(f'M{682+i*5} {324+i*2}H{750-i*4}','none',BROWN,.8))
    b.append("</g>")
    # Plain chapter captions are grounded in the engineer's learning focus.
    for x,num,title,sub in [(100,'01','Linux','Processes & APIs'),(359,'02','Cloud','Containers & delivery'),(642,'03','MLOps','Train · serve · observe')]:
        b += [rect(x,174,30,20,COPPER,rx=2),txt(x+15,188,num,12,CREAM,'middle',weight=700),
              txt(x+38,190,title,17,CREAM,family=SERIF,weight=700),
              txt(x,205,sub,10,PAPER2)]
    # Data as a compact punched tape. The 53 cells are chronological; intensity encodes
    # actual weekly activity. No randomly generated or inferred activity.
    b += [txt(34,443,'CONTRIBUTION TAPE',10,BROWN,weight=700,extra='letter-spacing="1"')]
    peak=max([n for _,n in weeks]+[1])
    for i,(day,n) in enumerate(weeks):
        x=35+i*11.4; h=5+int(18*math.sqrt(n/peak))
        f='#cfc1a2' if not n else (COPPER if n<peak else BLACK)
        b += [f'<g><title>Week of {e(day)}: {n} contributions</title>',
              rect(round(x,2),475-h,8,h,f,rx=1),'</g>']
    if not weeks: b.append(txt(34,470,'Calendar unavailable — no synthetic activity',12,BROWN))
    b += [txt(926,446,f'{sum(n for _,n in weeks)} contributions / {len(weeks)} weeks' if weeks else 'Calendar unavailable',12,INK,'end',weight=700),
          txt(926,467,f'Snapshot {date} UTC',10,BROWN,'end')]
    b.append('<style>.signal{animation:travel 4s linear infinite}@keyframes travel{to{stroke-dashoffset:-38}}@media(prefers-reduced-motion:reduce){.signal{animation:none}}</style>')
    desc='A warm engraved technical illustration of a Linux terminal, cloud server cabinet, and model-serving machine joined by a symbolic copper conduit. Weekly contribution tape uses measured GitHub counts.'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc"><title id="title">Arun Prasath — Field notes 2717</title><desc id="desc">{desc}</desc>{"".join(b)}</svg>\n'

def main():
    p=argparse.ArgumentParser(); p.add_argument('--live',action='store_true'); p.add_argument('--existing',action='store_true'); a=p.parse_args()
    if a.live==a.existing: p.error('Choose exactly one mode')
    date=dt.datetime.now(dt.timezone.utc).date().isoformat()
    if a.live:
        token=os.environ.get('GH_TOKEN')
        if not token: raise SystemExit('GH_TOKEN is required for live rendering')
        weeks=calendar(token)
        if not weeks: raise SystemExit('Calendar empty: preserving published asset')
    else: weeks=migrate()
    if not weeks: raise SystemExit('No verified contribution data available')
    svg=render(weeks,date); ET.fromstring(svg)
    ASSET.parent.mkdir(exist_ok=True)
    temporary=ASSET.with_suffix('.tmp')
    temporary.write_text(svg,encoding='utf-8'); temporary.replace(ASSET)
    print(f'Rendered {len(weeks)} weeks / {sum(n for _,n in weeks)} contributions / {len(svg.encode())} bytes')
if __name__=='__main__': main()
