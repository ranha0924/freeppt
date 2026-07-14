#!/usr/bin/env python3
"""
통합과학 LAB 소개 발표덱 빌더.

deck.src.html(플레이스홀더 템플릿)에
  - Galmuri 픽셀 폰트(사용 글자만 서브셋한 woff2)
  - 실제 화면 스크린샷(assets/*.png)
  - QR 코드(SVG)
를 모두 data URI로 인라인 삽입해 자기완결형 ../index.html 을 생성한다.

준비물:
  pip install fonttools brotli "qrcode[pil]"
  Galmuri TTF 4종을 src/fonts/ 에 둔다:
    Galmuri11.ttf, Galmuri11-Bold.ttf, Galmuri14.ttf, GalmuriMono11.ttf
  (npm pack galmuri 후 package/dist/ 에서 복사)

실행:  python src/build.py
"""
import base64, re, io
from pathlib import Path

BASE   = Path(__file__).resolve().parent      # src/
FONTS  = BASE / 'fonts'                        # Galmuri TTF 4종 (git 미포함)
ASSETS = BASE / 'assets'                       # 스크린샷
SRC    = BASE / 'deck.src.html'
OUT    = BASE.parent / 'index.html'            # 리포 루트

html = SRC.read_text(encoding='utf-8')

# ---------- 1. 서브셋 대상 글자 집합 ----------
# 소스에 등장하는 모든 문자(본문·data-title·alt 포함) + 기호 안전망 + ASCII
extra = "◆★▸◀▶←→↑↓·—…○●□■◐½×÷≈°′″ⁿ₂₃⁻⁺ⓘ✓✗“”‘’()[]{}%/\\|<>#&@:;,.!?~+-=*_ "
chars = set(html) | set(extra) | set(map(chr, range(0x20, 0x7f)))
charset = ''.join(sorted(chars))
print('charset size:', len(chars))

# ---------- 2. 폰트 서브셋 → woff2 base64 ----------
from fontTools import subset

def subset_font(ttf_name):
    path = FONTS / ttf_name
    if not path.exists():
        raise SystemExit(f"폰트 없음: {path}\n  Galmuri TTF를 src/fonts/ 에 두세요 (npm pack galmuri).")
    options = subset.Options()
    options.flavor = 'woff2'
    options.desubroutinize = True
    options.notdef_outline = True
    options.recalc_timestamp = False
    options.drop_tables += ['GSUB','GPOS','GDEF','kern','MERG','meta','sbix','CBDT','CBLC','EBDT','EBLC']
    font = subset.load_font(str(path), options)
    ss = subset.Subsetter(options=options)
    ss.populate(text=charset)
    ss.subset(font)
    buf = io.BytesIO()
    subset.save_font(font, buf, options)
    b = buf.getvalue()
    print(f'  {ttf_name}: {len(b)//1024} KB (woff2 subset)')
    return 'data:font/woff2;base64,' + base64.b64encode(b).decode('ascii')

print('subsetting fonts...')
FONTMAP = {
    '__G11__':   'Galmuri11.ttf',
    '__G11B__':  'Galmuri11-Bold.ttf',
    '__G14__':   'Galmuri14.ttf',
    '__GMONO__': 'GalmuriMono11.ttf',
}
FONTS_OUT = {k: subset_font(v) for k, v in FONTMAP.items()}

# ---------- 3. 이미지 → png base64 ----------
IMG_FILES = {
    '__IMG_HOME__':       'shot-home.png',
    '__IMG_INDEX__':      'nav-1-index.png',
    '__IMG_CONCEPT__':    'exp-mech-concept.png',
    '__IMG_CONCEPT2__':   'exp-mech-concept.png',
    '__IMG_EXPERIENCE__': 'exp-mech-freefall-run.png',
    '__IMG_QUIZ__':       'exp-mech-quiz.png',
    '__IMG_FREEFALL__':   'exp-mech-freefall-run.png',
    '__IMG_DNA__':        'el-dna-stage.png',
    '__IMG_SPECTRUM__':   'el-spectrum-stage.png',
    '__IMG_STELLAR__':    'el-stellar-stage.png',
    '__IMG_AUTHOR__':     'author-form-crop.png',
}
cache = {}
def img_uri(fn):
    if fn not in cache:
        b = (ASSETS / fn).read_bytes()
        cache[fn] = 'data:image/png;base64,' + base64.b64encode(b).decode('ascii')
    return cache[fn]
print('embedding images...')
IMGS = {k: img_uri(v) for k, v in IMG_FILES.items()}

# ---------- 4. QR 코드 (SVG, PIL 불필요) ----------
import qrcode, qrcode.image.svg
qr = qrcode.QRCode(border=1, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data('https://free-fall-experiment.vercel.app/')
qr.make(fit=True)
qr_svg = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage).to_string(encoding='unicode')
qr_svg = re.sub(r'<\?xml[^>]*\?>', '', qr_svg).strip()
qr_svg = re.sub(r'width="[^"]*"', 'width="100%"', qr_svg, count=1)
qr_svg = re.sub(r'height="[^"]*"', 'height="100%"', qr_svg, count=1)
if 'preserveAspectRatio' not in qr_svg:
    qr_svg = qr_svg.replace('<svg ', '<svg preserveAspectRatio="xMidYMid meet" ', 1)
qr_svg = qr_svg.replace('fill="#ffffff"', 'fill="none"').replace('fill:#ffffff', 'fill:none')
qr_svg = re.sub(r'(<path )', r'\1fill="#000000" ', qr_svg, count=1)

# ---------- 5. 치환 & 저장 ----------
for k, v in {**FONTS_OUT, **IMGS}.items():
    if k not in html:
        print('WARN placeholder not found:', k)
    html = html.replace(k, v)
html = html.replace('__QR_SVG__', qr_svg)

leftover = re.findall(r'__[A-Z0-9_]+__', html)
if leftover:
    print('LEFTOVER placeholders:', set(leftover))

OUT.write_text(html, encoding='utf-8')
print('WROTE', OUT, f'{OUT.stat().st_size//1024} KB')
