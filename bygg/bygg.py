#!/usr/bin/env python3
"""TSS: bygger statisk webbplats från markdown.
python3 bygg.py SRC UT [--preview] [--noindex] [--lang sv|en] [--namn FIL] [--sprak]

--preview  länkar till index.html (för att öppna filerna direkt i Safari) och noindex
--noindex  vanliga länkar, men sökmotorerna ombeds att inte indexera
--lang     språkversion: sv (TSS-sv, standard) eller en (TSS-en). Samma skript bygger båda.
--namn     namntabellen svenska ↔ engelska (standard: forvaltning/Ordlista svenska-engelska.md
           bredvid bygg/). Behövs för --sprak.
--sprak    slår på språklänken till motsvarande sida på det andra språket, hreflang och
           länken till språkvalet på www. Används när båda språkversionerna är publicerade.
Miljövariabel TSS_FORRAD: adress till förrådet på GitHub; ger en länk i sidfoten.
Kräver pandoc. Fungerar med Python 3.10.
Licens: CC BY-SA 4.0 (se LICENSE)."""
import os, sys, re, shutil, subprocess, unicodedata, html, collections, datetime
from urllib.parse import unquote

SRC, OUT = sys.argv[1], sys.argv[2]
PREVIEW = '--preview' in sys.argv
NOINDEX = PREVIEW or '--noindex' in sys.argv
FORRAD = os.environ.get('TSS_FORRAD', '').strip()
def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default
LANG = arg('--lang', 'sv')
SPRAK = '--sprak' in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
NAMN = arg('--namn', os.path.join(HERE, '..', 'forvaltning', 'Ordlista svenska-engelska.md'))
WWW = 'https://www.towardssustainablesociety.org/'

# Allt som skiljer språkversionerna åt. Sidnamnen följer namntabellen i forvaltning/.
SPRAKDATA = {
    'sv': dict(base='https://sv.towardssustainablesociety.org', site='Mot ett hållbart samhälle – TSS',
               start='Hållbart samhälle', top=('Vårt samhälle', 'Samhällskartan', 'Samhällsutforskaren', 'Om TSS'),
               kontakt='Kontakt', locale='sv_SE', licens='https://creativecommons.org/licenses/by-sa/4.0/deed.sv',
               licenstext='Texterna och bilderna får användas och byggas vidare på enligt',
               forrad='Texterna på GitHub', meny='Huvudmeny', duarhar='Du är här', sidorna='Sidorna i',
               sidornahar='Sidorna här', andra='In English', www='Andra språk – Other languages'),
    'en': dict(base='https://en.towardssustainablesociety.org', site='Towards Sustainable Society – TSS',
               start='Sustainable Society', top=('Our Society', 'The Society Map', 'Society Explorer', 'About TSS'),
               kontakt='Contact', locale='en_GB', licens='https://creativecommons.org/licenses/by-sa/4.0/deed.en',
               licenstext='The texts and images may be used and built upon under',
               forrad='The texts on GitHub', meny='Main menu', duarhar='You are here', sidorna='Pages in',
               sidornahar='Pages here', andra='På svenska', www='Other languages – Andra språk'),
}
L = SPRAKDATA[LANG]
OTHER = 'en' if LANG == 'sv' else 'sv'
LICENS = L['licens']
BASE = L['base']
SITE = L['site']
SHORT = 'TSS'
START = L['start']
ORDNING = 'Sidordning.md'
N = lambda s: unicodedata.normalize('NFC', s)
problems = []

def slug(s):
    s = N(s).lower().replace("'", '').replace('’', '')
    for a, b in (('å','a'),('ä','a'),('ö','o'),('é','e'),('ü','u')): s = s.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def pandoc(path):
    return subprocess.run(['pandoc', path, '-f', 'gfm', '-t', 'html', '--wrap=none'],
                          capture_output=True, text=True, check=True).stdout

# ---- sidor: en mapp per sida, och filen heter som mappen ----
pages = {}   # name -> dict
for r, d, f in os.walk(SRC):
    d.sort()
    for x in f:
        x2 = N(x)
        if not x2.endswith('.md') or x2.startswith(('~$', '.')): continue
        name = x2[:-3]
        rel = N(os.path.relpath(r, SRC))
        if name != os.path.basename(rel): continue
        pages[name] = dict(name=name, rel=rel, md=os.path.join(r, x))
for p in pages.values():
    p['url'] = '' if p['name'] == START else '/'.join(slug(x) for x in p['rel'].split('/')) + '/'
    p['parent'] = os.path.dirname(p['rel'])
byrel = {q['rel']: q for q in pages.values()}

def href(frm, to):
    """relativ länk från sida frm till sida to"""
    h = '../' * frm['url'].count('/') + to['url']
    if PREVIEW: h += 'index.html'
    return h or './'

# ---- ordningen: Sidordning.md ----
order = {}   # rel -> [rel, ...] barnsidor i ordning
def read_order():
    path = os.path.join(SRC, ORDNING)
    if not os.path.exists(path):
        problems.append(f'{ORDNING} saknas'); return
    stack, seen = [], set()   # (indrag, rel)
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^(\s*)[-*] (.+?)\s*$', N(line))
        if not m: continue
        ind, name = len(m.group(1).expandtabs(2)), m.group(2)
        while stack and stack[-1][0] >= ind: stack.pop()
        p = pages.get(name)
        if not p:
            problems.append(f'{ORDNING}: sidan "{name}" finns inte i mapparna'); continue
        if name in seen: problems.append(f'{ORDNING}: "{name}" står två gånger')
        seen.add(name)
        par = stack[-1][1] if stack else '.'
        if stack and p['parent'] != par:
            problems.append(f'{ORDNING}: "{name}" står under "{os.path.basename(par)}", men mappen ligger i "{p["parent"]}"')
        order.setdefault(p['parent'], []).append(p['rel'])
        stack.append((ind, p['rel']))
    for n in pages:
        if n not in seen: problems.append(f'{ORDNING}: sidan "{n}" saknas')
read_order()

def order_children(par):
    kids = [q for q in pages.values() if q['parent'] == par['rel'] and q is not par]
    seq = [byrel[r] for r in order.get(par['rel'], []) if byrel.get(r) in kids]
    return seq + sorted((k for k in kids if k not in seq), key=lambda q: q['name'])

# ---- toppmeny, brödsmulor (Du är här) och Sidorna i … sist på sidan ----
TOP = [pages[n] for n in L['top']]
def ancestors(p):
    out, r = [], p['parent']
    while r and r != '.':
        if r in byrel: out.insert(0, byrel[r])
        r = os.path.dirname(r)
    return out
def topmenu(p):
    anc = ancestors(p)
    out = []
    for t in TOP:
        if t is p: out.append(f'<span aria-current="page">{html.escape(t["name"])}</span>')
        else:
            cls = ' class="in"' if t in anc else ''
            out.append(f'<a href="{href(p, t)}"{cls}>{html.escape(t["name"])}</a>')
    return '\n'.join(out)
def crumbs(p):
    if p['name'] == START or p in TOP: return ''
    items = [f'<a href="{href(p, pages[START])}">{START}</a>'] + [f'<a href="{href(p, a)}">{html.escape(a["name"])}</a>' for a in ancestors(p)]
    items.append(f'<span aria-current="page">{html.escape(p["name"])}</span>')
    return f'<nav class="crumbs" aria-label="{L["duarhar"]}">' + ' <span class="sep">›</span> '.join(items) + '</nav>'
def section(p):
    kids = order_children(p)
    if kids:
        head, lst = p, kids
    else:
        par = byrel.get(p['parent'])
        if not par or par['name'] == START: return ''
        head, lst = par, order_children(par)
    if not lst: return ''
    li = []
    for q in lst:
        li.append(f'<li><span aria-current="page">{html.escape(q["name"])}</span></li>' if q is p else f'<li><a href="{href(p, q)}">{html.escape(q["name"])}</a></li>')
    title = f'{L["sidorna"]} {head["name"]}' if head is not p else L['sidornahar']
    first = f'<li class="head"><span aria-current="page">{html.escape(head["name"])}</span></li>' if head is p else f'<li class="head"><a href="{href(p, head)}">{html.escape(head["name"])}</a></li>'
    return f'<h2 class="section">{L["sidorna"]} {html.escape(head["name"])}</h2><nav class="section" aria-label="{html.escape(title)}"><ul>{first}{"".join(li)}</ul></nav>'

# ---- bilder: ![beskrivning](fil.png) i texten, filen i sidans mapp ----
os.makedirs(os.path.join(OUT, 'bilder'), exist_ok=True)
nimgs = 0
def figure(p, src, alt):
    global nimgs
    path = os.path.normpath(os.path.join(SRC, p['rel'], unquote(html.unescape(src))))
    if not os.path.exists(path):
        problems.append(f'{p["name"]}: bilden "{src}" finns inte'); return ''
    if path.endswith('.svg'): return inline_svg(p, path, alt)
    out = slug(os.path.basename(path)[:-4]) + '.png'
    if not os.path.exists(os.path.join(OUT, 'bilder', out)): nimgs += 1
    shutil.copyfile(path, os.path.join(OUT, 'bilder', out))
    up = '../' * p['url'].count('/')
    return f'<figure><img src="{up}bilder/{out}" alt="{alt}" loading="lazy"></figure>'

def inline_svg(p, path, alt):
    """SVG läggs in direkt i sidan, så att länkarna i bilden fungerar.
    Länkarna skrivs relativt till SVG-filens mapp, som länkarna i sidfilerna."""
    svgdir = N(os.path.relpath(os.path.dirname(path), SRC))
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'<\?xml[^>]*>\s*', '', s)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    def link(m):
        url = html.unescape(m.group(1))
        if url.startswith('#') or re.match(r'^[a-z]+:', url): return m.group(0)
        target = N(os.path.normpath(os.path.join(svgdir, unquote(url))))
        t = byrel.get(os.path.dirname(target)) if target.endswith('.md') else None
        if not t or os.path.basename(target) != t['name'] + '.md':
            problems.append(f'{p["name"]}: länken "{url}" i {os.path.basename(path)} hittar ingen sida'); return '<a href="#">'
        if t is not p: linked[t['name']] += 1
        return f'<a href="{href(p, t)}">'
    s = re.sub(r'<a href="([^"]+)">', link, s)
    s = s.replace('<svg ', f'<svg role="group" aria-label="{alt}" ', 1)
    return f'<figure class="karta">{s.strip()}</figure>'

# ---- brödtext ----
linked = collections.Counter()   # sida -> antal länkar från andra sidor
def body(p):
    h = pandoc(p['md'])
    def link(m):
        url, rest = html.unescape(m.group(1)), m.group(2)
        if url.startswith('mailto:'): return f'<a href="{html.escape(url, quote=True)}"{rest}>'
        if not re.match(r'^[a-z]+:', url):   # intern länk till en sidfil
            target = N(os.path.normpath(os.path.join(p['rel'], unquote(url))))
            t = byrel.get(os.path.dirname(target)) if target.endswith('.md') else None
            if not t or os.path.basename(target) != t['name'] + '.md':
                problems.append(f'{p["name"]}: länken "{url}" hittar ingen sida'); return f'<a href="#"{rest}>'
            if t is not p: linked[t['name']] += 1
            return f'<a href="{href(p, t)}"{rest}>'
        if 'sites.google.com' in url:
            problems.append(f'{p["name"]}: Sites-länk {url}')
        return f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener"{rest}>'
    h = re.sub(r'<a href="([^"]+)"([^>]*)>', link, h)
    h = re.sub(r'<li>(?!<p>)((?:(?!<li>|<ul>|<ol>).)*?)</li>', r'<li><p>\1</p></li>', h)   # samma radavstånd i alla listor
    h = re.sub(r'<p><img src="([^"]+)"\s+alt="([^"]*)"\s*/?></p>', lambda m: figure(p, m.group(1), m.group(2)), h)
    if re.search(r'<img(?![^>]*loading=)', h): problems.append(f'{p["name"]}: bild som inte står i ett eget stycke')
    return h

def desc(h):
    m = re.search(r'<p>(.*?)</p>', h, re.S)
    t = re.sub('<[^>]+>', '', m.group(1)) if m else ''
    t = html.unescape(t).strip()
    return (t[:155].rsplit(' ', 1)[0] + ' …') if len(t) > 160 else t

TPL = open(os.path.join(HERE, 'mall.html'), encoding='utf-8').read()
shutil.copyfile(os.path.join(HERE, 'stil.css'), os.path.join(OUT, 'stil.css'))
og_name = next((N(x) for x in sorted(os.listdir(os.path.join(SRC, START))) if '1200x630' in x and x.endswith('.png')), None)
og = ''
if og_name:
    og = 'bilder/' + slug(og_name[:-4]) + '.png'
    shutil.copyfile(os.path.join(SRC, START, og_name), os.path.join(OUT, og))
else: problems.append(f'delningsbilden (…1200x630.png) saknas i {START}')

# ---- andra språket: namntabellen ger motsvarande sida ----
def read_names():
    tab = {}
    try: lines = open(NAMN, encoding='utf-8').read().split('## Namntabell', 1)[1].split('\n## ', 1)[0].splitlines()
    except (OSError, IndexError):
        problems.append(f'namntabellen saknas ({NAMN})'); return tab
    for line in lines:
        c = [N(x.strip()) for x in line.strip().strip('|').split('|')]
        if len(c) == 2 and c[0] and c[0] not in ('Svenska', '---'):
            sv, en = c
            if LANG == 'sv': tab[sv] = en
            else: tab[en] = sv
    return tab
NAMES = read_names() if SPRAK else {}
OBASE = SPRAKDATA[OTHER]['base']
def other_url(p):
    if p['name'] == START: return OBASE + '/'
    parts = p['rel'].split('/')
    if any(x not in NAMES for x in parts):
        problems.append(f'{p["name"]}: saknas i namntabellen'); return OBASE + '/'
    return OBASE + '/' + '/'.join(slug(NAMES[x]) for x in parts) + '/'

for p in pages.values():
    b = body(p)
    up = '../' * p['url'].count('/')
    title = START if p['name'] == START else p['name']
    head_title = SITE if p['name'] == START else f'{p["name"]} – {SHORT}'
    d = desc(b) or SITE
    page = TPL
    for k, v in {
        '{{TITLE}}': html.escape(head_title), '{{H1}}': html.escape(title), '{{DESC}}': html.escape(d, quote=True),
        '{{CANON}}': BASE + '/' + p['url'], '{{OGIMG}}': BASE + '/' + og, '{{UP}}': up,
        '{{HOME}}': href(p, pages[START]), '{{KONTAKT}}': href(p, pages[L['kontakt']]),
        '{{KONTAKTNAMN}}': L['kontakt'], '{{LANG}}': LANG, '{{LOCALE}}': L['locale'], '{{MENY}}': L['meny'],
        '{{LICENSTEXT}}': L['licenstext'],
        '{{HREFLANG}}': (f'\n<link rel="alternate" hreflang="{LANG}" href="{BASE}/{p["url"]}">\n'
                         f'<link rel="alternate" hreflang="{OTHER}" href="{other_url(p)}">\n'
                         f'<link rel="alternate" hreflang="x-default" href="{WWW}">') if SPRAK else '',
        '{{SPRAKLANK}}': f'\n<a class="lang" href="{other_url(p)}" hreflang="{OTHER}" lang="{OTHER}">{L["andra"]}</a>' if SPRAK else '',
        '{{WWW}}': f' · <a href="{WWW}">{L["www"]}</a>' if SPRAK else '',
        '{{TOP}}': topmenu(p), '{{CRUMBS}}': crumbs(p), '{{SECTION}}': section(p), '{{SITE}}': SITE, '{{BODY}}': b,
        '{{ROBOTS}}': '<meta name="robots" content="noindex">' if NOINDEX else '',
        '{{LICENS}}': LICENS,
        '{{FORRAD}}': f' · <a href="{html.escape(FORRAD, quote=True)}">{L["forrad"]}</a>' if FORRAD else '',
    }.items():
        page = page.replace(k, v)
    os.makedirs(os.path.join(OUT, p['url']), exist_ok=True)
    with open(os.path.join(OUT, p['url'], 'index.html'), 'w', encoding='utf-8') as fh: fh.write(page)

# sitemap, robots, CNAME
today = datetime.date.today().isoformat()
with open(os.path.join(OUT, 'sitemap.xml'), 'w') as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p in sorted(pages.values(), key=lambda p: p['url']):
        fh.write(f'  <url><loc>{BASE}/{p["url"]}</loc><lastmod>{today}</lastmod></url>\n')
    fh.write('</urlset>\n')
with open(os.path.join(OUT, 'robots.txt'), 'w') as fh:
    if NOINDEX: fh.write('User-agent: *\nDisallow: /\n')
    else: fh.write(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')
with open(os.path.join(OUT, 'CNAME'), 'w') as fh: fh.write(BASE.split('//')[1] + '\n')

# ---- rapport ----
print(f'{len(pages)} sidor, {nimgs + 1} bilder')
for x in problems: print('PROBLEM:', x)
for n in pages:
    if not linked[n]: print('Ingen brödtext/Kopplingar-länk till:', n, '(nås via navigeringen)')
