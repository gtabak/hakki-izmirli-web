#!/usr/bin/env python3
"""Basic deployment preflight: multilingual/static/SEO completeness and internal links."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
import json
base=Path(__file__).resolve().parents[1]/'public'
pages=list(base.rglob('index.html'))
errs=[]
for p in pages:
 s=BeautifulSoup(p.read_text(encoding='utf8'),'html.parser')
 rel='/'+str(p.parent.relative_to(base)).replace('\\','/').strip('/')+'/'
 if rel in ('//','/./'):rel='/'
 for q in ['html[lang]','title','meta[name=description]','link[rel=canonical]','meta[property="og:title"]','h1','link[hreflang=x-default]']:
  if not s.select_one(q):errs.append(f'{rel}: missing {q}')
 if len(s.select('link[rel=alternate][hreflang]'))!=9:errs.append(f'{rel}: need 9 hreflangs')
 if len(s.select('h1'))!=1:errs.append(f'{rel}: h1 count={len(s.select("h1"))}')
 canon=s.select_one('link[rel=canonical]')
 if canon and not canon.get('href','').endswith(rel):errs.append(f'{rel}: canonical mismatch')
 for a in s.select('a[href]'):
  u=a.get('href','')
  if not u.startswith('/') or u.startswith('//'):continue
  target=base / u.lstrip('/')
  if target.is_dir(): target=target/'index.html'
  if not target.exists():errs.append(f'{rel}: broken internal href {u}')
 for script in s.select('script[type="application/ld+json"]'):
  try:json.loads(script.text)
  except Exception as e:errs.append(f'{rel}: schema invalid {str(e)[:70]}')
if len(pages)!=120:errs.append(f'Expected 120 pages, found {len(pages)}')
for required in ['assets/style.css','assets/site.js','_redirects','_headers','sitemap.xml','robots.txt','en/index.html','index.html']:
 if not (base/required).exists():errs.append(f'Missing asset {required}')
try:
 root=ET.parse(base/'sitemap.xml').getroot()
 urls=root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
 if len(urls)!=120:errs.append(f'Sitemap has {len(urls)} URLs')
except Exception as e:errs.append(f'Sitemap invalid: {e}')
print(f'Checked {len(pages)} pages, 8 locales, sitemap, internal links, metadata and schemas')
if errs:
 print('\n'.join(errs[:50]))
 raise SystemExit(f'FAILED with {len(errs)} issue(s)')
print('PASS — structural static-site checks')
