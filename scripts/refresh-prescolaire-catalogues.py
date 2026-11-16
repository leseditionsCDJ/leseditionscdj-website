from pathlib import Path
import re,json,html,subprocess
root=Path(__file__).resolve().parents[1];p=root/'plateforme-educative';follow=json.loads((root/'docs/prescolaire-5-ans/suivi.json').read_text());done={g['target'] for g in follow['games'] if g['status']=='termine'}
roothtml=(p/'prescolaire-4-ans.html').read_text().replace('prescolaire-4-ans','prescolaire-5-ans').replace('Préscolaire 4 ans','Préscolaire 5 ans').replace('Préscolaire · 4 ans','Préscolaire · 5 ans').replace('Mes premières découvertes','Mes nouvelles découvertes').replace('Des couleurs, des surprises et plein de petites aventures pour découvrir le monde en jouant.','Des défis pour continuer à explorer les nombres, les lettres, les formes et le monde à ton rythme.')
categories=re.findall(r'href="prescolaire-5-ans-([^"]+)\.html"',roothtml)
base=subprocess.check_output(['git','show','98b97f68ba3c7457a34456872da4d248f217a4a0:plateforme-educative/prescolaire-4-ans-chiffre.html'],cwd=root,text=True)
for cat in categories:
 games=[g for g in follow['games'] if g['target'].startswith('prescolaire-5-ans-'+cat+'-')];ready=[g for g in games if g['target'] in done]
 def rootcard(m):
  t=m.group(0)
  if f'href="prescolaire-5-ans-{cat}.html"' not in t:return t
  if not ready:t=re.sub(r'<a href="[^"]+"','<div aria-disabled="true"',t,count=1).replace('</a>','</div>')
  return t.replace('5 jeux · 1 gratuit',f'{len(ready)} jeux prêts · {5-len(ready)} en préparation' if ready and len(ready)<5 else '5 jeux · 1 gratuit' if ready else 'En préparation')
 roothtml=re.sub(r'<a href="prescolaire-5-ans-[^"]+".*?</a>',rootcard,roothtml,flags=re.S)
 if not ready:continue
 title=re.search(r'<h3[^>]*>(.*?)</h3>',next(m.group(0) for m in re.finditer(r'<a href="prescolaire-4-ans-[^"]+".*?</a>',(p/'prescolaire-4-ans.html').read_text(),re.S) if f'prescolaire-4-ans-{cat}.html' in m.group(0))).group(1)
 cards=[]
 for i,g in enumerate(games):
  src=(p/g['source']).read_text();m=re.search(r'const CFG=(.*?);',src);cfg=json.loads(m.group(1)) if m else {}
  originaltitle=cfg.get('title') or re.search(r'<h1[^>]*>(.*?)</h1>',src,re.S).group(1);originaltitle=re.sub('<[^>]+>','',originaltitle)
  isready=g['target'] in done;paid=cfg.get('paid',i!=0)
  if isready:
   actual=(p/g['target']).read_text();meta=json.loads(re.search(r'<script type="application/json" id="learning-metadata">(.*?)</script>',actual).group(1));description=meta['skill'];t=re.search(r'<h1[^>]*>(.*?)</h1>',actual,re.S).group(1);t=re.sub('<[^>]+>','',t)
  else:t=originaltitle;description='Cette aventure est en préparation.'
  tag=f'a href="{g["target"]}"' if isready else 'article aria-disabled="true"';end='a' if isready else 'article'
  icon={'chiffre':'3','quantite':'panier','lettre':'A','observation':'loupe','emotion':'happy','vie-sociale':'coeur','comparaison':'ruban','securite':'casque','corps-humain':'main','memoire':'livre','logique':'cube','couleurs':'fleur','formes':'triangle','espace':'maison'}[cat]
  colors=['#ffe8a4','#d1edff','#e3ddff','#ffdfc8','#d8f3cd'];access='Avec abonnement' if paid else 'Gratuit'
  cards.append(f'<{tag} class="catalog-card" style="--card:{colors[i%5]};--edge:#c3a16c"><div data-icon="{icon}"></div><h2>{html.escape(t)}</h2><p>{html.escape(description)}</p><span class="badge{ " paid" if paid and isready else ""}">{access if isready else "En préparation"}</span></{end}>')
 c=base.replace('prescolaire-4-ans','prescolaire-5-ans').replace('Préscolaire 4 ans','Préscolaire 5 ans').replace('de 4 ans','de 5 ans').replace('<h1 class="club-title">Chiffres</h1>',f'<h1 class="club-title">{title}</h1>')
 c=c.replace('Cinq petites aventures pour découvrir et s’amuser à son rythme.','Des aventures pour continuer à découvrir et à réfléchir à ton rythme.').replace('5 jeux · 1 gratuit',f'{len(ready)} jeux prêts sur 5')
 c=re.sub(r'(<section class="catalog-grid"[^>]*>).*?(</section>)',lambda m:m.group(1)+''.join(cards)+m.group(2),c,count=1,flags=re.S)
 c=c.replace('data-category-icon="3"',f'data-category-icon="{icon}"')
 (p/f'prescolaire-5-ans-{cat}.html').write_text(c)
(p/'prescolaire-5-ans.html').write_text(roothtml)
print(f'Catalogue actualisé : {len(done)}/70 jeux prêts.')
