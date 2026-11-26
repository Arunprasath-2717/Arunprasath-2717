"""AP/2717 engineering dossier. Native SVG, two themes, measured data only."""
from __future__ import annotations
import argparse, datetime as dt, html, json, os, pathlib, urllib.request
import xml.etree.ElementTree as ET
ROOT=pathlib.Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
DATA=ROOT/'data'
LOGIN='Arunprasath-2717'
from cinema import THEMES

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
    import cinema
    cinema.OUT=ASSETS
    for theme in THEMES:
        for i,p in enumerate(profile['projects'],1): cinema.project(theme,p,i)
        cinema.toolkit(theme);cinema.focus(theme);cinema.activity(theme,data)
    if a.live: source.write_text(json.dumps(data,indent=2)+'\n')
    print('Generated 12 SVGs;',sum(w['count'] for w in data['weeks']),'contributions')
if __name__=='__main__':main()
