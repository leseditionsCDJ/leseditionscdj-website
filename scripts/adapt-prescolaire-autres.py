from pathlib import Path
import re,json,subprocess,sys
root=Path(__file__).resolve().parents[1];p=root/'plateforme-educative';suffix=sys.argv[1]
source='prescolaire-4-ans-'+suffix+'.html';target=source.replace('-4-ans','-5-ans')
if (p/target).exists():raise SystemExit('Le jeu existe déjà : vérifier le suivi avant toute modification.')
s=subprocess.check_output(['git','show','98b97f68ba3c7457a34456872da4d248f217a4a0:plateforme-educative/'+source],cwd=root,text=True)
cfg=json.loads(re.search(r'const CFG=(.*?);',s).group(1));mode=cfg['mode']
s=s.replace("club4-","club5-")
s=re.sub(r"const LETTERS=\[.*?\];","const LETTERS=Array.from('ABCDEFGHIJKLMNOPQRSTUVWXYZ');",s)
s=s.replace('prescolaire-4-ans','prescolaire-5-ans').replace('Préscolaire 4 ans','Préscolaire 5 ans').replace('>4 ans<','>5 ans<').replace("STORE='club4-'", "STORE='club5-'")
s=s.replace("const LETTERS=['A','E','I','O','U','M','L','S','T','R','P','B','D','F','N','C'];", "const LETTERS=Array.from('ABCDEFGHIJKLMNOPQRSTUVWXYZ');")
def branch(name,new):
 global s
 pattern=r"(?:^if|^else if)\(MODE==='"+name+r"'\).*?(?=\nelse if\(|\nelse throw)"
 m=re.search(pattern,s,re.M|re.S)
 if not m:raise Exception('Branche absente : '+name)
 s=s[:m.start()]+new+s[m.end():]
extra=''
desc=''
if mode=='letterListen':
 s=s.replace("k=num?String(n):k;ask(`Touche ${num?'le chiffre':'la lettre'} ${k}.`);let pool=num?['1','2','3','4','5']:LETTERS;choose([k,...shuffle(pool.filter(x=>x!==k)).slice(0,2)],k);", "k=num?String(n):(round%2?k.toLowerCase():k);ask(`Touche ${num?'le nombre':'la lettre'} ${k}${num?'':round%2?' minuscule':' majuscule'}.`);let pool=num?['1','2','3','4','5']:LETTERS.map(x=>round%2?x.toLowerCase():x);choose([k,...shuffle(pool.filter(x=>x!==k)).slice(0,3)],k);")
 desc='Reconnaître les 26 lettres, en majuscules et en minuscules, parmi quatre choix.'
elif mode=='letterMatch':
 branch(mode,"""else if(MODE==='letterMatch'){let reverse=round%2===1,modelKey=reverse?k.toLowerCase():k,answer=reverse?k:k.toLowerCase();ask(`Voici la lettre ${modelKey} ${reverse?'minuscule':'majuscule'}. Retrouve sa lettre ${reverse?'majuscule':'minuscule'}.`);model(modelKey,'#ecb847');choose([answer,...shuffle(LETTERS.filter(x=>x!==k)).slice(0,3).map(x=>reverse?x:x.toLowerCase())],answer);}""")
 desc='Associer majuscules et minuscules dans les deux sens, parmi quatre choix.'
elif mode=='letterHunt':
 branch(mode,"""else if(MODE==='letterHunt'){let letters=shuffle([k,k.toLowerCase(),k.toLowerCase(),...shuffle(LETTERS.filter(x=>x!==k)).slice(0,7).map((x,i)=>i%2?x.toLowerCase():x)]),found=0;ask(`Retrouve les trois lettres ${k}, en majuscule ou en minuscule.`);model(k,'#ecb847');let b=box();letters.forEach(x=>b.append(btn(x,e=>{if(e.disabled)return;if(x.toUpperCase()===k){e.disabled=true;e.classList.add('done');if(++found===3)win('Tu as retrouvé la même lettre sous ses deux formes !');else feedback(`${found} sur 3`)}else wrong(e,'Cherche la même lettre, grande ou petite.')})));}""")
 desc='Retrouver une même lettre en majuscule et en minuscule dans dix lettres mélangées.'
elif mode=='initial':
 branch(mode,"""else if(MODE==='initial'){let answer=k.toLowerCase();ask(`Regarde le prénom ${d.name}. Quelle minuscule correspond à sa première lettre ?`);let b=box('display-model');b.innerHTML=`<p class="stage-title">${esc(d.name)}</p>`;choose([answer,...shuffle(LETTERS.filter(x=>x!==k)).slice(0,3).map(x=>x.toLowerCase())],answer);}""")
 desc='Observer l’initiale d’un prénom et retrouver la minuscule correspondante.'
elif mode=='trace':
 extra="""Object.assign(TRACES,{l:[[95,35],[95,90],[95,150],[95,210],[95,270]],t:[[135,60],[135,115],[135,175],[135,240],[160,265],[195,245],[135,120],[80,120],[195,120]],i:[[135,115],[135,170],[135,220],[135,270],[135,65]],v:[[55,120],[80,170],[105,220],[135,270],[160,220],[185,170],[210,120]],m:[[45,270],[45,210],[45,135],[45,195],[85,125],[130,150],[130,210],[130,270],[130,195],[175,125],[220,150],[220,210],[220,270]],a:[[205,150],[175,125],[110,125],[70,175],[70,235],[115,265],[175,250],[205,210],[205,135],[205,205],[205,265]]});\n"""
 s=s.replace('Explore la lettre ${k}.','Explore la lettre ${k} ${k===k.toLowerCase()?\'minuscule\':\'majuscule\'}.')
 desc='Explorer les chemins de six lettres en majuscules et de six minuscules, point par point.'
elif mode=='lookMatch':
 s=s.replace("{k:other[0],c}];", "{k:other[0],c},{k:other[1],c:pick(COLORS.filter(x=>x!==c))}];")
 desc='Comparer quatre objets et retrouver celui qui a exactement la même forme et la même couleur.'
elif mode=='odd':
 s=s.replace("items=shuffle([k,k,k,different])", "items=shuffle([k,k,k,k,k,different])").replace('différent des trois autres','différent des cinq autres')
 desc='Repérer l’intrus parmi six objets.'
elif mode=='difference':
 s=s.replace("keys=[k,...other.slice(0,3)],change=shuffle([0,1,2,3]).slice(0,2)","keys=[k,...other.slice(0,5)],change=shuffle([0,1,2,3,4,5]).slice(0,3)")
 s=s.replace('les deux objets qui ont changé','les trois objets qui ont changé').replace("if(done===2)win('Les deux changements", "if(done===3)win('Les trois changements")
 desc='Comparer deux tableaux de six objets et repérer trois changements de couleur.'
elif mode=='search':
 s=s.replace("let count=2+round%3", "let count=4+round%3").replace('...other.slice(0,6)','...other.slice(0,9)')
 desc='Chercher quatre à six objets identiques parmi neuf distracteurs.'
elif mode=='vanish':
 # The memory game has a specialized override in its source; replace its active render with a distinct challenge.
 start=s.index('function render(){');end=s.index('\nfunction faceOptions',start)
 # Use the generic render scaffolding and one active branch; drop overrides to avoid an older same-name declaration.
 s=s[:start]+"""function render(){cancel();solved=false;busy=false;state={};$('play').replaceChildren();$('next').hidden=true;$('progress').textContent=`${round+1} / ${rounds.length}`;feedback('À toi de jouer !');let d=rounds[round],k=d.k,c=d.c||COLORS[0],keys=shuffle([k,...shuffle(OBJECTS.filter(x=>x!==k)).slice(0,5)]),gone=shuffle(keys).slice(0,2);ask('Observe les six objets. Cache-les quand tu es prêt. Deux vont disparaître.');let view=box('display-model collection');view.innerHTML=keys.map(x=>art(x,c)).join('');action('Je suis prêt',button=>{button.remove();view.innerHTML=keys.filter(x=>!gone.includes(x)).map(x=>art(x,c)).join('');ask('Quels sont les deux objets disparus ?');let b=box(),found=0;shuffle([...gone,...shuffle(OBJECTS.filter(x=>!gone.includes(x))).slice(0,3)]).forEach(x=>b.append(btn(x,e=>{if(e.disabled)return;if(gone.includes(x)){e.disabled=true;e.classList.add('done');if(++found===2)win('Tu as retrouvé les deux objets !')}else wrong(e,'Compare avec ce qui est encore visible. Cet objet n’a pas disparu.')})));});}
"""+s[end:]
 # specialized overrides after the general helpers must be removed as well
 s=re.sub(r'\n//[^\n]*\nfunction renderVanish.*?(?=\nfunction |\n\$\(|\nsetupVoices)', '', s, flags=re.S)
 desc='Mémoriser six objets et retrouver les deux objets qui ont disparu.'
elif mode in ['size','length','height','sameSize','sizeOrder']:
 # Replace the complete active comparison block and retain related illustrated controls.
 a=s.index("else if(['size','length','height','sameSize','sizeOrder'].includes(MODE))")
 b=s.index("\nelse if(MODE==='equipment')",a)
 new="""else if(['size','length','height','sameSize','sizeOrder'].includes(MODE)){let small=round%2===0,values=[1,2,3,4];const draw=v=>MODE==='length'?`<div style="width:220px"><div class="ribbon" style="width:${v*45}px"></div></div>`:MODE==='height'?`<div class="tower">${Array(v+1).fill('<i></i>').join('')}</div>`:scaled(k,c,v);if(MODE==='sizeOrder'){ask('Range les quatre objets du plus petit au plus grand.');let idx=1,b=box();shuffle(values).forEach(v=>b.append(btn(k,e=>{if(e.disabled)return;if(v===idx){e.disabled=true;e.classList.add('done');if(++idx>4)win('Les quatre objets sont rangés !')}else wrong(e,'Compare avec les objets qui restent.')},{html:draw(v),label:`Objet de taille ${v}`})));}else{let target=MODE==='sameSize'?rand(1,4):small?1:4;if(MODE==='sameSize'){ask('Retrouve exactement la même taille que le modèle.');let b=box('display-model');b.innerHTML=scaled(k,c,target)}else ask(MODE==='length'?`Touche le ruban le plus ${small?'court':'long'}.`:MODE==='height'?`Touche la tour la plus ${small?'basse':'haute'}.`:`Touche l’objet le plus ${small?'petit':'grand'}.`);choose(values,target,v=>({html:draw(v),label:`Objet de taille ${v}`}));}}"""
 s=s[:a]+new+s[b:]
 s=s.replace('[75,120,170][v-1]','[60,95,130,170][v-1]')
 desc='Comparer quatre grandeurs et '+('les ordonner de la plus petite à la plus grande.' if mode=='sizeOrder' else 'retrouver la grandeur demandée.')
elif mode=='memory':
 s=s.replace('retrouve les trois paires','retrouve les quatre paires').replace("let keys=[k,...other.slice(0,2)],items=", "let keys=[k,...other.slice(0,3)],items=").replace("if(done===3)win('Tu as retrouvé les trois paires", "if(done===4)win('Tu as retrouvé les quatre paires")
 desc='Retrouver quatre paires parmi huit cartes cachées.'
elif mode in ['sequence','audioSequence']:
 # Replace both baseline and later customized declarations by using one new render.
 a=s.index('function render(){');b=s.index('\nfunction faceOptions',a)
 s=s[:a]+"""function render(){cancel();solved=false;busy=false;state={};$('play').replaceChildren();$('next').hidden=true;$('progress').textContent=`${round+1} / ${rounds.length}`;feedback('À toi de jouer !');let d=rounds[round],keys=shuffle(OBJECTS).slice(0,6),seq=shuffle(keys).slice(0,round<3?4:5),index=0,shown=false,c=COLORS[round%6],buttons=[],b=box();state.sequence=seq;ask(MODE==='sequence'?'Observe la suite, puis touche les images dans le même ordre.':'Écoute la suite, puis touche les images dans le même ordre.');let slots=box('slots');seq.forEach(()=>slots.append(node('div','slot','?')));keys.forEach(x=>{let e=btn(x,e=>{if(!shown){feedback('Découvre la suite avant de commencer.');return}if(x===seq[index]){slots.children[index].innerHTML=art(x,c);if(++index===seq.length)win('Tu as reproduit toute la suite !')}else{index=0;[...slots.children].forEach(e=>e.textContent='?');wrong(e,'Reprends au début. Tu peux revoir ou réécouter la suite.')}},{color:c});buttons.push(e);b.append(e)});action(MODE==='sequence'?'Voir la suite':'Écouter la suite',()=>{if(busy)return;busy=true;shown=false;index=0;[...slots.children].forEach(e=>e.textContent='?');const done=()=>{buttons.forEach(e=>e.classList.remove('flash'));[...slots.children].forEach(e=>e.textContent='?');shown=true;busy=false;feedback('À toi !')};if(MODE==='audioSequence'&&'speechSynthesis' in window){speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(seq.map(label).join(' … '));u.lang='fr-CA';u.rate=.8;u.onend=done;u.onerror=()=>{busy=false;shown=true;feedback('La voix est indisponible. Demande à un adulte de lire la suite : '+seq.map(label).join(', '));};speechSynthesis.speak(u)}else{if(MODE==='audioSequence')feedback('La voix est indisponible : observe la suite.');seq.forEach((x,i)=>later(()=>{buttons.forEach(e=>e.classList.remove('flash'));buttons[keys.indexOf(x)].classList.add('flash');slots.children[i].innerHTML=art(x,c)},i*1200));later(done,seq.length*1200+500)}});}
"""+s[b:]
 desc='Reproduire une suite '+('entendue' if mode=='audioSequence' else 'observée')+' de quatre à cinq images, parmi six choix.'
elif mode=='positions':
 a=s.index('function render(){');b=s.index('\nfunction faceOptions',a)
 s=s[:a]+"""function render(){cancel();solved=false;busy=false;state={};$('play').replaceChildren();$('next').hidden=true;$('progress').textContent=`${round+1} / ${rounds.length}`;let keys=shuffle(OBJECTS).slice(0,8),targets=shuffle(keys).slice(0,3),idx=0,b=box('memory-grid');state.keys=keys;state.targets=targets;ask('Mémorise les places des huit objets. Cache-les quand tu es prêt.');keys.forEach((x,i)=>b.append(btn(x,e=>{if(!state.hidden||e.disabled)return;if(x===targets[idx]){e.disabled=true;e.innerHTML=art(x);e.classList.add('done');if(++idx===targets.length)win('Tu as retrouvé trois places !');else ask('Où était '+label(targets[idx])+' ?')}else wrong(e,'Essaie une autre place. Tu peux recommencer pour revoir les images.')})));action('Cacher les images',button=>{button.remove();state.hidden=true;[...b.children].forEach((e,i)=>{e.innerHTML='<span class="memory-back" aria-hidden="true">?</span>';e.setAttribute('aria-label',`Emplacement ${i+1}`)});ask('Où était '+label(targets[0])+' ?')});}
"""+s[b:]
 desc='Mémoriser huit emplacements, puis retrouver trois objets demandés après le masquage.'
elif mode=='pattern':
 branch(mode,"""else if(MODE==='pattern'){let patterns=[[0,1,2],[0,0,1],[0,1,1]],pattern=patterns[round%3],keys=[k,...other.slice(0,2)],seq=Array.from({length:pattern.length*2},(_,i)=>keys[pattern[i%pattern.length]]),answer=keys[pattern[0]];state.answer=answer;ask('Observe les deux groupes du collier. Quelle image commence le groupe suivant ?');let b=box('display-model collection');seq.forEach(x=>b.insertAdjacentHTML('beforeend',art(x,c)));b.insertAdjacentHTML('beforeend','<div class="slot">?</div>');choose(keys,answer);}""")
 desc='Prolonger des régularités ABC, AAB et ABB après deux répétitions complètes.'
elif mode=='puzzle':
 s=s.replace("['cercle','carre','triangle','etoile','coeur','rectangle']).slice(0,3)","['cercle','carre','triangle','etoile','coeur','rectangle','ovale','losange','hexagone']).slice(0,5)")
 s=s.replace("if(++done===3)win('Les trois pièces", "if(++done===5)win('Les cinq pièces")
 extra="""Object.assign(LABELS,{ovale:'ovale',losange:'losange',hexagone:'hexagone'});\n"""
 s=s.replace('s=map[k];',"Object.assign(map,{ovale:`<ellipse cx=\"80\" cy=\"80\" rx=\"65\" ry=\"43\" fill=\"${g}\" ${w}/>`,losange:`<path d=\"M80 12L140 80L80 148L20 80Z\" fill=\"${g}\" ${w}/>`,hexagone:`<path d=\"M45 20H115L150 80L115 140H45L10 80Z\" fill=\"${g}\" ${w}/>`});s=map[k];")
 desc='Associer cinq pièces à leurs silhouettes parmi neuf formes, dont ovale, losange et hexagone.'
elif mode=='positions':
 branch(mode,"""else if(MODE==='positions'){let keys=shuffle(OBJECTS).slice(0,8),targets=shuffle(keys).slice(0,3),idx=0,hidden=false,b=box('memory-grid');state.keys=keys;state.targets=targets;ask('Mémorise les places des huit images. Cache-les quand tu es prêt.');keys.forEach((x,i)=>b.append(btn(x,e=>{if(!hidden||e.disabled)return;if(x===targets[idx]){e.innerHTML=art(x,c);e.disabled=true;e.classList.add('done');if(++idx===targets.length)win('Tu as retrouvé les trois places !');else ask(`Où était ${label(targets[idx])} ?`)}else wrong(e,'Essaie une autre place. Tu peux revoir toutes les images.')})));action('Cacher les images',button=>{hidden=true;idx=0;[...b.children].forEach((e,i)=>{e.innerHTML='<span class="memory-back" aria-hidden="true">?</span>';e.disabled=false;e.classList.remove('done');e.setAttribute('aria-label',`Emplacement ${i+1}`)});ask(`Où était ${label(targets[0])} ?`)});action('Revoir les images',()=>{hidden=false;idx=0;[...b.children].forEach((e,i)=>{e.innerHTML=art(keys[i],c);e.disabled=false;e.classList.remove('done');e.setAttribute('aria-label',label(keys[i]))});ask('Observe à nouveau les places, puis cache les images.')});}""")
 desc='Mémoriser huit emplacements et retrouver trois images demandées après les avoir cachées.'
elif mode=='path':
 s=s.replace("stones=new Set(level.stones)","stones=new Set([...level.stones,12])")
 s=s.replace('Aide l’ourson à trouver le cadeau. Choisis un chemin. Si le passage s’arrête, reviens sur tes pas.','Passe d’abord par l’étoile, puis rejoins le cadeau. Si le chemin s’arrête, reviens sur tes pas.')
 s=s.replace("if(current===24){win(","if(current===24&&visited.has(12)){win(")
 s=s.replace(':visited.has(i)?\'<span class="stone-paw"',':i===12?art(\'etoile\',\'#edbc4b\'):visited.has(i)?\'<span class="stone-paw"')
 desc='Planifier un parcours avec un détour obligatoire par l’étoile avant de rejoindre le cadeau.'
elif mode in ['sort','belongs']:
 if mode=='sort':
  s=s.replace('i+=2','i+=3').replace('groups.slice(i,i+2)','groups.slice(i,i+3)').replace('COLORS[(i/2)%COLORS.length]','COLORS[(i/3)%COLORS.length]')
 else:s=s.replace('distractors.slice(i*2,i*2+2)','distractors.slice(i*3,i*3+3)')
 desc='Classer six objets dans trois familles illustrées.' if mode=='sort' else 'Comparer quatre propositions pour compléter une famille et expliquer la propriété commune.'
elif mode in ['social','help','polite','safety','askAdult','boundaries','comfort']:
 stories={
 'social':["Vous voulez deux jeux différents. Vous avez déjà expliqué vos idées. Quelle proposition permet de décider ensemble ?",["Chercher une règle de choix ensemble","Décider seul parce que tu as parlé en premier","Changer de règle sans en parler","Prendre le jeu de l’autre"],0,'ballon'],
 'help':["Ton amie essaie d’assembler une tour. Elle dit : je veux essayer moi-même. Comment l’aider tout en respectant son choix ?",["Lui dire que tu es disponible si elle le souhaite","Construire la tour à sa place tout de suite","Lui retirer les cubes pour la protéger d’une erreur","Insister jusqu’à ce qu’elle accepte"],0,'cube'],
 'polite':["Tu as interrompu un ami qui expliquait son idée. Comment reprendre la conversation ?",["Dire pardon, le laisser finir, puis demander ton tour","Dire merci et continuer à parler","Parler moins fort mais sans le laisser finir","T’en aller sans l’écouter"],0,'oreille'],
 'safety':["Un ballon roule vers la rue. Tu es encore dans la cour avec ton adulte. Que fais-tu d’abord ?",["Rester dans la cour et appeler ton adulte","Courir derrière le ballon avant qu’il soit loin","Traverser en regardant seulement un côté","Demander à un autre enfant de courir"],0,'ballon'],
 'askAdult':["Tu t’éloignes du groupe et tu ne vois plus ton adulte dans le magasin. Que peux-tu faire ?",["Rester sur place et demander l’aide du personnel du magasin","Sortir seul pour le chercher","Te cacher pour attendre","Partir avec une personne inconnue"],0,'maison'],
 'boundaries':["Tu avais accepté un câlin, mais maintenant tu n’en veux plus. Que peux-tu faire ?",["Dire stop et demander de l’aide si ton choix n’est pas respecté","Continuer parce que tu avais accepté avant","Croire que tu ne peux plus changer d’avis","Rester silencieux même si tu es mal à l’aise"],0,'main'],
 'comfort':["Ton amie est déçue et dit qu’elle veut rester seule un moment. Que peux-tu proposer ?",["Respecter son espace et lui dire que tu restes disponible","L’obliger à parler tout de suite","Lui demander de sourire pour te faire plaisir","Prendre son jouet pour lui changer les idées"],0,'coeur']}
 # New contexts join the original bank; every choice is spoken before confirmation.
 extra='BANKS['+json.dumps(mode)+'].push('+json.dumps(stories[mode],ensure_ascii=False)+');\n'
 s=s.replace("win(options[index]+'.');", "win(options[index]+'. Tu peux raconter à un adulte pourquoi cette idée aide.');")
 desc='Écouter un contexte plus long, choisir une action respectueuse et expliquer ce qu’elle permet.'
elif mode=='emotionListen':
 branch(mode,"""else if(MODE==='emotionListen'){let target=k;ask(`Touche la ${label(target)}. Puis écoute une idée pour en parler.`);choose(EMOTIONS,target,faceOptions);}""")
 s=s.replace("win()}","win('Tu as reconnu cette expression. Raconte un moment où tu as ressenti cette émotion, si tu en as envie.')}" ,1)
 desc='Reconnaître une expression, nommer l’émotion et raconter une situation vécue si on le souhaite.'
elif mode=='emotionStory':
 extra="""BANKS.emotionStory.push(['Léo espérait finir sa construction. Elle tombe et il dit : je suis déçu, j’ai envie de pleurer. Quel visage va avec ce qu’il raconte ?','sad'],['Mia attend son tour. Elle serre les poings et dit : je suis fâchée, je vais demander une pause. Quel visage va avec ses mots ?','angry']);\n"""
 desc='Écouter une courte histoire avec plusieurs indices et relier les mots du personnage à une émotion.'
elif mode=='mirror':
 s=s.replace('puis choisis un autre visage à imiter.','puis compare-le avec un autre visage. Observe ce qui change dans les yeux et la bouche.')
 s=s.replace('Chaque émotion a sa place. Tu peux en parler avec un adulte.','Chaque émotion a sa place. Raconte ce que tu as observé dans les yeux ou la bouche.')
 desc='Comparer et imiter des expressions, puis décrire ce qui change dans les yeux ou la bouche.'
elif mode=='breathe':
 s=s.replace("let ball=add($('play')", "feedback('Avant de commencer, demande-toi comment tu te sens. Après la pause, tu pourras comparer.');let ball=add($('play')")
 s=s.replace('Merci pour cette petite pause. Comment te sens-tu ?', 'Comment te sens-tu après cette pause ? Est-ce pareil ou différent ? Tu peux en parler.')
 desc='Choisir une pause douce et comparer son ressenti avant et après, sans obligation ni performance.'
elif mode in ['turns','cooperate']:
 s=s.replace('let total=6,count=0','let total=10,count=0')
 s=s.replace('Vous avez joué chacun votre tour !','Vous avez joué chacun votre tour ! Quelle règle vous a aidés à construire ensemble ?')
 desc='Réaliser cinq tours chacun en respectant l’alternance et expliquer la règle de coopération.'
elif mode=='body':
 extra="""Object.assign(LABELS,{coude:'coude',genou:'genou',epaule:'épaule'});\n"""
 s=s.replace("['tete','bras','main','ventre','jambes','pied'].map", "['tete','bras','main','ventre','jambes','pied','coude','genou','epaule'].map")
 s=s.replace("pied:'un pied'", "pied:'un pied',coude:'un coude',genou:'un genou',epaule:'une épaule'")
 s=s.replace("${part('ventre'", "${part('coude','<circle cx=\"82\" cy=\"201\" r=\"15\" fill=\"#e6b58d\"/>')}${part('genou','<circle cx=\"120\" cy=\"311\" r=\"17\" fill=\"#7eadd3\"/>')}${part('epaule','<circle cx=\"107\" cy=\"155\" r=\"16\" fill=\"#e6b58d\"/>')}${part('ventre'")
 desc='Repérer neuf parties du corps, dont coude, genou et épaule.'
elif mode=='senses':
 extra="""SENSES.push(['Tu écoutes un bruit pour savoir si la cloche sonne. Quelle partie du corps t’aide ?','oreille','cloche'],['Tu observes la peau d’une pomme avant de la toucher. Quelle partie du corps utilises-tu d’abord ?','oeil','pomme'],['Tu touches doucement un tissu, puis tu décris s’il est doux. Quelle partie du corps t’aide ?','main','ruban']);\n"""
 s=s.replace("slice(0,2)],answer);", "slice(0,3)],answer);")
 desc='Choisir le sens utilisé à une étape précise d’une situation, parmi quatre réponses.'
elif mode=='movement':
 s=s.replace("Tu peux aussi regarder et imaginer le geste.","Puis fais doucement un signe avec la main, si c’est confortable. Tu peux aussi imaginer les deux gestes.")
 desc='Comprendre et explorer une consigne de deux gestes doux, avec une alternative d’observation.'
elif mode=='movement':
 branch(mode,"""else if(MODE==='movement'){let moves=[['Bouge doucement une main, puis un pied.','main','pied'],['Lève les bras selon ton confort, puis bouge les doigts.','bras','main'],['Touche doucement ta tête, puis ton ventre.','tete','ventre'],['Bouge un pied, puis fais un signe de la main.','pied','main']][d.variant%4];ask(moves[0]+' Tu peux aussi observer et imaginer.');let b=box('display-model collection');b.innerHTML=art(moves[1],c)+'<span>→</span>'+art(moves[2],c);action('J’ai essayé ou observé',()=>win('Tu as exploré deux gestes dans l’ordre, à ta façon !'));}""")
 desc='Explorer une consigne de deux gestes successifs, avec une alternative assise ou imaginée.'
elif mode=='routine':
 extra="""ROUTINES.splice(0,ROUTINES.length,['Avant la collation.',['cube','panier','savon','pomme'],['Terminer le jeu','Ranger les jouets','Se laver les mains','Manger la collation']],['Au retour d’une promenade.',['maison','bottes','savon','gourde'],['Rentrer avec son adulte','Enlever les bottes','Se laver les mains','Boire de l’eau']],['Pour un atelier de dessin.',['crayon','livre','panier','savon'],['Préparer les crayons et le papier','Dessiner','Ranger le matériel','Se laver les mains']]);\n"""
 s=s.replace("if(idx===3)win('Les trois étapes sont dans l’ordre !')", "if(idx===icons.length)win('Les étapes sont dans l’ordre !')")
 desc='Remettre quatre étapes de la vie quotidienne dans un ordre logique.'
elif mode=='clothes':
 s=s.replace("choose([part,...shuffle(['tete','main','pied','oeil'].filter(x=>x!==part)).slice(0,2)],part);", "choose([part,...shuffle(['tete','main','pied','oeil','jambes'].filter(x=>x!==part)).slice(0,3)],part);")
 s=s.replace('Sur quelle partie du corps met-on','Observe le vêtement. Sur quelle partie du corps met-on')
 desc='Relier un vêtement à la partie du corps correspondante parmi quatre possibilités.'
elif mode=='equipment':
 s=s.replace(".filter(x=>x!==answer).slice(0,2)]),answer);", ".filter(x=>x!==answer)]),answer);")
 extra="""EQUIP.push(['Tu sors au soleil avec ton adulte. Quelle protection portes-tu sur la tête ?','chapeau'],['Tu pars jouer dans la neige. Que peux-tu porter aux mains pour les garder au chaud ?','gant']);\n"""
 desc='Choisir l’équipement adapté à une situation et à la partie du corps à protéger, parmi quatre choix.'
elif mode=='safeSteps':
 s=s.replace('Remets les trois gestes dans l’ordre.','Remets les quatre gestes dans l’ordre.').replace("orderedSteps(['main','bouche','maison'],['Je m’arrête et je ne touche pas','J’appelle mon adulte de confiance','J’attends son aide'],false)","orderedSteps(['main','bouche','maison','oreille'],['Je m’arrête et je ne touche pas','J’appelle mon adulte de confiance','J’attends à distance','J’écoute ses consignes'],false)")
 s=s.replace("if(idx===3)win('Les trois étapes sont dans l’ordre !')", "if(idx===icons.length)win('Les quatre étapes sont dans l’ordre !')")
 desc='Ordonner quatre gestes de prudence : arrêter, appeler, attendre à distance et écouter l’adulte.'
else:raise Exception('Mode non traité '+mode)
# Insert extensions after their tables and before the game starts.
s=s.replace('function buildRounds(){',extra+'function buildRounds(){',1)
# Prompt strategy after logic activities without requiring reading or an invented unique verbal answer.
if mode in ['sort','belongs','path']:
 s=s.replace("feedback('À toi de jouer !')", "feedback('Observe les indices. Tu pourras raconter ta stratégie à un adulte.')")
 s=s.replace("feedback('Une nouvelle partie te propose d’autres découvertes.')", "feedback('Raconte à un adulte comment tu as trouvé, si tu en as envie.')")
if not desc:raise Exception('Description manquante')
s=re.sub(r'(<h1 class="club-title" id="play-title">.*?</h1>)<p>.*?</p>',lambda m:m.group(1)+'<p>'+desc+'</p>',s,count=1)
subject='francais' if cfg['cat']=='lettre' else 'developpement_global'
meta={'level':'prescolaire_5','subject':subject,'domain':cfg['cat'],'skill':desc,'official_scope':'cycle','platform_year':'prescolaire_5','progress_state':'entrainement','difficulty':2,'prerequisites':['Explorer les activités correspondantes des 4 ans'],'game_type':mode,'reading_load':'faible','answer_key':'Clé propre à la manche; activités expressives sans réponse unique signalées comme telles.','feedback':'Réécoute, essais libres et accompagnement possible.','source_tag':{'guide':'Guide_plateforme_Quebec.pdf, sections 4 à 6','url':'https://www.quebec.ca/education/prescolaire-primaire-et-secondaire/programmes-formations-evaluation/programme-formation-ecole-quebecoise/education-prescolaire','verified':'2026-11-15','status':'Progression de plateforme dans le programme-cycle commun; aucune exigence annuelle locale inventée.'}}
s=s.replace('</head>','<script type="application/json" id="learning-metadata">'+json.dumps(meta,ensure_ascii=False)+'</script></head>')
(p/target).write_text(s);print(target+' : '+mode+' : '+desc)
