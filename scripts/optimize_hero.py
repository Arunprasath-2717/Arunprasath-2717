"""Build a compact, seamless animated WebP from the original six-frame CGI artwork.
Pillow is only needed for this optional offline asset build, not scheduled telemetry.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from math import cos, pi
ROOT=Path(__file__).resolve().parents[1]/'assets'
with Image.open(ROOT/'hero.gif') as im:
    source=[]
    for i in range(im.n_frames):
        im.seek(i)
        source.append(im.convert('RGB'))
# Lock typography and architecture to the reference. Only the energy paths
# and central ring transition between source frames, to avoid scene jitter.
base=source[0]
mask=Image.new('L',base.size)
d=ImageDraw.Draw(mask)
d.ellipse((228,83,455,260),fill=220)
d.polygon([(0,298),(37,286),(114,282),(178,252),(210,247),(208,278),(116,327),(0,358)],fill=220)
d.polygon([(115,177),(230,138),(262,149),(222,185),(138,219),(115,215)],fill=190)
d.polygon([(442,142),(560,146),(592,183),(545,205),(451,188)],fill=210)
mask=mask.filter(ImageFilter.GaussianBlur(13))
frames=[]
for i in range(48):
    phase=i*len(source)/48
    n=int(phase); f=phase-n
    t=(1-cos(pi*f))/2
    transition=Image.blend(source[n],source[(n+1)%len(source)],t)
    frames.append(Image.composite(transition,base,mask))
for quality in (78,72,65,58):
    out=ROOT/'hero-motion.webp'
    frames[0].save(out,format='WEBP',save_all=True,append_images=frames[1:],duration=[42 if i%3!=2 else 41 for i in range(48)],loop=0,quality=quality,method=4,minimize_size=True)
    if out.stat().st_size<600000:break
with Image.open(out) as im:
    assert im.is_animated and im.n_frames>=36
    print('Hero WebP:',im.size,im.n_frames,'frames;',out.stat().st_size,'bytes')
