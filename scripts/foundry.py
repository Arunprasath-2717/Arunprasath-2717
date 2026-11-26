"""Signal Foundry: original procedural vector title sequence.
53 engraved channels encode the actual weekly GitHub contribution counts.
No external imagery, JavaScript or WebGL. The art is illustrative, data is not.
"""
import math, random
from pathlib import Path
import fieldwork as f
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'
def poly(points,fill,extra=''):
    return '<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+'" fill="'+fill+'" '+extra+'/>'
def hero(data):
    # Oblique projection of a machined silicon substrate, viewed like a product photograph.
    def pt(x,y,z=0):return (756+(x-y)*.83,207+(x+y)*.39-z)
    def face(x,y,w,h,z,fill,extra=''):
        return poly([pt(x,y,z),pt(x+w,y,z),pt(x+w,y+h,z),pt(x,y+h,z)],fill,extra)
    def block(x,y,w,h,z,d,top,side,front):
        a,b,c,d0=pt(x,y,z),pt(x+w,y,z),pt(x+w,y+h,z),pt(x,y+h,z)
        return poly([b,c,pt(x+w,y+h,z-d),pt(x+w,y,z-d)],side)+poly([d0,c,pt(x+w,y+h,z-d),pt(x,y+h,z-d)],front)+poly([a,b,c,d0],top,'stroke="#b9a58d" stroke-opacity=".28" stroke-width=".7"')
    def trace(points,color,width=1,extra=''):
        return f.p('M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in points),color,width,extra)
    b='''<defs>
      <linearGradient id="bg" x2="1" y2="1"><stop stop-color="#191a1d"/><stop offset=".7" stop-color="#151618"/><stop offset="1" stop-color="#25211d"/></linearGradient>
      <radialGradient id="halo"><stop stop-color="#bda27f" stop-opacity=".19"/><stop offset="1" stop-color="#bda27f" stop-opacity="0"/></radialGradient>
      <linearGradient id="base" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#484745"/><stop offset=".5" stop-color="#292c2e"/><stop offset="1" stop-color="#62605a"/></linearGradient>
      <linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#b4a28a"/><stop offset=".3" stop-color="#625a50"/><stop offset=".62" stop-color="#a58e71"/><stop offset="1" stop-color="#393938"/></linearGradient>
      <linearGradient id="die" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#4a4c4a"/><stop offset=".45" stop-color="#222728"/><stop offset="1" stop-color="#4c4942"/></linearGradient>
      <linearGradient id="gold"><stop stop-color="#80674a"/><stop offset=".48" stop-color="#dfc7a0"/><stop offset="1" stop-color="#8d7459"/></linearGradient>
      <radialGradient id="shadow"><stop stop-color="#070809" stop-opacity=".92"/><stop offset="1" stop-color="#070809" stop-opacity="0"/></radialGradient>
      <clipPath id="edge"><rect width="1200" height="460" rx="15"/></clipPath>
      <linearGradient id="reflection"><stop stop-color="#f6e4cb" stop-opacity="0"/><stop offset=".5" stop-color="#f6e4cb" stop-opacity=".3"/><stop offset="1" stop-color="#f6e4cb" stop-opacity="0"/></linearGradient>
      </defs>'''
    b+=f.r(0,0,1200,460,'url(#bg)','rx="15"')
    b+='<g clip-path="url(#edge)"><ellipse cx="830" cy="214" rx="377" ry="236" fill="url(#halo)"/><ellipse cx="782" cy="346" rx="285" ry="89" fill="url(#shadow)"/>'
    # A restrained etched background, material marks aligned to the substrate perspective.
    for i in range(20):
        x=590+i*33
        b+=f.p(f'M{x} 424L{x+230} 310','#a69b87',.5,'opacity=".055"')
    # Lower substrate and copper rails, physically layered.
    b+=block(-178,-178,356,356,0,17,'url(#base)','#292929','#212224')
    b+=block(-169,-169,338,338,8,9,'#323638','#282b2c','#202324')
    for i in range(19):
        v=-152+i*17
        for side in (-1,1):
            if side<0:
                b+=face(v,-167,9,18,10,'url(#gold)')
                b+=face(-167,v,18,9,10,'url(#gold)')
            else:
                b+=face(v,149,9,18,10,'url(#gold)')
                b+=face(149,v,18,9,10,'url(#gold)')
    for i in range(14):
        v=-145+i*22
        b+=trace([pt(v,-144,11),pt(v,-118,11),pt(v*.68,-99,11)],'#b89c74',.65,'opacity=".55"')
        b+=trace([pt(-144,v,11),pt(-118,v,11),pt(-99,v*.68,11)],'#b89c74',.65,'opacity=".55"')
        b+=trace([pt(v,144,11),pt(v,118,11),pt(v*.68,99,11)],'#b89c74',.65,'opacity=".55"')
        b+=trace([pt(144,v,11),pt(118,v,11),pt(99,v*.68,11)],'#b89c74',.65,'opacity=".55"')
    b+=block(-112,-112,224,224,26,18,'url(#metal)','#51473a','#72614d')
    b+=block(-103,-103,206,206,34,8,'url(#die)','#303234','#2b2c2c')
    b+=face(-98,-98,196,196,35,'#252a2b','stroke="#b0a08c" stroke-opacity=".5" stroke-width=".7"')
    # Microstructures occupy the central die, not generic floating nodes.
    for i in range(11):
        for j in range(9):
            x=-89+i*16;y=-87+j*13
            b+=face(x,y,11,8,36,'#434745' if (i+j)%3 else '#71695a','opacity=".64"')
    weeks=data['weeks'];peak=max([w['count'] for w in weeks]+[1])
    # Individual etched grooves on the near edge. Length is linearly proportional to count.
    for i,w in enumerate(weeks):
        x=-96+i*(192/max(1,len(weeks)));n=w['count'];l=2+47*n/peak
        b+=f'<g><title>Week of {w["date"]}: {n} contributions</title>'
        b+=trace([pt(x,92,37),pt(x,92-l,37)],'#ddc5a0' if n else '#626565',1.4,'stroke-linecap="round" opacity=".82"')+'</g>'
    # A travelling reflection on four fixed traces, no zoom or camera motion.
    for i,points in enumerate([[(0,-155),(0,-121),(0,-109)],[(-155,26),(-122,26),(-108,18)],[(78,155),(78,125),(55,109)],[(155,-46),(124,-46),(108,-35)]]):
        q=[pt(x,y,12) for x,y in points]
        b+=trace(q,'#e4c6a0',1.8,f'stroke-dasharray="5 35" stroke-linecap="round" class="travel" style="animation-delay:-{i*.81}s"')
    # Small engraved maker mark on die, aligned with the top plane.
    x,y=pt(0,0,38)
    b+=f'<g transform="translate({x:.2f} {y:.2f}) matrix(.83 .39 -.83 .39 0 0)"><rect x="-53" y="-31" width="106" height="62" rx="5" fill="#272a2a" stroke="#a5957c" stroke-opacity=".7"/><text x="0" y="-2" text-anchor="middle" font-size="26" font-family="Arial,sans-serif" font-weight="700" fill="#ead8b8">AP</text><text x="0" y="18" text-anchor="middle" font-size="12" font-family="monospace" fill="#c4af8f">2717</text></g>'
    # A moving specular highlight confined to the metal surface.
    rim=[pt(-112,-112,26),pt(112,-112,26),pt(112,112,26),pt(-112,112,26)]
    b+='<defs><clipPath id="metal-reflect">'+poly(rim,'white')+'</clipPath></defs>'
    b+='<g clip-path="url(#metal-reflect)"><path d="M510 45L590 45L790 350L710 350Z" fill="url(#reflection)" class="reflect" opacity=".65"/></g>'
    b+='</g>'
    b+=f.t(47,49,'AP / 2717',13,'#c7b69b',700,font=f.MONO,extra='letter-spacing="3"')
    b+=f.t(47,150,'Arun',81,'#f4f1e9',700)
    b+=f.t(43,233,'Prasath',81,'#f4f1e9',700)
    b+=f.r(48,262,44,3,'#d3b68c','rx="1.5"')
    b+=f.t(47,303,'Backend engineering',25,'#ede9e0',500)
    b+=f.t(47,339,'Applied AI  /  MLOps',25,'#ede9e0',500)
    b+=f.t(47,387,'Computer science student · India',16,'#bfc1bf')
    b+=f.p('M47 413H1153','#7f807e',.8,'opacity=".38"')
    b+=f.t(47,438,'SIGNAL FOUNDRY',12,'#c7b69b',700,font=f.MONO,extra='letter-spacing="2"')
    b+=f.t(1153,438,f'{len(weeks)} engraved weekly contribution channels · {data["as_of"]} UTC',12,'#c0bbb3',400,'end',f.MONO)
    css='.travel{animation:travel 2.6s linear infinite}.reflect{animation:reflect 7s ease-in-out infinite}@keyframes travel{to{stroke-dashoffset:-40}}@keyframes reflect{0%,12%{transform:translateX(-110px);opacity:0}25%{opacity:.65}72%{opacity:.5}85%,100%{transform:translateX(420px);opacity:0}}'
    f.OUT=OUT
    f.write('foundry-hero.svg',1200,460,'Arun Prasath — Signal Foundry','Backend engineering, applied AI and MLOps. An original oblique silicon substrate with engraved channels proportional to actual weekly GitHub contributions.',b,css)
def skills():
    # A compact technical index, with a distinctive engineered material strip rather than scenery.
    b=f.shell(960,379,'#d7bd96')
    b+=f.t(28,37,'ENGINEERING TOOLKIT',12,'#d7bd96',700,font=f.MONO,extra='letter-spacing="2"')
    b+=f.t(28,78,'From source to serving.',35,f.FG,700)
    rows=[('Languages','Python · Java · TypeScript','JavaScript · C/C++ · SQL'),('Backend','FastAPI · Flask · Node.js','REST · SQLAlchemy · JWT'),('Applied AI','PyTorch · Transformers · spaCy','scikit-learn · OpenCV · BM25'),('Data systems','PostgreSQL · PostGIS · Redis','SQLite · MongoDB · Supabase'),('Linux & delivery','Linux · Docker · Git · Actions','CI/CD · Pytest · Ruff · Mypy'),('Web engineering','React · Next.js · Vite','HTML/CSS · WebSockets')]
    for i,(head,l1,l2) in enumerate(rows):
        x=28+(i%2)*468;y=113+(i//2)*86
        b+=f.p(f'M{x} {y-11}H{x+436}',f.LINE)
        b+=f.t(x,y+13,f'{i+1:02}',11,'#d7bd96',700,font=f.MONO)
        b+=f.t(x+35,y+14,head,19,f.FG,700)
        b+=f.t(x+35,y+36,l1,15,f.DIM)+f.t(x+35,y+55,l2,15,f.DIM)
    b+=f.p('M28 354H932',f.LINE)
    f.OUT=OUT
    f.write('field-skills.svg',960,379,'Engineering toolkit','Languages, backend, applied AI, data, Linux and delivery, web engineering.',b)
