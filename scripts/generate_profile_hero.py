#!/usr/bin/env python3
import io, urllib.request
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'assets/hero'; OUT.mkdir(parents=True,exist_ok=True)
URL='https://avatars.githubusercontent.com/u/228095676?v=4&size=1024'; CH=' .:-=+*#%@'
INFO=[('Name','Omar Arafa'),('Role','Full Stack PHP Developer'),('Based','Egypt'),('Major','Computer & Systems Engineering'),('University','Zagazig University'),('', ''),('BUILD.FOCUS',''),('Backend','PHP / Laravel / REST APIs / MySQL'),('Frontend','HTML / CSS / JavaScript / Bootstrap'),('Architecture','MVC / Service-Oriented'),('Hardware','PID / Sensors / Microcontrollers / IoT'),('Toolchain','Git / GitHub / VS Code / Arduino')]
PAL={'dark':('#0D1117','#161B22','#F0F6FC','#8B949E','#58A6FF','#79C0FF','#30363D'),'light':('#F6F8FA','#FFFFFF','#1F2328','#656D76','#0969DA','#218BFF','#D0D7DE')}

def avatar():
    r=urllib.request.Request(URL,headers={'User-Agent':'profile-hero'}); im=Image.open(io.BytesIO(urllib.request.urlopen(r,timeout=30).read())).convert('RGB')
    im=ImageOps.fit(im,(900,900),Image.Resampling.LANCZOS,centering=(.5,.43)); im=ImageOps.grayscale(im)
    im=ImageEnhance.Contrast(im).enhance(1.42); im=ImageEnhance.Brightness(im).enhance(1.04)
    return im.filter(ImageFilter.UnsharpMask(1.4,140,2))

def art(im,cols,rows):
    a=im.resize((cols,rows),Image.Resampling.LANCZOS); e=a.filter(ImageFilter.FIND_EDGES); p=a.load(); q=e.load(); out=[]
    for y in range(rows):
        s=''
        for x in range(cols):
            v=max(0,min(1,(255-p[x,y])/255*1.06+q[x,y]/255*.22-.05)); s+=CH[round(v*(len(CH)-1))]
        out.append(s)
    return out

def text_art(lines,x,y,lh):
    return '\n'.join(f'<tspan x="{x}" y="{y+i*lh:.2f}" xml:space="preserve">{escape(s)}</tspan>' for i,s in enumerate(lines))

def info_rows(x,y,lh,c,mobile):
    primary,muted,accent=c[2],c[3],c[4]; out=[f'<text x="{x}" y="{y}" class="head"><tspan fill="{primary}">omar@developer</tspan><tspan fill="{muted}"> --------------------------</tspan></text>']; i=1
    for k,v in INFO:
        if not k: i+=.65; continue
        yy=y+i*lh
        if k=='BUILD.FOCUS': out.append(f'<text x="{x}" y="{yy:.1f}" class="row sec" fill="{accent}">- BUILD.FOCUS --------------------</text>')
        else:
            vx=x+(126 if mobile else 134); out.append(f'<text x="{x}" y="{yy:.1f}" class="row"><tspan class="key" fill="{accent}">{escape(k)}:</tspan><tspan x="{vx}" fill="{primary}">{escape(v)}</tspan></text>')
        i+=1
    out.append(f'<text x="{x}" y="{y+i*lh+3:.1f}" class="foot" fill="{muted}">BRIDGING SOFTWARE &amp; HARDWARE</text>')
    return '\n'.join(out)

def svg(im,theme,mobile=False):
    bg0,bg1,primary,muted,accent,accent2,border=PAL[theme]
    if mobile:
        W,H=720,1080; tb=(20,20,680,42); vp=(48,94,624,350); ip=(48,470,624,526); clip=(58,122,604,312); ap=(84,54,180,132,5.7,6.6); sx,sy,slh=72,520,28; vt=(66,116); it=(66,492); fy=1045
    else:
        W,H=1180,610; tb=(3,3,1174,34); vp=(14,64,488,468); ip=(508,48,655,500); clip=(24,82,470,438); ap=(96,64,78,90,6.65,6.5); sx,sy,slh=528,82,21.5; vt=(30,62); it=(524,62); fy=585
    cols,rows,ax,ay,alh,afs=ap; px,py,pw,ph=clip; cx=px+pw*.52; cy=py+ph*(.43 if mobile else .48); rx=pw*(.36 if mobile else .45); ry=ph*(.24 if mobile else .29)
    tx,ty,tw,th=tb; vx,vy,vw,vh=vp; ix,iy,iw,ih=ip
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title description">
<title id="title">Omar Arafa - Full Stack PHP Developer</title><desc id="description">Terminal profile card with a static ASCII portrait generated from Omar's GitHub profile photo.</desc>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="{bg0}"/><stop offset="1" stop-color="{bg1}"/></linearGradient><linearGradient id="ascii" x2="1" y2="1"><stop stop-color="{primary}"/><stop offset="1" stop-color="{accent2}"/></linearGradient><linearGradient id="bd"><stop stop-color="{muted}"/><stop offset=".48" stop-color="{accent}"/><stop offset="1" stop-color="{muted}"/></linearGradient><radialGradient id="halo"><stop stop-color="{accent}" stop-opacity=".13"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient><pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse"><path d="M44 0H0V44" fill="none" stroke="{muted}" opacity=".09"/></pattern><clipPath id="pc"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12"/></clipPath><style>.mono,.ascii,.pt,.term,.live,.head,.row,.foot{{font-family:'Courier New',Consolas,monospace}}.ascii{{font-size:{afs}px;letter-spacing:-.15px;fill:url(#ascii)}}.pt{{font-size:{13 if mobile else 11}px;letter-spacing:2px;fill:{primary};opacity:.78}}.term{{font-size:{14 if mobile else 12}px;fill:{muted}}}.live{{font-size:{12 if mobile else 10}px;fill:{accent};letter-spacing:1px}}.head{{font-size:{17 if mobile else 16}px;font-weight:700}}.row,.foot{{font-size:{15 if mobile else 14}px}}.sec,.key{{font-weight:700}}text,tspan{{white-space:pre}}.orbit{{transform-box:view-box}}@keyframes a{{to{{transform:rotate(360deg)}}}}@keyframes b{{to{{transform:rotate(-360deg)}}}}@media(prefers-reduced-motion:no-preference){{.o1{{animation:a 42s linear infinite}}.o2{{animation:b 34s linear infinite}}}}</style></defs>
<rect width="{W}" height="{H}" rx="{22 if mobile else 18}" fill="url(#bg)"/><rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="{14 if mobile else 16}" fill="{bg1}" opacity=".9"/><circle cx="{tx+21}" cy="{ty+(21 if mobile else 17)}" r="5" fill="{accent}"/><circle cx="{tx+39}" cy="{ty+(21 if mobile else 17)}" r="5" fill="{muted}"/><circle cx="{tx+57}" cy="{ty+(21 if mobile else 17)}" r="5" fill="{muted}"/><text x="{W/2}" y="{47 if mobile else 25}" text-anchor="middle" class="term">omar@developer ~ % ./profile</text><circle cx="{571 if mobile else 1039}" cy="{41 if mobile else 20}" r="4" fill="{accent}"/><text x="{584 if mobile else 1049}" y="{45 if mobile else 24}" class="live">BUILDING</text>
<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="14" fill="{bg1}" opacity=".42" stroke="url(#bd)" stroke-opacity=".45"/><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="14" fill="{bg1}" opacity=".46" stroke="url(#bd)" stroke-opacity=".45"/><text x="{vt[0]}" y="{vt[1]}" class="pt">PORTRAIT / OMAR</text><text x="{it[0]}" y="{it[1]}" class="pt">PROFILE / ENGINEER</text>
<g clip-path="url(#pc)"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" fill="url(#grid)"/><ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#halo)"/><ellipse class="orbit o1" style="transform-origin:{cx:.1f}px {cy:.1f}px" cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="{primary}" stroke-dasharray="3 14" opacity=".13"/><ellipse class="orbit o2" style="transform-origin:{cx:.1f}px {cy:.1f}px" cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx*.78:.1f}" ry="{ry*.76:.1f}" fill="none" stroke="{muted}" stroke-dasharray="28 24" opacity=".1"/><text class="ascii">{text_art(art(im,cols,rows),ax,ay,alh)}</text></g>
{info_rows(sx,sy,slh,(bg0,bg1,primary,muted,accent,accent2,border),mobile)}
<text x="{W/2}" y="{fy}" text-anchor="middle" class="mono" font-family="'Courier New',Consolas,monospace" font-size="{13 if mobile else 11}" font-weight="700" letter-spacing="2" fill="{muted}">PHP / LARAVEL / MYSQL / JAVASCRIPT / EMBEDDED SYSTEMS / IOT</text></svg>'''

def main():
    im=avatar()
    for theme in ('dark','light'):
        for mobile in (False,True):
            name=f"omar-profile-v3{'-mobile' if mobile else ''}-{theme}.svg"; (OUT/name).write_text(svg(im,theme,mobile),encoding='utf-8'); print(name)
if __name__=='__main__': main()
