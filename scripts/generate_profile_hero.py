#!/usr/bin/env python3
"""Generate the responsive v9 terminal hero used by the profile README."""

from __future__ import annotations

import io
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "hero"
OUT.mkdir(parents=True, exist_ok=True)

AVATAR_URL = "https://avatars.githubusercontent.com/u/228095676?v=4&size=1024"
ASCII_RAMP = "  ..`,:;i1tfLCG08@"


def download_avatar() -> Image.Image:
    request = urllib.request.Request(
        AVATAR_URL,
        headers={"User-Agent": "omar-profile-hero-generator"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return Image.open(io.BytesIO(response.read())).convert("RGB")


def isolate_portrait(image: Image.Image) -> Image.Image:
    """Keep the complete portrait while muting the busy photo background."""
    image = ImageOps.fit(
        image,
        (920, 920),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )

    # The GitHub avatar is a stable square portrait. This soft silhouette follows
    # the full visible figure from the cap down to the bottom of the photo.
    polygon = [
        (300, 0), (485, 0), (535, 72), (555, 155), (540, 264),
        (512, 302), (584, 332), (655, 382), (686, 470), (677, 568),
        (652, 635), (626, 640), (610, 920), (274, 920), (232, 845),
        (208, 720), (190, 575), (182, 458), (199, 390), (256, 337),
        (316, 302), (292, 245), (286, 157),
    ]
    mask = Image.new("L", image.size, 0)
    ImageDraw.Draw(mask).polygon(polygon, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(10))

    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray, cutoff=(0.6, 0.8))
    gray = ImageEnhance.Contrast(gray).enhance(1.55)
    gray = ImageEnhance.Brightness(gray).enhance(1.05)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=1.25, percent=165, threshold=2))

    clean = Image.new("L", image.size, 255)
    clean.paste(gray, mask=mask)

    # Allocate the available character grid to Omar instead of the empty sides
    # of the square avatar. Larger glyphs remain crisp at GitHub's display size.
    return clean.crop((150, 0, 720, 920))


def ascii_art(image: Image.Image, columns: int, rows: int) -> list[str]:
    sample = image.resize((columns, rows), Image.Resampling.LANCZOS)
    edges = sample.filter(ImageFilter.FIND_EDGES)
    pixels = sample.load()
    edge_pixels = edges.load()
    lines: list[str] = []

    for y in range(rows):
        line = []
        for x in range(columns):
            darkness = (255 - pixels[x, y]) / 255
            edge = 0.0 if x in (0, columns - 1) or y in (0, rows - 1) else edge_pixels[x, y] / 255
            edge_detail = edge * 0.24 * min(1.0, darkness * 3.0)
            density = max(
                0.0,
                min(0.76, (darkness ** 1.55) * 0.78 + edge_detail - 0.075),
            )
            index = round(density * (len(ASCII_RAMP) - 1))
            line.append(ASCII_RAMP[index])
        lines.append("".join(line).rstrip())

    non_empty = [index for index, line in enumerate(lines) if line.strip()]
    if not non_empty:
        return lines
    return lines[non_empty[0] : non_empty[-1] + 1]


def tspans(lines: list[str], x: float, y: float, line_height: float) -> str:
    return "\n".join(
        f'<tspan x="{x}" y="{y + index * line_height:.2f}" '
        f'xml:space="preserve">{escape(line)}</tspan>'
        for index, line in enumerate(lines)
    )


def desktop_svg(portrait: Image.Image) -> str:
    art = ascii_art(portrait, 84, 94)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="735" viewBox="0 0 1280 735" role="img" aria-labelledby="title description">
<title id="title">Omar Arafa — Full Stack PHP Developer</title>
<desc id="description">Large premium terminal card with a high-detail, full-frame ASCII portrait of Omar Arafa.</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0D1117"/><stop offset="1" stop-color="#07111E"/></linearGradient>
  <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#111A25" stop-opacity=".94"/><stop offset="1" stop-color="#0B141F" stop-opacity=".96"/></linearGradient>
  <linearGradient id="blue" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#A5D6FF"/><stop offset=".48" stop-color="#58A6FF"/><stop offset="1" stop-color="#2F81F7"/></linearGradient>
  <linearGradient id="ascii" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#E6EDF3"/><stop offset=".52" stop-color="#AAB7C4"/><stop offset="1" stop-color="#8B949E"/></linearGradient>
  <linearGradient id="border" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#30363D"/><stop offset=".5" stop-color="#58A6FF"/><stop offset="1" stop-color="#30363D"/></linearGradient>
  <radialGradient id="halo"><stop stop-color="#58A6FF" stop-opacity=".16"/><stop offset="1" stop-color="#58A6FF" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#58A6FF" stroke-opacity=".05"/></pattern>
  <clipPath id="portraitClip"><rect x="42" y="196" width="526" height="420" rx="12"/></clipPath>
  <filter id="nameGlow" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <style>
    .mono,.ascii,.tiny,.key,.value,.sec,.foot{{font-family:'Courier New',Consolas,monospace}}
    .ascii{{font-size:7.25px;letter-spacing:-.25px;fill:url(#ascii)}}
    .tiny{{font-size:11px;letter-spacing:2px;fill:#8B949E}}
    .key{{font-size:15px;font-weight:700;fill:#58A6FF}}
    .value{{font-size:15px;font-weight:700;fill:#F0F6FC}}
    .sec{{font-size:11px;font-weight:700;letter-spacing:2.2px;fill:#8B949E}}
    .foot{{font-size:11px;letter-spacing:1.8px;fill:#8B949E}}
    @keyframes pulse{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
    @keyframes scan{{0%{{transform:translateY(-178px);opacity:0}}15%,85%{{opacity:.75}}100%{{transform:translateY(190px);opacity:0}}}}
    .pulse{{animation:pulse 2.2s ease-in-out infinite}}.scan{{animation:scan 6.2s linear infinite}}
  </style>
</defs>
<rect width="1280" height="735" rx="24" fill="url(#bg)"/>
<rect x="5" y="5" width="1270" height="725" rx="21" fill="none" stroke="#30363D"/>
<text x="640" y="42" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="27" font-weight="800" letter-spacing="6" fill="url(#blue)" filter="url(#nameGlow)">OMAR ARAFA</text>
<text x="640" y="62" text-anchor="middle" class="mono" font-size="9.5" font-weight="700" letter-spacing="2.6" fill="#79C0FF">FULL STACK PHP DEVELOPER • COMPUTER &amp; SYSTEMS ENGINEER</text>
<rect x="22" y="78" width="1236" height="44" rx="12" fill="#101823" stroke="#21262D"/>
<circle cx="47" cy="100" r="5" fill="#FF7B72"/><circle cx="65" cy="100" r="5" fill="#D29922"/><circle cx="83" cy="100" r="5" fill="#3FB950"/>
<text x="113" y="104" class="mono" font-size="12" fill="#8B949E">omar@developer ~ % ./profile --full-frame</text>
<circle cx="1142" cy="100" r="4.5" fill="#58A6FF" class="pulse"/><text x="1157" y="104" class="mono" font-size="10" font-weight="700" letter-spacing="2" fill="#58A6FF">BUILDING</text>

<rect x="22" y="138" width="566" height="514" rx="16" fill="url(#panel)" stroke="url(#border)" stroke-opacity=".64"/>
<rect x="602" y="138" width="656" height="514" rx="16" fill="url(#panel)" stroke="url(#border)" stroke-opacity=".55"/>
<text x="42" y="164" class="sec">PORTRAIT / OMAR — COMPLETE FRAME</text><text x="622" y="164" class="sec">PROFILE / ENGINEER</text>
<line x1="42" y1="176" x2="568" y2="176" stroke="#21262D"/><line x1="622" y1="176" x2="1238" y2="176" stroke="#21262D"/>

<g clip-path="url(#portraitClip)">
  <rect x="42" y="196" width="526" height="420" rx="12" fill="url(#grid)"/>
  <text x="305" y="392" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="96" font-weight="900" letter-spacing="10" fill="#58A6FF" opacity=".025">OMAR</text>
  <ellipse cx="305" cy="405" rx="218" ry="180" fill="url(#halo)"/>
  <text class="ascii" transform="translate(4 0) scale(1.07 1)">{tspans(art, 118, 194, 4.48)}</text>
  <rect x="72" y="358" width="466" height="1.2" fill="url(#blue)" opacity=".56" class="scan"/>
</g>
<rect x="42" y="619" width="526" height="18" rx="7" fill="#0B1521" stroke="#1F6FEB" stroke-opacity=".7"/>
<text x="305" y="632" text-anchor="middle" class="mono" font-size="9.3" font-weight="700" letter-spacing="1.35" fill="#79C0FF">COMPLETE FRAME • CLEAN ASCII • GITHUB OPTIMIZED</text>

<text x="622" y="211" class="mono" font-size="15" font-weight="700" fill="#F0F6FC">omararafa295-cmd</text>
<text x="622" y="251" class="key">Name:</text><text x="780" y="251" class="value">Omar Arafa</text>
<text x="622" y="284" class="key">Role:</text><text x="780" y="284" class="value">Full Stack PHP Developer</text>
<text x="622" y="317" class="key">Major:</text><text x="780" y="317" class="value">Computer &amp; Systems Engineering</text>
<text x="622" y="350" class="key">University:</text><text x="780" y="350" class="value">Zagazig University</text>
<text x="622" y="383" class="key">Based:</text><text x="780" y="383" class="value">Egypt</text>
<line x1="622" y1="407" x2="1238" y2="407" stroke="#21262D"/>
<text x="622" y="431" class="sec">BUILD.FOCUS</text>
<text x="622" y="468" class="key">Backend:</text><text x="780" y="468" class="value">PHP / Laravel / RESTful APIs / MySQL</text>
<text x="622" y="501" class="key">Frontend:</text><text x="780" y="501" class="value">HTML / CSS / JavaScript / Bootstrap</text>
<text x="622" y="534" class="key">Architecture:</text><text x="780" y="534" class="value">MVC / Service-Oriented Design</text>
<text x="622" y="567" class="key">Hardware:</text><text x="780" y="567" class="value">PID / Sensors / Microcontrollers / IoT</text>
<text x="622" y="600" class="key">Toolchain:</text><text x="780" y="600" class="value">Git / GitHub / VS Code / Arduino</text>

<rect x="22" y="670" width="1236" height="40" rx="10" fill="#0E1621" stroke="#21262D"/>
<rect x="22" y="670" width="1236" height="1.5" fill="url(#blue)" opacity=".8"/>
<text x="640" y="695" text-anchor="middle" class="foot">PHP / LARAVEL / MYSQL / JAVASCRIPT / BOOTSTRAP / EMBEDDED SYSTEMS / IOT</text>
</svg>'''


def mobile_svg(portrait: Image.Image) -> str:
    art = ascii_art(portrait, 84, 94)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="1180" viewBox="0 0 720 1180" role="img" aria-labelledby="title description">
<title id="title">Omar Arafa — Full Stack PHP Developer</title>
<desc id="description">Mobile premium terminal card with a large, full-frame ASCII portrait of Omar Arafa.</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0D1117"/><stop offset="1" stop-color="#07111E"/></linearGradient>
  <linearGradient id="panel" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#111A25"/><stop offset="1" stop-color="#0B141F"/></linearGradient>
  <linearGradient id="blue"><stop stop-color="#A5D6FF"/><stop offset=".5" stop-color="#58A6FF"/><stop offset="1" stop-color="#2F81F7"/></linearGradient>
  <linearGradient id="ascii" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#E6EDF3"/><stop offset=".52" stop-color="#AAB7C4"/><stop offset="1" stop-color="#8B949E"/></linearGradient>
  <linearGradient id="border"><stop stop-color="#30363D"/><stop offset=".5" stop-color="#58A6FF"/><stop offset="1" stop-color="#30363D"/></linearGradient>
  <radialGradient id="halo"><stop stop-color="#58A6FF" stop-opacity=".16"/><stop offset="1" stop-color="#58A6FF" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="#58A6FF" stroke-opacity=".05"/></pattern>
  <clipPath id="portraitClip"><rect x="50" y="198" width="620" height="438" rx="12"/></clipPath>
  <filter id="nameGlow" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <style>
    .mono,.ascii,.key,.value,.sec,.foot{{font-family:'Courier New',Consolas,monospace}}
    .ascii{{font-size:7.6px;letter-spacing:-.22px;fill:url(#ascii)}}
    .key{{font-size:15px;font-weight:700;fill:#58A6FF}}.value{{font-size:15px;font-weight:700;fill:#F0F6FC}}
    .sec{{font-size:11px;font-weight:700;letter-spacing:2.2px;fill:#8B949E}}.foot{{font-size:11px;letter-spacing:1.8px;fill:#8B949E}}
    @keyframes pulse{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}@keyframes scan{{0%{{transform:translateY(-185px);opacity:0}}15%,85%{{opacity:.75}}100%{{transform:translateY(195px);opacity:0}}}}
    .pulse{{animation:pulse 2.2s ease-in-out infinite}}.scan{{animation:scan 6.2s linear infinite}}
  </style>
</defs>
<rect width="720" height="1180" rx="24" fill="url(#bg)"/><rect x="5" y="5" width="710" height="1170" rx="21" fill="none" stroke="#30363D"/>
<text x="360" y="43" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="27" font-weight="800" letter-spacing="6" fill="url(#blue)" filter="url(#nameGlow)">OMAR ARAFA</text>
<text x="360" y="63" text-anchor="middle" class="mono" font-size="9.5" font-weight="700" letter-spacing="2.3" fill="#79C0FF">FULL STACK PHP DEVELOPER • SYSTEMS ENGINEER</text>
<rect x="24" y="80" width="672" height="44" rx="12" fill="#101823" stroke="#21262D"/>
<circle cx="48" cy="102" r="5" fill="#FF7B72"/><circle cx="66" cy="102" r="5" fill="#D29922"/><circle cx="84" cy="102" r="5" fill="#3FB950"/>
<text x="108" y="106" class="mono" font-size="11" fill="#8B949E">omar@developer ~ % ./profile</text><circle cx="602" cy="102" r="4.5" fill="#58A6FF" class="pulse"/><text x="617" y="106" class="mono" font-size="9" font-weight="700" letter-spacing="1.5" fill="#58A6FF">BUILDING</text>

<rect x="32" y="144" width="656" height="526" rx="16" fill="url(#panel)" stroke="url(#border)" stroke-opacity=".64"/>
<text x="50" y="171" class="sec">PORTRAIT / OMAR — COMPLETE FRAME</text><line x1="50" y1="184" x2="670" y2="184" stroke="#21262D"/>
<g clip-path="url(#portraitClip)"><rect x="50" y="198" width="620" height="438" rx="12" fill="url(#grid)"/><text x="360" y="405" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="105" font-weight="900" letter-spacing="10" fill="#58A6FF" opacity=".025">OMAR</text><ellipse cx="360" cy="414" rx="245" ry="190" fill="url(#halo)"/>
<text class="ascii" transform="translate(14 0) scale(1.10 1)">{tspans(art, 104, 198, 4.62)}</text><rect x="82" y="366" width="556" height="1.2" fill="url(#blue)" opacity=".56" class="scan"/></g>
<rect x="50" y="640" width="620" height="18" rx="7" fill="#0B1521" stroke="#1F6FEB" stroke-opacity=".7"/><text x="360" y="653" text-anchor="middle" class="mono" font-size="9.3" font-weight="700" letter-spacing="1.25" fill="#79C0FF">COMPLETE FRAME • CLEAN ASCII • GITHUB OPTIMIZED</text>

<rect x="32" y="690" width="656" height="398" rx="16" fill="url(#panel)" stroke="url(#border)" stroke-opacity=".55"/>
<text x="50" y="718" class="sec">PROFILE / ENGINEER</text><line x1="50" y1="731" x2="670" y2="731" stroke="#21262D"/>
<text x="50" y="763" class="mono" font-size="15" font-weight="700" fill="#F0F6FC">omararafa295-cmd</text>
<text x="50" y="800" class="key">Name:</text><text x="210" y="800" class="value">Omar Arafa</text>
<text x="50" y="829" class="key">Role:</text><text x="210" y="829" class="value">Full Stack PHP Developer</text>
<text x="50" y="858" class="key">Major:</text><text x="210" y="858" class="value">Computer &amp; Systems Engineering</text>
<text x="50" y="887" class="key">University:</text><text x="210" y="887" class="value">Zagazig University</text>
<text x="50" y="916" class="key">Based:</text><text x="210" y="916" class="value">Egypt</text>
<line x1="50" y1="939" x2="670" y2="939" stroke="#21262D"/><text x="50" y="963" class="sec">BUILD.FOCUS</text>
<text x="50" y="995" class="key">Backend:</text><text x="210" y="995" class="value">PHP / Laravel / APIs / MySQL</text>
<text x="50" y="1024" class="key">Frontend:</text><text x="210" y="1024" class="value">HTML / CSS / JS / Bootstrap</text>
<text x="50" y="1053" class="key">Toolchain:</text><text x="210" y="1053" class="value">Git / GitHub / VS Code / Arduino</text>

<rect x="24" y="1110" width="672" height="42" rx="10" fill="#0E1621" stroke="#21262D"/><rect x="24" y="1110" width="672" height="1.5" fill="url(#blue)" opacity=".8"/><text x="360" y="1136" text-anchor="middle" class="foot">PHP / LARAVEL / MYSQL / JAVASCRIPT / EMBEDDED SYSTEMS / IOT</text>
</svg>'''


def main() -> None:
    portrait = isolate_portrait(download_avatar())
    files = {
        "omar-profile-v9.svg": desktop_svg(portrait),
        "omar-profile-v9-mobile.svg": mobile_svg(portrait),
    }
    for name, contents in files.items():
        svg_path = OUT / name
        svg_path.write_text(contents, encoding="utf-8")
        print(name)

        # GitHub scales README images to fractional sizes. A 2x raster copy keeps
        # the ASCII glyphs crisp and avoids colored sub-pixel fringes in browsers.
        try:
            import cairosvg
        except ImportError:
            continue

        width, height = ((1440, 2360) if "mobile" in name else (2560, 1470))
        png_path = svg_path.with_suffix(".png")
        cairosvg.svg2png(
            bytestring=contents.encode("utf-8"),
            write_to=str(png_path),
            output_width=width,
            output_height=height,
        )
        print(png_path.name)


if __name__ == "__main__":
    main()
