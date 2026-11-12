"""Täglicher MVP-Import öffentlicher Google-News-RSS-Ergebnisse in Supabase.
Keine LinkedIn-Scrapes. Quelleninhalte bitte vor redaktioneller Verwendung prüfen.
"""
import os, json, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

BASE=os.environ.get('SUPABASE_URL','').rstrip('/')
KEY=os.environ.get('SUPABASE_SECRET_KEY','')
if not BASE or not KEY: raise SystemExit('SUPABASE_URL und SUPABASE_SECRET_KEY fehlen')
# Fokussierte Suchanfragen mit Erkennung der wichtigen Hersteller.
QUERIES=[
 ('GZ Media','Hersteller',1,'"GZ Media" vinyl pressing innovation'),
 ('Sonopress & Topac','Hersteller',1,'Sonopress EcoRecord Smart Media pressing'),
 ('optimal media','Hersteller',1,'"optimal media" vinyl pressing packaging'),
 ('MPO International','Hersteller',2,'"MPO International" vinyl pressing'),
 ('Pallas & Vivid Vinyl','Hersteller',2,'"Pallas" "vinyl" pressing innovation'),
 ('Memphis Record Pressing','Hersteller',2,'"Memphis Record Pressing"'),
 ('United Record Pressing','Hersteller',2,'"United Record Pressing"'),
 ('National Audio Company','Hersteller',2,'"National Audio Company" cassette tape'),
 ('Record Industry','Hersteller',3,'"Record Industry" vinyl pressing Haarlem'),
 ('Noiseland Industries','Hersteller',3,'"Noiseland" vinyl pressing'),
 ('Media Duplication','Hersteller',3,'"Media Duplication" cassette UK'),
 ('','Vinyl',2,'vinyl record pressing new technology innovation'),
 ('','Packaging',2,'physical music packaging box set innovation'),
 ('','Nachhaltigkeit',2,'sustainable recycled vinyl record manufacturing'),
 ('','Markt',3,'vinyl CD physical music sales market report'),
 ('','Sony Music',2,'Sony Music limited edition vinyl box set physical release')]
HEADERS={'User-Agent':'PhysicalMusicRadar/1.0 (+public news reader)'}
def request(url,headers=None,body=None,method=None):
  req=urllib.request.Request(url,data=body,headers={**HEADERS,**(headers or {})},method=method)
  with urllib.request.urlopen(req,timeout=25) as response:return response.read()
def items_for(query):
  rss='https://news.google.com/rss/search?'+urllib.parse.urlencode({'q':query+' when:7d','hl':'en-US','gl':'US','ceid':'US:en'})
  root=ET.fromstring(request(rss))
  for item in root.findall('./channel/item')[:8]:
    title=item.findtext('title','').strip();url=item.findtext('link','').strip()
    source=item.find('source');name=source.text if source is not None else 'Google News'
    raw_date=item.findtext('pubDate','')
    try: date=parsedate_to_datetime(raw_date).astimezone(timezone.utc).isoformat()
    except: date=datetime.now(timezone.utc).isoformat()
    if title and url:yield dict(title=title[:450],summary='Neue öffentliche Meldung zum Thema. Bitte den Originalbeitrag aufrufen und redaktionell prüfen.',url=url,source=name or 'Google News',published_at=date)
rows={}
for manufacturer,category,priority,query in QUERIES:
  try:
    entries=list(items_for(query));print(f'{query}: {len(entries)}')
    for item in entries:
      item.update(manufacturer=manufacturer,category=category,priority=priority)
      # Deduplikation per URL, Hersteller-Meldung bei Überschneidungen bevorzugen.
      if item['url'] not in rows or priority<rows[item['url']]['priority']:rows[item['url']]=item
  except Exception as e:print('Query fehlgeschlagen:',query,repr(e))
if not rows:raise SystemExit('Keine Treffer. Datenbank unverändert.')
payload=json.dumps(list(rows.values()),ensure_ascii=False).encode('utf-8')
response = request(
    BASE + '/rest/v1/articles?on_conflict=url',
    {
        'apikey': KEY,
        'Content-Type': 'application/json',
        'Prefer': 'resolution=merge-duplicates,return=minimal'
    },
    payload,
    'POST'
)
print('Importiert/aktualisiert:',len(rows),'Meldungen')
