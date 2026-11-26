"""Original AP/2717 engraved fantasy architecture. Flat pigments, no filters.
The 53 engraved marks encode GitHub activity; all other scenery is fictional.
"""
import argparse
import datetime as dt
import html
import math
import pathlib
import random
import re
import xml.etree.ElementTree as ET
import render_profile as api

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'/'forge.svg'
W,H=960,402
BLACK='#121411'; DARK='#1c2019'; STONE='#30362b'; MID='#454b39'
MOSS='#566348'; BRONZE='#b18b4a'; GOLD='#d3b679'; IVORY='#e8dfc8'
DIM='#8b8c73'
SERIF='Georgia, Times New Roman, serif'
MONO='ui-monospace, Consolas, monospace'
def esc(s): return html.escape(str(s),quote=True)
def path(d,fill='none',stroke='none',sw=1,extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def rect(x,y,w,h,fill,stroke='none',extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" {extra}/>'
def circ(x,y,r,fill='none',stroke='none',sw=1,extra=''):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def text(x,y,s,size=12,fill=IVORY,anchor='start',family=SERIF,extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-family="{family}" {extra}>{esc(s)}</text>'
def point(cx,cy,r,a): return cx+r*math.cos(a),cy+r*math.sin(a)
def pair(x,y): return f'{x:.2f} {y:.2f}'
def weekly(cal):
    if not cal: return []
    return [(w['contributionDays'][0]['date'],sum(d['contributionCount'] for d in w['contributionDays']))
            for w in cal.get('weeks',[]) if w.get('contributionDays')][-53:]
def existing():
    # Migrate verified published weekly data once; never invent a value.
    old=ROOT/'assets'/'neural-grid.svg'
    if not old.exists(): return []
    return sorted((d,int(n)) for d,n in re.findall(r'<title>Week of (\d{4}-\d{2}-\d{2}): (\d+) contributions</title>',old.read_text()))

def render(weeks, date):
    peak=max([n for _,n in weeks]+[1])
    b=[rect(0,0,W,H,BLACK),rect(9,9,942,384,'none',STONE)]
    # Far chamber: two receding pointed vaults and a pale aperture.
    b.append(path('M164 324V168Q164 64 480 24Q796 64 796 168V324Z',DARK,STONE,2))
    b.append(path('M230 324V163Q230 77 480 48Q730 77 730 163V324Z','#24291f',MID,2))
    b.append(path('M286 324V169Q286 94 480 68Q674 94 674 169V324Z',STONE,MOSS,1.2))
    # Inner recess and deliberate flat gold light.
    b.append(path('M332 322V181Q332 116 480 83Q628 116 628 181V322Z','#1a1d16',BRONZE,1))
    b.append(circ(480,193,101,'#282e23',MID,1))
    b.append(circ(480,193,85,'#373d2c',MOSS,1))
    b.append(circ(480,193,67,'#777448',BRONZE,1.5))
    b.append(circ(480,193,54,GOLD))
    b.append(circ(480,193,43,BLACK,BRONZE,1))
    # Central floating monolith: faceted, not a logo badge.
    b.append(path('M480 131L509 171L502 222L480 250L458 222L451 171Z','#23291f',GOLD,1.5))
    b.append(path('M480 131L480 250L458 222L451 171Z','#454b39',GOLD,.7))
    b.append(path('M480 145L494 174L488 210L480 224L472 210L466 174Z','none',BRONZE,1))
    b.append(path('M467 185H493M480 160V218','none',GOLD,.8))
    b.append(circ(480,185,3,IVORY))
    # Fine engraved radial marks, activity only on the outer ring.
    for i in range(53):
        a=math.radians(190+i*160/52)
        n=weeks[i][1] if i<len(weeks) else None
        length=4 if not n else 6+10*math.sqrt(n/peak)
        color=STONE if n is None else (DIM if n==0 else (IVORY if n==peak else BRONZE))
        p=point(480,193,106,a); q=point(480,193,106+length,a)
        tip='' if n is None else f'<title>Week of {esc(weeks[i][0])}: {n} contributions</title>'
        b.append(f'<g>{tip}'+path('M'+pair(*p)+'L'+pair(*q),'none',color,1.7 if n else .8)+'</g>')
    # Perspective floor, stone dais, stairs.
    b.append(path('M0 346L332 279H628L960 346V402H0Z',DARK,STONE,1))
    for x in range(-180,1200,100):
        b.append(path(f'M{x} 402L480 274','none',MID,.7))
    for y,x in [(308,267),(325,183),(350,62),(385,0)]:
        b.append(path(f'M{x} {y}H{960-x}','none',MID,.8))
    for x,y,w,h in [(396,269,168,10),(382,279,196,12),(365,291,230,14),(347,305,266,16)]:
        b.append(rect(x,y,w,h,STONE,MID))
        b.append(path(f'M{x} {y}H{x+w}','none',BRONZE,.8))
    # Towering near columns, visible tool-cut facets and capitals.
    def pillar(x,flip):
        s=f'<g transform="translate({x} 0) scale({flip} 1)">'
        s+=path('M0 25H116L95 48V282L118 314H0Z',BLACK,STONE,1)
        s+=path('M17 52H85L78 282H25Z',STONE,MID,1)
        s+=path('M25 60H40V280H25Z',MID)
        s+=path('M47 60V276M63 60V276','none','#676a50',1)
        s+=path('M12 33H103L88 53H22ZM19 278H88L106 307H7Z',MID,STONE,1)
        s+=path('M29 45H82M25 295H89','none',BRONZE,1)
        # Shallow engraved stepped motif.
        for y in (86,138,190,242):
            s+=path(f'M47 {y}l8 -8 8 8 -8 8Z','none',BRONZE,.8)
        return s+'</g>'
    b.extend([pillar(58,1),pillar(902,-1)])
    # A small human silhouette creates scale, no animation on the subject.
    b.append(circ(480,320,3.8,BLACK,GOLD,.5))
    b.append(path('M477 324L483 324L487 341L473 341Z',BLACK,GOLD,.55))
    b.append(path('M477 339L475 347M483 339L485 347','none',GOLD,.7))
    # Sparse hand-engraving texture, clipped to scene silhouette rather than simulated noise.
    rng=random.Random(2717)
    for i in range(84):
        x=rng.choice([rng.randrange(18,55),rng.randrange(905,941)])
        y=rng.randrange(43,324)
        b.append(path(f'M{x} {y}l{rng.randrange(3,10)} -3','none',MID,.55))
    # Only one restrained motion: the suspended forge's ember.
    b.append(circ(480,185,6,'none',GOLD,.75,'class="ember"'))
    b.append('<style>.ember{animation:breath 5s ease-in-out infinite}@keyframes breath{0%,100%{opacity:.25}50%{opacity:.9}}@media(prefers-reduced-motion:reduce){.ember{animation:none}}</style>')
    # Engraved lower margin gives data context without making it a dashboard.
    b.append(rect(0,361,960,41,BLACK))
    b.append(path('M20 361H940','none',BRONZE,.8))
    b.append(text(24,386,'AP / 2717',12,GOLD,family=MONO))
    caption=f'{sum(n for _,n in weeks)} contributions · {len(weeks)} weeks · {date} UTC' if weeks else 'Contribution calendar unavailable'
    b.append(text(480,386,caption,12,IVORY,'middle',MONO))
    b.append(text(936,386,'THE FORGE',12,GOLD,'end',MONO))
    desc='A monumental stone forge with an amber eclipse and a tiny figure for scale. The engraved radial marks show weekly GitHub contributions. Scenery is symbolic.'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc"><title id="title">The Forge — Arun Prasath</title><desc id="desc">{desc} {esc(caption)}.</desc>{"".join(b)}</svg>\n'

def main():
    p=argparse.ArgumentParser(); p.add_argument('--live',action='store_true'); p.add_argument('--existing',action='store_true'); a=p.parse_args()
    if a.live==a.existing: p.error('Choose one data source')
    today=dt.datetime.now(dt.timezone.utc).date().isoformat()
    if a.live:
        data=api.fetch_live(); weeks=weekly(data.get('calendar')); today=data['as_of'][:10]
        if not weeks and OUT.exists():
            print('Calendar unavailable; preserving last verified artwork.')
            return
    else:
        weeks=existing()
        # Old SVG contains the snapshot timestamp in its text.
        old=(ROOT/'assets'/'neural-grid.svg').read_text()
        m=re.search(r'WEEK NODES / UTC (\d{4}-\d{2}-\d{2})',old)
        if m: today=m[1]
    svg=render(weeks,today); ET.fromstring(svg)
    OUT.parent.mkdir(exist_ok=True); OUT.write_text(svg,encoding='utf-8')
    print(f'Rendered The Forge: {len(weeks)} weekly marks; {len(svg.encode())} bytes')
if __name__=='__main__': main()
