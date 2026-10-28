#!/usr/bin/env python3
"""TSS: bygger statisk webbplats från markdown. python3 bygg.py SRC UT [--preview] [--noindex]

--preview  länkar till index.html (för att öppna filerna direkt i Safari) och noindex
--noindex  vanliga länkar, men sökmotorerna ombeds att inte indexera
Miljövariabel TSS_FORRAD: adress till förrådet på GitHub; ger en länk i sidfoten.
Kräver pandoc. Fungerar med Python 3.10.
Licens: CC BY-SA 4.0 (se LICENSE)."""
import os, sys, re, shutil, subprocess, unicodedata, html, collections, datetime
from urllib.parse import unquote

SRC, OUT = sys.argv[1], sys.argv[2]
PREVIEW = '--preview' in sys.argv
NOINDEX = PREVIEW or '--noindex' in sys.argv
FORRAD = os.environ.get('TSS_FORRAD', '').strip()
LICENS = 'https://creativecommons.org/licenses/by-sa/4.0/deed.sv'
BASE = 'https://sv.towardssustainablesociety.org'
SITE = 'Mot ett hållbart samhälle – TSS'
SHORT = 'TSS'
START = 'Hållbart samhälle'
ORDNING = 'Sidordning.md'
N = lambda s: unicodedata.normalize('NFC', s)
problems = []

def slug(s):
    s = N(s).lower()
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
TOP = [pages[n] for n in ('Vårt samhälle', 'Samhällskartan', 'Samhällsutforskaren', 'Om TSS')]
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
    return '<nav class="crumbs" aria-label="Du är här">' + ' <span class="sep">›</span> '.join(items) + '</nav>'
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
    title = f'Sidorna i {head["name"]}' if head is not p else 'Sidorna här'
    first = f'<li class="head"><span aria-current="page">{html.escape(head["name"])}</span></li>' if head is p else f'<li class="head"><a href="{href(p, head)}">{html.escape(head["name"])}</a></li>'
    return f'<h2 class="section">Sidorna i {html.escape(head["name"])}</h2><nav class="section" aria-label="{html.escape(title)}"><ul>{first}{"".join(li)}</ul></nav>'

# ---- bilder: ![beskrivning](fil.png) i texten, filen i sidans mapp ----
os.makedirs(os.path.join(OUT, 'bilder'), exist_ok=True)
nimgs = 0
def figure(p, src, alt):
    global nimgs
    path = os.path.normpath(os.path.join(SRC, p['rel'], unquote(html.unescape(src))))
    if not os.path.exists(path):
        problems.append(f'{p["name"]}: bilden "{src}" finns inte'); return ''
    out = slug(os.path.basename(path)[:-4]) + '.png'
    if not os.path.exists(os.path.join(OUT, 'bilder', out)): nimgs += 1
    shutil.copyfile(path, os.path.join(OUT, 'bilder', out))
    up = '../' * p['url'].count('/')
    return f'<figure><img src="{up}bilder/{out}" alt="{alt}" loading="lazy"></figure>'

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

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = open(os.path.join(HERE, 'mall.html'), encoding='utf-8').read()
shutil.copyfile(os.path.join(HERE, 'stil.css'), os.path.join(OUT, 'stil.css'))
og_src = os.path.join(SRC, START, 'Hållbart samhälle delningsbild 1200x630.png')
shutil.copyfile(og_src, os.path.join(OUT, 'bilder', 'hallbart-samhalle-delningsbild-1200x630.png'))
og = 'bilder/hallbart-samhalle-delningsbild-1200x630.png'

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
        '{{HOME}}': href(p, pages[START]), '{{KONTAKT}}': href(p, pages['Kontakt']),
        '{{TOP}}': topmenu(p), '{{CRUMBS}}': crumbs(p), '{{SECTION}}': section(p), '{{SITE}}': SITE, '{{BODY}}': b,
        '{{ROBOTS}}': '<meta name="robots" content="noindex">' if NOINDEX else '',
        '{{LICENS}}': LICENS,
        '{{FORRAD}}': f' · <a href="{html.escape(FORRAD, quote=True)}">Texterna på GitHub</a>' if FORRAD else '',
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
