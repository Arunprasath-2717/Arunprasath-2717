"""Build a self-contained cinematic SVG from the original rendered panorama.
Only the backdrop is raster; typography and continuous motion are native SVG.
"""
from pathlib import Path
import base64, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'

def build():
    image=base64.b64encode((ASSETS/'ruins-landscape.webp').read_bytes()).decode()
    out=f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1600" height="640" viewBox="0 0 1600 640" role="img" aria-labelledby="title desc">
<title id="title">Arun Prasath — beyond the clouds</title><desc id="desc">Cinematic floating mountains, overgrown stone ruins, waterfalls and a sunrise. Backend engineering, applied AI and MLOps.</desc>
<defs><clipPath id="frame"><rect width="1600" height="640" rx="12"/></clipPath>
<linearGradient id="shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#081b16" stop-opacity="0"/><stop offset=".56" stop-color="#081b16" stop-opacity=".02"/><stop offset="1" stop-color="#071511" stop-opacity=".92"/></linearGradient>
<radialGradient id="mist"><stop stop-color="#eaf4dd" stop-opacity=".22"/><stop offset="1" stop-color="#eaf4dd" stop-opacity="0"/></radialGradient>
<style>.camera{{transform-origin:800px 320px;animation:camera 18s ease-in-out infinite}} .mist{{animation:mist 14s ease-in-out infinite}} .fall{{animation:fall 1.8s linear infinite}} .bird{{animation:bird 15s linear infinite}} .spark{{animation:spark 4s ease-in-out infinite}} @keyframes camera{{0%,100%{{transform:scale(1.008)}}50%{{transform:translate(-8px,3px) scale(1.04)}}}} @keyframes mist{{0%,100%{{transform:translateX(-26px);opacity:.55}}50%{{transform:translateX(30px);opacity:.9}}}} @keyframes fall{{to{{stroke-dashoffset:-40}}}} @keyframes bird{{0%{{transform:translate(-80px,12px);opacity:0}}12%,88%{{opacity:.65}}100%{{transform:translate(360px,-35px);opacity:0}}}} @keyframes spark{{0%,100%{{opacity:.1}}50%{{opacity:.8}}}} @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style></defs>
<g clip-path="url(#frame)"><rect width="1600" height="640" fill="#173627"/><g class="camera"><image x="0" y="0" width="1600" height="640" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/webp;base64,{image}"/>
<g fill="none" stroke="#edf9ec" stroke-linecap="round" stroke-width="2.1" stroke-dasharray="12 28" opacity=".25" class="fall"><path d="M988 278Q995 310 995 346"/><path d="M891 433Q902 478 913 528"/><path d="M1008 414L1016 480"/><path d="M1460 289L1451 391"/></g>
<g class="mist"><ellipse cx="1120" cy="374" rx="210" ry="24" fill="url(#mist)"/><ellipse cx="1300" cy="480" rx="190" ry="34" fill="url(#mist)"/><ellipse cx="825" cy="545" rx="130" ry="30" fill="url(#mist)"/></g>
<g class="bird" fill="none" stroke="#253c2b" stroke-width="2" stroke-linecap="round"><path d="M1040 157q9 -8 18 0q8 -9 18 -2"/><path d="M1007 171q6 -5 12 0q6 -6 12 -1"/><path d="M1083 180q7 -6 14 0q7 -7 14 -1"/></g></g>
<rect width="1600" height="640" fill="url(#shade)"/><rect x="55" y="481" width="66" height="4" rx="2" fill="#dbcb8f"/><text x="55" y="465" font-size="17" letter-spacing="5" fill="#f4e6bf" font-family="system-ui,sans-serif" font-weight="600">AP / 2717</text>
<text x="52" y="558" fill="#fffef4" font-size="76" font-weight="700" font-family="Georgia,serif">Arun Prasath</text><text x="56" y="600" fill="#f5f4e6" font-size="26" font-family="system-ui,sans-serif">Backend Engineering  ·  Applied AI  ·  MLOps</text>
<text x="1544" y="603" text-anchor="end" font-size="15" font-family="system-ui,sans-serif" letter-spacing="3" fill="#e8e5d3">BEYOND THE CLOUDS</text></g></svg>'''
    ET.fromstring(out)
    (ASSETS/'ruins-hero.svg').write_text(out,encoding='utf-8')
    print('Hero SVG:',len(out),'bytes')
if __name__=='__main__':build()
