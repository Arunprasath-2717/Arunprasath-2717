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
def activity(theme,data):
 c=THEMES[theme];fg,dim,gr,rule=c['fg'],c['dim'],c['accent'],c['rule'];weeks=data['weeks'];counts=[w['count'] for w in weeks]
 b=t(32,31,'Development record',21,fg,font=SERIF)+t(928,31,data['as_of']+' UTC',16,dim,'end',MONO)
 for x,num,label in [(32,sum(counts),'Contributions'),(350,sum(n>0 for n in counts),'Active weeks'),(670,max(counts+[0]),'Peak week')]:b+=t(x,91,num,44,fg,weight=600,font=MONO)+t(x,118,label,18,dim)
 b+=path('M32 138H928',rule)
 for w in weeks:b+=g(f'<title>Week of {e(w["date"])}: {w["count"]} contributions</title>')
 write('activity',theme,150,'GitHub contribution totals',f'{sum(counts)} contributions across {len(weeks)} weeks. Snapshot {data["as_of"]}.',b)
