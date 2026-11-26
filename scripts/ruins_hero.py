"""Fixed-camera landscape with localized animated water textures.
Pillow is an optional offline artwork dependency, not required by CI.
"""
from pathlib import Path
import base64, io, math, random, xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFilter, ImageOps
ROOT=Path(__file__).resolve().parents[1]; A=ROOT/'assets'
W,H=1600,640
# Coordinates measured against the 1600 x 640 landscape plate.
FALLS=[(975,269,42,91,[(979,273),(1000,275),(1006,302),(1014,351),(990,351),(981,308)],2.1),
       (840,416,77,159,[(842,422),(895,428),(904,474),(916,552),(910,570),(876,567),(856,495)],1.8),
       (997,400,31,142,[(1005,406),(1014,406),(1024,450),(1021,527),(1008,540),(1003,494)],2.5),
       (1434,281,45,151,[(1455,286),(1476,284),(1469,321),(1461,364),(1450,428),(1437,422),(1443,361)],2.3),
       (1096,470,18,41,[(1098,473),(1105,474),(1113,501),(1105,507)],1.7)]
def uri(b,m):return f'data:image/{m};base64,'+base64.b64encode(b).decode()
def png(im):
    f=io.BytesIO();im.save(f,format='PNG',optimize=True);return uri(f.getvalue(),'png')
def build():
    plate=(A/'ruins-landscape.webp').read_bytes();im=Image.open(io.BytesIO(plate)).convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
    defs=[]; layers=[]
    for i,(x,y,w,h,poly,speed) in enumerate(FALLS):
        mask=Image.new('L',(w,h));ImageDraw.Draw(mask).polygon([(a-x,b-y) for a,b in poly],fill=255);mask=mask.filter(ImageFilter.GaussianBlur(3.4))
        # Extract fine vertical detail from the photographed falls, not artificial white dashes.
        crop=ImageOps.grayscale(im.crop((x,y,x+w,y+h)))
        blur=crop.filter(ImageFilter.GaussianBlur(4));import PIL.ImageChops as IC
        detail=IC.subtract(crop,blur,scale=1,offset=128)
        rng=random.Random(2717+i); tw,th=w,64
        # Blend actual waterfall detail with an elongated, tiled flow texture.
        tex=detail.resize((w,th),Image.Resampling.BICUBIC); alpha=Image.new('L',(w,th));d=ImageDraw.Draw(alpha)
        for j in range(max(12,w*2)):
            xx=rng.randrange(w);yy=rng.randrange(th);ll=rng.randrange(5,26);opacity=rng.randrange(7,38)
            for off in (-th,0,th):d.line((xx,yy+off,xx+rng.choice([0,0,1]),yy+ll+off),fill=opacity,width=1)
        alpha=alpha.filter(ImageFilter.GaussianBlur(.7)); alpha=IC.add(alpha,tex.point(lambda n:max(0,min(35,(n-124)*2))))
        rgba=Image.new('RGBA',(w,th),(232,251,246,255));rgba.putalpha(alpha)
        # White-alpha mask, bounded to the actual water surface.
        ma=Image.new('RGBA',(w,h),'white');ma.putalpha(mask)
        defs.append(f'<mask id="water{i}" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}" style="mask-type:alpha"><image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="{png(ma)}"/></mask>')
        u=png(rgba);tiles=''.join(f'<image x="{x}" y="{y+k*th}" width="{w}" height="{th}" xlink:href="{u}"/>' for k in range(-1,math.ceil(h/th)+1))
        layers.append(f'<g mask="url(#water{i})"><g class="water" style="animation-duration:{speed}s;animation-delay:-{i*.39}s">{tiles}</g></g>')
    rng=random.Random(2717);p=[]
    for i in range(26):
        x=rng.randrange(90,1540);y=rng.randrange(100,448);r=rng.uniform(.85,2.0); dx=rng.choice([-1,1])*rng.randrange(12,35);dy=-rng.randrange(15,38)
        p.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="#fff0c1" opacity=".5" class="mote" style="--dx:{dx}px;--dy:{dy}px;animation-duration:{rng.randrange(7,14)}s;animation-delay:-{rng.uniform(0,12):.2f}s"/>')
    # Feathered mist is tied to the waterfall base. No camera transforms.
    css='''.water{animation:water 2s linear infinite}.mote{animation:mote 10s ease-in-out infinite}.vapor{animation:vapor 12s ease-in-out infinite}@keyframes water{to{transform:translateY(64px)}}@keyframes mote{0%,100%{opacity:0;transform:translate(0,0)}20%{opacity:.52}75%{opacity:.4;transform:translate(var(--dx),var(--dy))}}@keyframes vapor{50%{transform:translate(18px,-5px);opacity:.65}}@media(prefers-reduced-motion:reduce){*{animation:none!important}.mote{opacity:.24}}'''
    # Name and role read as a film title, not an overlay card. Native text is sharp.
    out=f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1600" height="640" viewBox="0 0 1600 640" role="img" aria-labelledby="title desc"><title id="title">Arun Prasath</title><desc id="desc">Floating mountain ruins with flowing waterfalls, rising mist and drifting particles. Backend engineering, applied AI and MLOps.</desc><defs>{''.join(defs)}<clipPath id="frame"><rect width="1600" height="640"/></clipPath><linearGradient id="title-shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c1712" stop-opacity="0"/><stop offset=".55" stop-color="#0c1712" stop-opacity="0"/><stop offset="1" stop-color="#07110d" stop-opacity=".94"/></linearGradient><radialGradient id="mist"><stop stop-color="#e6f4e7" stop-opacity=".20"/><stop offset="1" stop-color="#e6f4e7" stop-opacity="0"/></radialGradient><style>{css}</style></defs><g clip-path="url(#frame)"><image width="1600" height="640" preserveAspectRatio="xMidYMid slice" xlink:href="{uri(plate,'webp')}"/>{''.join(layers)}<g class="vapor" opacity=".55"><ellipse cx="893" cy="557" rx="105" ry="27" fill="url(#mist)"/><ellipse cx="1458" cy="428" rx="74" ry="24" fill="url(#mist)"/><ellipse cx="1007" cy="355" rx="76" ry="23" fill="url(#mist)"/></g>{''.join(p)}<rect width="1600" height="640" fill="url(#title-shade)"/><text x="800" y="526" text-anchor="middle" fill="#fffdf1" font-family="Georgia,serif" font-size="100" font-weight="400">Arun Prasath</text><text x="800" y="583" text-anchor="middle" fill="#f3f5ed" font-family="Arial,sans-serif" font-size="32" font-weight="500">Backend engineering · Applied AI · MLOps</text><path d="M756 607H844" stroke="#c2a975" stroke-width="2"/></g></svg>'''
    ET.fromstring(out);(A/'ruins-hero.svg').write_text(out); print('Hero:',len(out.encode()),'bytes')

def build_river():
    """Second establishing shot. Water texture follows the foreground cascade."""
    plate=(A/'river-landscape.webp').read_bytes();w,h=1440,640
    # Feathered alpha mask along the water's curved edge, cut from this specific shot.
    x,y,mw,mh=572,499,202,141
    ma=Image.new('L',(mw,mh));d=ImageDraw.Draw(ma)
    d.polygon([(a-x,b-y) for a,b in [(581,511),(625,515),(653,537),(676,560),(699,611),(711,640),(674,640),(651,603),(625,555),(603,532)]],fill=200)
    d.polygon([(a-x,b-y) for a,b in [(712,526),(731,531),(748,560),(757,604),(765,640),(744,640),(733,590),(722,551)]],fill=180)
    ma=ma.filter(ImageFilter.GaussianBlur(4));rgba=Image.new('RGBA',(mw,mh),'white');rgba.putalpha(ma)
    src=Image.open(io.BytesIO(plate)).convert('L').crop((x,y,x+mw,y+mh));import PIL.ImageChops as IC
    tile=IC.subtract(src,src.filter(ImageFilter.GaussianBlur(5)),offset=128).resize((mw,64),Image.Resampling.BICUBIC)
    alpha=tile.point(lambda n:max(0,min(45,(n-118)*2)));tex=Image.new('RGBA',(mw,64),(239,250,244));tex.putalpha(alpha)
    u=png(tex);tiles=''.join(f'<image x="{x}" y="{y+i*64}" width="{mw}" height="64" xlink:href="{u}"/>' for i in range(-1,4))
    rng=random.Random(2717);motes=[]
    for i in range(18):
        xx=rng.randrange(400,1300);yy=rng.randrange(150,480)
        motes.append(f'<circle cx="{xx}" cy="{yy}" r="{rng.uniform(1,1.8):.1f}" fill="#fff1c5" class="mote" style="animation-delay:-{rng.uniform(0,10):.2f}s;animation-duration:{rng.randrange(7,13)}s"/>')
    css='''.cascade{animation:water 1.8s linear infinite}.mote{animation:mote 9s ease-in-out infinite}.mist{animation:mist 14s ease-in-out infinite}@keyframes water{to{transform:translateY(64px)}}@keyframes mote{0%,100%{opacity:0;transform:translate(0,0)}25%{opacity:.6}75%{opacity:.25;transform:translate(24px,-38px)}}@keyframes mist{50%{transform:translate(18px,-5px);opacity:.65}}@media(prefers-reduced-motion:reduce){*{animation:none!important}.mote{opacity:.2}}'''
    out=f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1440" height="640" viewBox="0 0 1440 640" role="img" aria-labelledby="title desc"><title id="title">The passage</title><desc id="desc">A sunlit stone passage above a river valley, with flowing water and drifting particles.</desc><defs><mask id="cascade" maskUnits="userSpaceOnUse" x="{x}" y="{y}" width="{mw}" height="{mh}" style="mask-type:alpha"><image x="{x}" y="{y}" width="{mw}" height="{mh}" xlink:href="{png(rgba)}"/></mask><radialGradient id="mist"><stop stop-color="#f6ebd6" stop-opacity=".14"/><stop offset="1" stop-color="#f6ebd6" stop-opacity="0"/></radialGradient><style>{css}</style></defs><image width="1440" height="640" xlink:href="{uri(plate,'webp')}"/><g mask="url(#cascade)"><g class="cascade">{tiles}</g></g><g class="mist" opacity=".38"><ellipse cx="1050" cy="467" rx="135" ry="30" fill="url(#mist)"/><ellipse cx="736" cy="616" rx="83" ry="27" fill="url(#mist)"/></g>{''.join(motes)}</svg>'''
    ET.fromstring(out);(A/'river-hero.svg').write_text(out);print('Passage:',len(out.encode()),'bytes')

def build_still():
    # Explicit picture-source fallback: no animated CSS, particles or water overlays.
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    root=ET.parse(A/'ruins-hero.svg').getroot()
    for parent in root.iter():
        for item in list(parent):
            if item.tag.rsplit('}',1)[-1] in ('style','mask') or item.attrib.get('class') in ('mote','vapor','water') or 'mask' in item.attrib:
                parent.remove(item)
    ET.ElementTree(root).write(A/'ruins-still.svg',encoding='unicode')

if __name__=='__main__':
    build();build_river();build_still()
