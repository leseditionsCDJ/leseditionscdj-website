from pathlib import Path
import subprocess,re,json,sys
root=Path(__file__).resolve().parents[1];p=root/'plateforme-educative';suffix=sys.argv[1];target='prescolaire-5-ans-'+suffix+'.html'
if (p/target).exists():raise SystemExit('Jeu déjà présent.')
source=subprocess.check_output(['git','show','98b97f68ba3c7457a34456872da4d248f217a4a0:plateforme-educative/prescolaire-4-ans-'+suffix+'.html'],cwd=root,text=True)
title=re.sub('<[^>]+>','',re.search(r'<h1[^>]*>(.*?)</h1>',source,re.S).group(1));cat,slug=suffix.split('-',1)
config={
'couleurs-ballons':('balloons','Reconnaître quatorze couleurs, dont gris, turquoise, beige et bleu marine, parmi quatre ballons.'),
'couleurs-train':('trainColors','Trier huit objets de quatre couleurs dans les wagons correspondants, parmi quatorze couleurs possibles.'),
'couleurs-safari':('safariColors','Retrouver quatre objets en tenant compte de leur forme et de leur couleur, parmi douze objets.'),
'couleurs-tableaux':('paintModel','Reproduire un tableau de six zones en choisissant parmi quatorze couleurs.'),
'couleurs-machine':('mix','Explorer huit recettes de mélanges de peinture simulés pour obtenir une couleur demandée.'),
'formes-jardin':('shapeListen','Reconnaître neuf formes, dont ovale, losange et hexagone, parmi quatre propositions.'),
'formes-chasse':('shapeHunt','Retrouver quatre formes identiques parmi dix formes aux couleurs variées; neuf formes possibles.'),
'formes-paniers':('shapeSort','Trier six pièces dans trois paniers selon leur forme, en ignorant leur couleur; neuf formes possibles.'),
'formes-construis':('shapeBuild','Reproduire une mosaïque de six pièces à partir d’un modèle; neuf formes possibles.'),
'formes-coloriage':('shapePaint','Suivre neuf consignes combinant une forme et une couleur pour colorier neuf formes.'),
'espace-cache':('spaceFind','Repérer une scène qui respecte simultanément deux positions autour d’une table.'),
'espace-campement':('spaceCamp','Comprendre deux consignes de placement et installer les deux objets aux bonnes positions.'),
'espace-photo':('spacePhoto','Mémoriser ou observer un modèle et reproduire les positions de quatre objets autour d’une table.'),
'espace-parcours':('spacePath','Suivre quatre directions successives sur un quadrillage, une case à la fois.'),
'espace-promenades':('spaceWalk','Suivre trois directions successives sur un quadrillage et atteindre la bonne case.')}
mode,desc=config[suffix];paid=suffix not in ['couleurs-ballons','formes-jardin','espace-cache'];category={'couleurs':'Couleurs','formes':'Formes','espace':'Espace'}[cat]
base=subprocess.check_output(['git','show','98b97f68ba3c7457a34456872da4d248f217a4a0:plateforme-educative/prescolaire-4-ans-chiffre-ecoute.html'],cwd=root,text=True)
script=re.search('<script>(.*?)</script>',base,re.S).group(1);core=script[:script.index('const LETTERS=')];core='\n'.join(core.splitlines()[2:]);core=core.replace('club4-','club5-');core=core.replace('s=map[k];',"Object.assign(map,{ovale:`<ellipse cx=\"80\" cy=\"80\" rx=\"65\" ry=\"43\" fill=\"${g}\" ${w}/>`,losange:`<path d=\"M80 12L140 80L80 148L20 80Z\" fill=\"${g}\" ${w}/>`,hexagone:`<path d=\"M45 20H115L150 80L115 140H45L10 80Z\" fill=\"${g}\" ${w}/>`});s=map[k];")
cfg={'cat':cat,'category':category,'slug':slug,'title':title,'mode':mode,'paid':paid,'file':target}
end=script[script.index("$('next').onclick"):].replace('club4-','club5-')
engine=(root/'scripts/templates/prescolaire-special.js').read_text()
# Compact palettes and scene cards keep the controls practical on a phone.
engine=engine.replace("const b=box();state.items.forEach", "const b=box();state.items.forEach")
engine=engine.replace("const b=box();shuffle([d.name", "const b=box();shuffle([d.name")
engine=engine.replace("const palette=box();", "const palette=box('tiles paint-palette');")
engine=engine.replace("const picture=box('mosaic'),palette=box();", "const picture=box('mosaic'),palette=box('tiles paint-palette');")
engine=engine.replace("let rels=shuffle(PLACES).slice(0,2);", "let rels=shuffle(PLACES).slice(0,2);")
engine=engine.replace("let rels=shuffle(PLACES).slice(0,2);", "let rels=shuffle(PLACES).slice(0,2);")
engine=engine.replace("const b=box();shuffle([state.arrangement", "const b=box('space-options');shuffle([state.arrangement")
# spaceFind is a separate block; use two-column illustrated scenes there only.
engine=engine.replace("deux personnages.'),{html:tableScene", "deux personnages.'),{html:tableScene")
engine=engine.replace("let rels=shuffle(PLACES).slice(0,2);state.arrangement", "let rels=shuffle(PLACES).slice(0,2);state.arrangement")
newscript='const CFG='+json.dumps(cfg,ensure_ascii=False)+';\n'+core+'\n'+engine+'\n'+end
s=base.replace('prescolaire-4-ans','prescolaire-5-ans').replace('Préscolaire 4 ans','Préscolaire 5 ans').replace('>4 ans<','>5 ans<').replace('prescolaire-5-ans-chiffre.html',f'prescolaire-5-ans-{cat}.html').replace('>Chiffres</a>',f'>{category}</a>').replace('Les chiffres qui parlent',title).replace('Écouter et reconnaître les chiffres de 1 à 5.',desc)
if paid:s=s.replace('<span class="badge ">Gratuit</span>','<span class="badge paid">Avec abonnement</span>')
s=re.sub('<script>.*?</script>',lambda m:'<script>'+newscript+'</script>',s,count=1,flags=re.S)
meta={'level':'prescolaire_5','subject':'developpement_global','domain':cat,'skill':desc,'official_scope':'cycle','platform_year':'prescolaire_5','progress_state':'entrainement','difficulty':2,'prerequisites':['Explorer les activités des 4 ans correspondantes'],'game_type':mode,'reading_load':'faible','answer_key':'Cible de couleur, forme, position ou séquence définie dans la manche; correspondance visuelle au modèle.','feedback':'Indices, réécoute et essais libres.','source_tag':{'guide':'Guide_plateforme_Quebec.pdf, sections 4 à 6','url':'https://www.quebec.ca/education/prescolaire-primaire-et-secondaire/programmes-formations-evaluation/programme-formation-ecole-quebecoise/education-prescolaire','verified':'2026-11-15','status':'Défi de plateforme dans le programme-cycle commun, sans exigence annuelle inventée.'}}
s=s.replace('</head>','<link rel="stylesheet" href="assets/prescolaire-special.css"><script type="application/json" id="learning-metadata">'+json.dumps(meta,ensure_ascii=False)+'</script></head>')
(p/target).write_text(s);print(target+' : '+mode)
