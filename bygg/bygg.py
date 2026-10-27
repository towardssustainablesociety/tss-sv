#!/usr/bin/env python3
"""TSS: bygger statisk webbplats från docx. python3 bygg.py SRC UT [--preview] [--noindex]

--preview  länkar till index.html (för att öppna filerna direkt i Safari) och noindex
--noindex  vanliga länkar, men sökmotorerna ombeds att inte indexera (före publicering)
Miljövariabel TSS_FORRAD: adress till förrådet på GitHub; ger en länk i sidfoten.
Licens: CC BY-SA 4.0 (se LICENSE)."""
import os, sys, re, shutil, subprocess, unicodedata, html, collections, datetime
import docx

SRC, OUT = sys.argv[1], sys.argv[2]
PREVIEW = '--preview' in sys.argv
NOINDEX = PREVIEW or '--noindex' in sys.argv
FORRAD = os.environ.get('TSS_FORRAD', '').strip()
LICENS = 'https://creativecommons.org/licenses/by-sa/4.0/deed.sv'
BASE = 'https://sv.towardssustainablesociety.org'
SITE = 'Mot ett hållbart samhälle – TSS'
SHORT = 'TSS'
START = 'Hållbart samhälle'
N = lambda s: unicodedata.normalize('NFC', s)

def slug(s):
    s = N(s).lower()
    for a, b in (('å','a'),('ä','a'),('ö','o'),('é','e'),('ü','u')): s = s.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def key(s):
    s = N(s).replace('\xa0', ' ').split(' – ')[0].split(' - Startsida')[0].strip().lower()
    return re.sub(r'\boch\b', 'o', s).replace('fn:s', 'fns')

# ---- sidor ----
pages = {}   # name -> dict
for r, d, f in os.walk(SRC):
    d.sort()
    for x in f:
        x2 = N(x)
        if not x2.endswith('.docx') or x2.startswith(('Navigera', '~$', '.')): continue
        name = x2[:-5]
        rel = N(os.path.relpath(r, SRC))
        if name != os.path.basename(rel): continue
        pages[name] = dict(name=name, rel=rel, docx=os.path.join(r, x))
pages['Samhällskartan'] = dict(name='Samhällskartan', rel='Vårt samhälle/Samhällskartan', docx=None)
for p in pages.values():
    parts = p['rel'].split('/')
    p['url'] = '' if p['name'] == START else '/'.join(slug(x) for x in parts) + '/'
    p['parent'] = os.path.dirname(p['rel'])
bykey = {key(n): p for n, p in pages.items()}
bykey['ramverket'] = pages['Ramverk']

def href(frm, to):
    """relativ länk från sida frm till sida to"""
    depth = frm['url'].count('/')
    h = '../' * depth + to['url']
    if PREVIEW: h += 'index.html'
    return h or './'

# ---- sid-id -> sida (från länktexterna) ----
idcount = collections.defaultdict(collections.Counter)
htmlcache = {}
for p in pages.values():
    if not p['docx']: continue
    h = subprocess.run(['pandoc', p['docx'], '-t', 'html', '--wrap=none'], capture_output=True, text=True, check=True).stdout
    htmlcache[p['name']] = h
    for sid, t in re.findall(r'href="https://sites\.google\.com[^"]*/p/([^/"]+)/edit"[^>]*>(.*?)</a>', h):
        k = key(re.sub('<[^>]+>', '', t))
        if k in bykey: idcount[sid][k] += 1
navfiles = {}
for r, d, f in os.walk(SRC):
    for x in f:
        if N(x) == 'Navigera i samhället.docx':
            navfiles[N(os.path.relpath(r, SRC))] = os.path.join(r, x)
            h = subprocess.run(['pandoc', os.path.join(r, x), '-t', 'html', '--wrap=none'], capture_output=True, text=True).stdout
            for sid, t in re.findall(r'href="https://sites\.google\.com[^"]*/p/([^/"]+)/edit"[^>]*>(.*?)</a>', h):
                k = key(re.sub('<[^>]+>', '', t))
                if k in bykey: idcount[sid][k] += 3
idmap = {sid: bykey[c.most_common(1)[0][0]] for sid, c in idcount.items()}
problems = []

# ---- navigering ----
# Navigera i samhället.docx visas inte längre (2026-10-27). Den används bara för sidornas ordning,
# tills ordningen får en egen fil.
def navlines(navpath):
    d = docx.Document(navpath)
    lines = []
    for para in d.paragraphs:
        for line in para.text.split('\n'):
            line = line.strip()
            if line: lines.append(line)
    return lines
navs = {rel: navlines(p) for rel, p in navfiles.items()}

# ---- toppmeny, brödsmulor (Du är här) och Sidorna i … sist på sidan ----
def order_children(par):
    """barnsidor till par, i den ordning de står i Navigera i samhället.docx (tills vidare)"""
    kids = [q for q in pages.values() if q['parent'] == par['rel'] and q is not par]
    seq = []
    for cand in (par['rel'],) + tuple(r for r in navs if os.path.dirname(r) == par['rel']):
        for line in navs.get(cand, []):
            t = bykey.get(key(line))
            if t in kids and t not in seq: seq.append(t)
    return seq + sorted((k for k in kids if k not in seq), key=lambda q: q['name'])
TOP = [pages[n] for n in ('Vårt samhälle', 'Samhällskartan', 'Samhällsutforskaren', 'Om TSS')]
byrel = {q['rel']: q for q in pages.values()}
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

# ---- bilder ----
imgs = {}
for r, d, f in os.walk(SRC):
    for x in f:
        if N(x).lower().endswith('.png'): imgs[N(x)] = os.path.join(r, x)
os.makedirs(os.path.join(OUT, 'bilder'), exist_ok=True)
def image(prefix):
    c = sorted(n for n in imgs if n.lower().startswith(prefix.lower()))
    if not c: return None
    n = c[-1]   # senaste datum i namnet
    out = slug(n[:-4]) + '.png'
    shutil.copyfile(imgs[n], os.path.join(OUT, 'bilder', out))
    return 'bilder/' + out

def figure(p, prefix, alt):
    src = image(prefix)
    if not src:
        problems.append(f'{p["name"]}: bild "{prefix}" saknas'); return ''
    up = '../' * p['url'].count('/')
    return f'<figure><img src="{up}{src}" alt="{html.escape(alt)}" loading="lazy"></figure>'

# ---- brödtext ----
def body(p):
    h = htmlcache.get(p['name'], '')
    h = re.sub(r'<h2([^>]*)><strong>(.*?)</strong></h2>', r'<h2\1>\2</h2>', h)
    def link(m):
        url, rest = m.group(1), m.group(2)
        s = re.search(r'sites\.google\.com/.*/p/([^/"]+)', url)
        if s:
            t = idmap.get(s.group(1))
            if not t:
                problems.append(f'{p["name"]}: okänd intern länk {s.group(1)}'); return f'<a href="#"{rest}>'
            return f'<a href="{href(p, t)}"{rest}>'
        if 'sites.google.com' in url:
            problems.append(f'{p["name"]}: Sites-länk {url}')
        if url.startswith('mailto:'): return f'<a href="{url}"{rest}>'
        return f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener"{rest}>'
    h = re.sub(r'<a href="([^"]+)"([^>]*)>', link, h)
    def bild(m):
        txt = html.unescape(m.group(1))
        first = txt.split(',')[0].strip()
        return figure(p, first, txt)
    h = re.sub(r'<p>\[BILD:\s*(.*?)\]</p>', bild, h)
    return h

def desc(h):
    m = re.search(r'<p>(.*?)</p>', h, re.S)
    t = re.sub('<[^>]+>', '', m.group(1)) if m else ''
    t = html.unescape(t).strip()
    return (t[:155].rsplit(' ', 1)[0] + ' …') if len(t) > 160 else t

TPL = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mall.html'), encoding='utf-8').read()
css_ok = shutil.copyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stil.css'), os.path.join(OUT, 'stil.css'))

for p in pages.values():
    b = body(p)
    if p['name'] == START:
        b = figure(p, 'Hållbart samhälle översikt', 'Hållbart samhälle – översiktsbild: ett gott liv för alla, inom planetens gränser') + b
    if p['name'] == 'Samhällskartan':
        b = figure(p, 'Samhällskartan', 'Samhällskartan: de fyra samhällssystemen med människan i mitten, den sociala grunden och planetens gränser') + b
    up = '../' * p['url'].count('/')
    title = START if p['name'] == START else p['name']
    head_title = SITE if p['name'] == START else f'{p["name"]} – {SHORT}'
    d = desc(b) or SITE
    og = image('Hållbart samhälle delningsbild')
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

# ---- länkkontroll ----
linked = collections.Counter()
for p in pages.values():
    for sid in re.findall(r'sites\.google\.com[^"]*/p/([^/"]+)/edit', htmlcache.get(p['name'], '')):
        if sid in idmap and idmap[sid] is not p: linked[idmap[sid]['name']] += 1
print(f'{len(pages)} sidor, {len(idmap)} kända sid-id, {len(imgs)} bilder')
for x in problems: print('PROBLEM:', x)
for n in pages:
    if not linked[n]: print('Ingen brödtext/Kopplingar-länk till:', n, '(nås via navigeringen)')
