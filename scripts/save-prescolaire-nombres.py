from pathlib import Path
import json,re,sys
p=Path(__file__).resolve().parents[1];age=int(sys.argv[1]);suffix=sys.argv[2];summary=sys.argv[3]
f=f'prescolaire-{age}-ans-{suffix}.html';s=(p/'plateforme-educative'/f).read_text();meta=json.loads(re.search(r'<script type="application/json" id="learning-metadata">(.*?)</script>',s).group(1));title=re.search(r'<h1 class="club-title" id="play-title">(.*?)</h1>',s).group(1)
cat='chiffre' if suffix.startswith('chiffre-') else 'quantite';catalog=p/'plateforme-educative'/f'prescolaire-{age}-ans-{cat}.html'
if not catalog.exists():
 catalog.write_text((p/'plateforme-educative'/f'prescolaire-4-ans-{cat}.html').read_text().replace('prescolaire-4-ans',f'prescolaire-{age}-ans').replace('Préscolaire 4 ans',f'Préscolaire {age} ans').replace('de 4 ans',f'de {age} ans'))
c=catalog.read_text()
# Update existing cards; only finished games receive a link in five-year catalogs.
pat=rf'<(?:a|article)[^>]*>.*?<h2>{re.escape(title)}</h2>.*?</(?:a|article)>'
# Titles may have changed from chiffre to nombre: find the card by its source slug or original title.
oldtitle=re.search(r'<h1 class="club-title" id="play-title">(.*?)</h1>',(p/'plateforme-educative'/f'prescolaire-4-ans-{suffix}.html').read_text()).group(1)
# For prepared 5-year disabled articles title remains original.
original={'chiffre-ecoute':'Les chiffres qui parlent','chiffre-train':'Le train des chiffres','chiffre-manquant':'Le chiffre disparu','chiffre-collections':'Le chiffre et ses trésors'}.get(suffix,oldtitle)
pattern=r'<(?:a|article)[^>]*class="catalog-card".*?</(?:a|article)>'
def card(m):
 t=m.group(0)
 if f in t or f'<h2>{original}</h2>' in t or f'<h2>{title}</h2>' in t:
  t=re.sub('<h2>.*?</h2>','<h2>'+title+'</h2>',t,count=1);t=re.sub('<p>.*?</p>','<p>'+meta['skill']+'</p>',t,count=1)
  if age==5:
   t=t.replace('<article aria-disabled="true"',f'<a href="{f}"').replace('</article>','</a>')
   t=t.replace('En préparation','Gratuit' if '-ecoute' in f else 'Avec abonnement')
  return t
 if age==5:
  t=re.sub(r'<a href="[^"]+"','<article aria-disabled="true"',t,count=1).replace('</a>','</article>');t=re.sub(r'<span class="badge[^>]*>.*?</span>','<span class="badge">En préparation</span>',t)
 return t
# Do not disable previous finished cards.
follow=p/'docs/prescolaire-5-ans/suivi.json';data=json.loads(follow.read_text())
finished={g['target'] for g in data['games'] if g['status']=='termine'}|{f}
def filtered(m):
 t=m.group(0)
 if age==5 and any(f'href="{prev}"' in t for prev in finished if prev!=f):return t
 return card(m)
c=re.sub(pattern,filtered,c,flags=re.S)
if age==4:
 c=c.replace('Cinq petites aventures pour découvrir et s’amuser à son rythme.','Des découvertes en petits paliers, jusqu’à 15. Commence par 1 à 5 et continue à ton rythme.')
catalog.write_text(c)
if age==5:
 for g in data['games']:
  if g['target']==f:g.update(status='termine',verification=summary)
else:data.setdefault('four_year_numeric_games',{})[f]={'status':'adapte_et_verifie','verification':summary}
follow.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
with follow.with_name('JOURNAL.md').open('a') as out:out.write(f'\n- {f} : {summary}\n')
