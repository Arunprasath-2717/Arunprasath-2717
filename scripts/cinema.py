"""AP/2717 field guide: explanatory technical motion, not decorative dashboards."""
from pathlib import Path
import html, math, xml.etree.ElementTree as ET
OUT=Path(__file__).resolve().parents[1]/'assets'
THEMES={'dark':dict(bg='#171c19',fg='#edf1e9',dim='#bbc6bd',rule='#46574b',accent='#b5d5ac',ink='#24312a',gold='#d7b477',quiet='#34433a'), 'light':dict(bg='#f4f7f3',fg='#1c2b22',dim='#45584b',rule='#afc1b1',accent='#286440',ink='#e4ebe3',gold='#805421',quiet='#d1dfd2')}
SANS='Arial, Helvetica, sans-serif'; SERIF='Georgia, Times New Roman, serif'; MONO='Consolas, Liberation Mono, monospace'
def e(s):return html.escape(str(s),quote=True)
def t(x,y,s,size,c,anchor='start',font=SANS,weight=400,extra=''):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" font-family="{font}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{e(s)}</text>'
def r(x,y,w,h,c,extra=''):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" {extra}/>'
def path(d,c,w=1,extra=''):return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" {extra}/>'
def circle(x,y,rad,c,extra=''):return f'<circle cx="{x}" cy="{y}" r="{rad}" fill="{c}" {extra}/>'
def g(s,extra=''):return f'<g {extra}>{s}</g>'
def write(name,theme,h,title,desc,body,css=''):
 c=THEMES[theme];s=f'<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{h}" viewBox="0 0 960 {h}" role="img" aria-labelledby="title desc"><title id="title">{e(title)}</title><desc id="desc">{e(desc)}</desc><style>{css}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.moving{{opacity:0}}}}</style>{r(0,0,960,h,c["bg"])}{body}</svg>\n';ET.fromstring(s);(OUT/f'{name}-{theme}.svg').write_text(s,encoding='utf-8')
def title(c,head,sub):return t(32,48,head,34,c['fg'],font=SERIF)+t(32,80,sub,17,c['dim'])
def project(theme,p,index):
 c=THEMES[theme];fg,dim,gr,rule,gold=c['fg'],c['dim'],c['accent'],c['rule'],c['gold'];slug=p['slug']
 if slug=='verifai':
  # An evidence inspection view, using a clearly marked example rather than invented benchmarks.
  b=title(c,'Evidence before verdict','Illustrative example from the verification workflow')
  b+=path('M32 99H928',rule)
  b+=t(32,133,'Model claim',18,dim)+t(32,164,'“The library is closed on Sunday.”',26,fg,font=SERIF)
  b+=r(32,179,430,2,rule)+r(32,179,430,2,gr,'class="scan" style="transform-origin:32px 179px"')
  b+=t(32,220,'Retrieved evidence',18,dim)+t(32,252,'“Sunday hours: 10:00–16:00.”',24,fg,font=SERIF)
  b+=path('M489 137V256',rule,1)
  b+=t(531,133,'Independent review',18,dim)
  b+=t(531,173,'Claim and source disagree',24,fg,weight=600)
  b+=t(531,210,'Verdict: dispute',30,gold,weight=600)
  b+=t(531,244,'No evidence → unknown',17,dim)
  b+=path('M32 280H928',rule)+t(32,307,'Extract claim  →  retrieve sources  →  review  →  keep evidence',17,dim)
  css='.scan{animation:scan 5s ease-in-out infinite}@keyframes scan{0%,100%{transform:scaleX(.04);opacity:.25}55%,82%{transform:scaleX(1);opacity:1}}'
  write(slug,theme,326,'VerifAI evidence review','Illustrative claim about a library disagrees with sample retrieved Sunday opening hours; independent review yields dispute.',b,css)
 elif slug=='atlox':
  # Text streams become two event clusters. Geometry encodes a real relationship.
  b=title(c,'Find the event behind the headlines','Illustrative clustering of related news fragments')
  b+=path('M32 99H928',rule)
  b+=t(32,126,'Incoming headlines',18,dim)+t(634,126,'Grouped events',18,dim)
  items=[('City opens new rail line',154,180),('First trains begin service',196,180),('Rain warning issued',238,258),('Heavy rainfall forecast',280,258)]
  for i,(label,y,target) in enumerate(items):
   b+=t(32,y,label,21,fg)+path(f'M340 {y-7}C455 {y-7} 480 {target-7} 616 {target-7}',rule,1.5)
   # Move along the actual corresponding grouping path, not a decorative dot.
   d=f'M340 {y-7}C455 {y-7} 480 {target-7} 616 {target-7}'
   b+=f'<circle r="4" fill="{gr}" class="moving" style="offset-path:path(\'{d}\');animation:route 3.2s linear infinite;animation-delay:-{i*.7}s" cx="0" cy="0"/>'
  b+=path('M634 143V205',gr,3)+t(650,168,'Rail opening',27,fg,weight=600)+t(650,192,'2 matching reports',17,dim)
  b+=path('M634 223V285',gold,3)+t(650,248,'Weather warning',27,fg,weight=600)+t(650,272,'2 matching reports',17,dim)
  b+=path('M32 304H928',rule)+t(32,331,'Normalize and deduplicate before NLP and density-based clustering.',17,dim)
  css='@keyframes route{0%{offset-distance:0%;opacity:0}12%,88%{opacity:1}100%{offset-distance:100%;opacity:0}}'
  write(slug,theme,350,'Atlox event grouping','Four illustrative headlines converge into two event clusters; moving points depict data grouping.',b,css)
 else:
  # Routing decision ledger, a separate form language from the other two.
  b=title(c,'One message, one explainable decision','Illustrative messages and routing outcomes')
  b+=path('M32 99H928',rule)
  for x,s in [(32,'Incoming message'),(394,'Context'),(735,'Action')]:b+=t(x,130,s,17,dim)
  rows=[('“Build failed”','Urgent work item','Notify',gr),('“Weekly summary”','Routine update','Digest',gold),('“Unsolicited offer”','Low relevance','Mute',dim)]
  for i,(msg,reason,act,col) in enumerate(rows):
   y=171+i*64;b+=path(f'M32 {y+24}H928',rule)
   b+=t(32,y,msg,23,fg)+t(394,y,reason,20,fg)+t(735,y,act,24,col,weight=600)
   b+=r(32,y+15,7,3,col)+r(40,y+15,160,3,col,f'class="marker" style="animation-delay:-{i*1.6}s;transform-origin:40px {y+15}px"')
  b+=t(32,358,'Context + historical retrieval + deterministic scoring',17,dim)
  css='.marker{animation:mark 4.8s ease-in-out infinite}@keyframes mark{0%,100%{transform:scaleX(.03);opacity:.1}33%,60%{transform:scaleX(1);opacity:.8}}'
  write(slug,theme,378,'CANE routing ledger','Illustrative messages and deterministic routing outcomes; urgent work notifies, routine update digests, low relevance mutes.',b,css)

def toolkit(theme):
 c=THEMES[theme];fg,dim,gr,rule=c['fg'],c['dim'],c['accent'],c['rule']
 b=title(c,'From source to serving','A software delivery sequence I work with and study')
 # One trace with real labels, no fake telemetry or floating decorative objects.
 xs=[90,285,480,675,870];labels=[('Linux','Source'),('Git / CI','Tests'),('Docker','Image'),('Cloud','Deploy'),('MLOps','Serve')]
 b+=path('M90 158H870',rule,3)
 for x,(a,d) in zip(xs,labels):
  b+=circle(x,158,10,c['bg'],f'stroke="{gr}" stroke-width="2"')+t(x,127,a,22,fg,'middle',weight=600)+t(x,199,d,19,dim,'middle')
 b+=g(r(78,145,24,26,gr)+path('M84 154H96M84 159H96M84 164H92',c['bg'],1.5),'class="artifact moving"')
 b+=t(480,239,'Build and test an artifact before promoting it to the next stage.',17,dim,'middle')
 css='.artifact{animation:artifact 8s linear infinite}@keyframes artifact{0%{transform:translateX(0);opacity:0}5%,95%{opacity:1}100%{transform:translateX(780px);opacity:0}}'
 write('toolchain',theme,260,'Source to serving','Illustrative Linux to ML serving delivery sequence. The moving artifact follows five stages.',b,css)

def focus(theme):
 c=THEMES[theme];fg,dim,gr,rule,gold=c['fg'],c['dim'],c['accent'],c['rule'],c['gold']
 b=title(c,'The path of a request','Conceptual backend and model-serving boundary')
 b+=t(32,137,'Client',22,fg,weight=600)+t(351,137,'API boundary',22,fg,weight=600)+t(725,137,'Model service',22,fg,weight=600)
 b+=path('M32 164H928',rule,2)+path('M928 214H32',rule,2)
 b+=t(32,198,'Request',17,dim)+t(928,250,'Response + trace',17,dim,'end')
 b+=r(344,153,3,72,gr)+r(712,153,3,72,gr)
 b+=g(r(32,157,22,14,gr)+path('M37 161H49M37 166H45',c['bg'],1),'class="request moving"')
 b+=g(r(906,207,22,14,gold)+path('M911 211H923M911 216H919',c['bg'],1),'class="response moving"')
 b+=t(32,286,'Validate → persist or retrieve → infer → return a traceable result',18,dim)
 css='.request{animation:request 7s linear infinite}.response{animation:response 7s linear infinite}@keyframes request{0%{transform:translateX(0);opacity:0}5%{opacity:1}43%{transform:translateX(874px);opacity:1}49%,100%{opacity:0;transform:translateX(874px)}}@keyframes response{0%,49%{opacity:0;transform:translateX(0)}53%{opacity:1}95%{opacity:1;transform:translateX(-874px)}100%{opacity:0;transform:translateX(-874px)}}'
 write('focus',theme,310,'Request lifecycle','A request goes through an API boundary to a model service and returns a response. This is a conceptual architecture.',b,css)

def lifecycle(theme):
 c=THEMES[theme];fg,dim,gr,rule,gold=c['fg'],c['dim'],c['accent'],c['rule'],c['gold']
 b=title(c,'The model lifecycle','Learning roadmap, from input data to measured feedback')
 # A topographic-style contour route is a meaningful map of lifecycle, not a dashboard.
 route='M96 175H350Q480 175 480 244T610 329H864'
 b+=path(route,rule,10,'stroke-linecap="round"')+path(route,gr,2,'stroke-linecap="round"')
 b+=path('M864 329Q916 329 916 280V147Q916 105 882 105H600',rule,1.5,'stroke-dasharray="5 7"')
 nodes=[(96,175,'Ingest','Data checks',145,-1),(275,175,'Train','Version model',145,-1),(468,218,'Evaluate','Quality gates',208,-1),(610,329,'Serve','API / container',290,-1),(746,329,'Observe','Logs / metrics',368,1),(864,329,'Improve','Feedback',290,-1)]
 for x,y,label,sub,ty,side in nodes:
  b+=circle(x,y,9,c['bg'],f'stroke="{gr}" stroke-width="2"')
  lx=x+100 if label=='Evaluate' else x
  b+=t(lx,ty,label,20,fg,'middle',weight=600)+t(lx,ty+(22 if label=='Evaluate' or side==1 else -19),sub,15,dim,'middle')
 b+=f'<circle r="5" cx="0" cy="0" fill="{gold}" class="moving" style="offset-path:path(\'{route}\');animation:journey 9s linear infinite"/>'
 b+=t(896,94,'Feedback to the next experiment',16,dim,'end')
 b+=t(32,413,'Evaluation and monitoring feed the next experiment.',17,dim)
 css='@keyframes journey{0%{offset-distance:0%;opacity:0}7%,93%{opacity:1}100%{offset-distance:100%;opacity:0}}'
 write('lifecycle',theme,432,'MLOps learning roadmap','Ingest, train, evaluate, serve, observe, improve. Feedback returns to the next experiment. Conceptual learning map.',b,css)

def activity(theme,data):
 c=THEMES[theme];fg,dim,gr,rule=c['fg'],c['dim'],c['accent'],c['rule'];weeks=data['weeks'];counts=[w['count'] for w in weeks]
 b=t(32,31,'Development record',21,fg,font=SERIF)+t(928,31,data['as_of']+' UTC',16,dim,'end',MONO)
 for x,num,label in [(32,sum(counts),'Contributions'),(350,sum(n>0 for n in counts),'Active weeks'),(670,max(counts+[0]),'Peak week')]:b+=t(x,91,num,44,fg,weight=600,font=MONO)+t(x,118,label,18,dim)
 b+=path('M32 138H928',rule)
 for w in weeks:b+=g(f'<title>Week of {e(w["date"])}: {w["count"]} contributions</title>')
 write('activity',theme,150,'GitHub contribution totals',f'{sum(counts)} contributions across {len(weeks)} weeks. Snapshot {data["as_of"]}.',b)
