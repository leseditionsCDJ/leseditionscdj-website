from pathlib import Path
import re,json,sys,subprocess
root=Path(__file__).resolve().parents[1]; p=root/'plateforme-educative'
age=int(sys.argv[1]);suffix=sys.argv[2]
src=p/('prescolaire-4-ans-'+suffix+'.html'); dst=p/(f'prescolaire-{age}-ans-'+suffix+'.html')
s=subprocess.check_output(['git','show','98b97f68ba3c7457a34456872da4d248f217a4a0:plateforme-educative/'+src.name],cwd=root,text=True) if age==5 else src.read_text();cfg=json.loads(re.search(r'const CFG=(.*?);',s).group(1));mode=cfg['mode']; maximum=31 if age==5 else 15
if 'CLUB_NUMBERS' in s: raise Exception('Already adapted')
s=s.replace('prescolaire-4-ans',f'prescolaire-{age}-ans').replace('Préscolaire 4 ans',f'Préscolaire {age} ans').replace('>4 ans<',f'>{age} ans<')
s=s.replace('<body class="club-page">',f'<body class="club-page" data-number-age="{age}">')
s=s.replace('</head>','<link rel="stylesheet" href="assets/prescolaire-nombres.css"></head>')
s=s.replace('<script>const CFG=', '<script src="assets/prescolaire-nombres.js"></script><script>const CFG=',1)
s=s.replace("STORE='club4-'+CFG.cat+'-'+CFG.slug+'-v1'",f"STORE='club{age}-'+CFG.cat+'-'+CFG.slug+'-nombres-v2'")
# Supports two-digit numbers as digits, never the fallback drawing.
s=s.replace("/^[A-Za-zÀ-ÿ0-9]$/", "/^(?:[A-Za-zÀ-ÿ]|[0-9]{1,2})$/")
s=s.replace('font-size="88" fill="#fffaf0"','font-size="${String(k).length>1?64:88}" fill="#fffaf0"')
s=s.replace("if(MODE==='numberListen')return sample([1,2,3,4,5].map(n=>({n})),5,'bank');", "if(['numberListen','numberMatch','countTouch','feed','countMake','equal','moreLess','share'].includes(MODE))return sample(CLUB_NUMBERS.values().map(n=>({n,k:pick(OBJECTS),c:pick(COLORS)})),Math.min(6,CLUB_NUMBERS.values().length),'bank-'+CLUB_NUMBERS.key);if(['numberOrder','numberMissing'].includes(MODE))return sample(CLUB_NUMBERS.values().map(n=>({n})),Math.min(6,CLUB_NUMBERS.values().length),'bank-'+CLUB_NUMBERS.key);")
s=s.replace("ask(`Touche ${num?'le chiffre':'la lettre'} ${k}.`);let pool=num?['1','2','3','4','5']:LETTERS;choose([k,...shuffle(pool.filter(x=>x!==k)).slice(0,2)],k);", "ask(`Touche ${num?'le nombre':'la lettre'} ${k}.`);let pool=num?CLUB_NUMBERS.values().map(String):LETTERS;choose([k,...shuffle(pool.filter(x=>x!==k)).slice(0,num&&CLUB_NUMBERS.age===5?3:2)],k);postNumberChoices();")
# Numeric render branches are adapted individually; inactive modes stay intact.
if mode=='numberMatch':
 s=s.replace("let nums=[n,...shuffle([1,2,3,4,5].filter(x=>x!==n)).slice(0,2)];", "let nums=[n,...shuffle(CLUB_NUMBERS.values().filter(x=>x!==n)).slice(0,2)];")
 s=s.replace('Quel panier contient ${n} ${label(k)}${n>1?\'s\':\'\'} ?', 'Quel panier contient ${n} objets ?')
 s=s.replace('<div class="collection">${Array(v)', '<div class="collection number-collection">${Array(v)')
if mode=='numberOrder':
 s=s.replace("let len=round<2?3:5;ask(`Touche les chiffres dans l’ordre, de 1 à ${len}.`);let idx=1,b=box();shuffle(Array.from({length:len},(_,i)=>i+1))", "let len=round<2?3:5,low=Math.max(CLUB_NUMBERS.min,Math.min(d.n,CLUB_NUMBERS.max-len+1)),end=low+len-1;ask(`Touche les nombres dans l’ordre, de ${low} à ${end}.`);let idx=low,b=box();shuffle(Array.from({length:len},(_,i)=>low+i))")
 s=s.replace("if(idx>len)win('Le train des chiffres", "if(idx>end)win('Le train des nombres")
 s=s.replace('Cherche le chiffre ${idx}.','Cherche le nombre ${idx}.')
if mode=='numberMissing':
 s=s.replace("let len=3+round%3,missing=rand(1,len);ask('Un chiffre est caché. Lequel manque dans cette suite ?');let b=box('display-model collection');for(let i=1;i<=len;i++)", "let len=3+round%3,low=Math.max(CLUB_NUMBERS.min,Math.min(d.n,CLUB_NUMBERS.max-len+1)),missing=rand(low,low+len-1);ask('Un nombre est caché. Lequel manque dans cette suite ?');let b=box('display-model collection');for(let i=low;i<low+len;i++)")
 s=s.replace("shuffle([1,2,3,4,5].filter(x=>x!==missing))", "shuffle(CLUB_NUMBERS.values().filter(x=>x!==missing))")
if mode=='countTouch': s=s.replace("let count=0,b=box();shuffle(Array.from({length:n}", "let count=0,b=box('tiles number-touch-grid');shuffle(Array.from({length:n}")
if mode in ['feed','countMake','equal']:
 s=s.replace("`Prépare autant de ${label(other[0])}s que dans le modèle.`:`Prépare ${n} ${label(k)}${n>1?'s':''}.", "`Prépare autant d’objets que dans le modèle.`:`Prépare ${n} objets.")
 s=s.replace("if(count<7)","if(count<CLUB_NUMBERS.max+2)")
 s=s.replace("function collection(n,k,c,parent=$('play')){let b=box('collection',parent);", "function collection(n,k,c,parent=$('play')){let b=box('collection number-collection',parent);")
 s=s.replace("const tray=box('display-model collection')", "const tray=box('display-model collection number-collection')")
if mode=='moreLess':
 s=s.replace("let a=n,b=n===5?rand(1,4):rand(n+1,6),more=round%2===0;", "let a=n,b=pick(CLUB_NUMBERS.values().filter(v=>v!==a)),more=round%2===0;")
 s=s.replace('<div class="collection">${Array(v)', '<div class="collection number-collection">${Array(v)')
if mode=='share':
 old=re.search(r"else if\(MODE==='share'\)\{.*?(?=\nelse if)",s).group(0)
 new="""else if(MODE==='share'){let count=n,done=0;ask(`Donne un cadeau à chacun des ${count} animaux. Touche chaque animal une seule fois.`);let b=box('tiles number-touch-grid');for(let i=0;i<count;i++){let e=btn('ours',e=>{if(e.disabled)return;e.disabled=true;e.classList.add('done');e.insertAdjacentHTML('beforeend',art('cadeau',c));done++;feedback(`${done} cadeaux distribués sur ${count}.`);if(done===count)win(`Chaque animal a reçu un cadeau : ${count} cadeaux distribués !`)},{color:COLORS[i%6],label:`Animal ${i+1}`});b.append(e)}}"""
 s=s.replace(old,new)
# Keep useful feedback and a visible fallback on devices with no speech synthesis.
s=s.replace("function wrong(b,t='Prends ton temps. Tu peux essayer un autre choix.')", "function wrong(b,t='Regarde bien les nombres. Tu peux réécouter la consigne et essayer encore.')")
s=s.replace("function start(){", "function postNumberChoices(){document.querySelectorAll('#play .tile').forEach(e=>e.querySelectorAll('svg').forEach(svg=>svg.setAttribute('aria-hidden','true')))}\nfunction start(){")
desc={ 'numberListen':f'Écouter et reconnaître les nombres, par paliers, jusqu’à {maximum}.','numberMatch':f'Associer les nombres à des collections, par paliers jusqu’à {maximum}.','numberOrder':f'Remettre trois à cinq nombres consécutifs dans l’ordre, jusqu’à {maximum}.','numberMissing':f'Retrouver un nombre caché dans une suite, jusqu’à {maximum}.','countTouch':f'Compter des collections, par paliers jusqu’à {maximum}.','feed':f'Préparer une provision exacte, par paliers jusqu’à {maximum} objets.','countMake':f'Préparer une commande illustrée, jusqu’à {maximum} objets.','equal':f'Reproduire une quantité avec d’autres objets, jusqu’à {maximum}.','moreLess':f'Comparer deux collections contenant jusqu’à {maximum} objets chacune.','share':f'Donner un cadeau à chaque animal, jusqu’à {maximum} animaux.'}[mode]
s=re.sub(r'(<h1 class="club-title" id="play-title">.*?</h1>)<p>.*?</p>',lambda m:m.group(1)+'<p>'+desc+'</p>',s,count=1)
if mode in ['numberListen','numberMatch','numberOrder','numberMissing']:
 s=s.replace('Les chiffres qui parlent','Les nombres qui parlent').replace('Le chiffre et ses trésors','Le nombre et ses trésors').replace('Le train des chiffres','Le train des nombres').replace('Le chiffre disparu','Le nombre disparu')
meta={'level':f'prescolaire_{age}','subject':'mathematique','domain':'premieres_mathematiques','skill':desc,'official_scope':'cycle','platform_year':f'prescolaire_{age}','progress_state':'decouverte','difficulty':2 if age==5 else 1,'prerequisites':['Explorer les premiers nombres avec un adulte'],'game_type':mode,'reading_load':'faible','answer_key':'Nombre demandé ou règle de quantité indiquée dans la consigne.','feedback':'Essais libres, réécoute et rétroaction immédiate.','source_tag':{'guide':'Guide_plateforme_Quebec.pdf, sections 4 à 6','url':'https://www.quebec.ca/education/prescolaire-primaire-et-secondaire/programmes-formations-evaluation/programme-formation-ecole-quebecoise/education-prescolaire','verified':'2026-11-15','numeric_limit':'Recommandation de plateforme demandée par la propriétaire, pas un seuil prescrit par le ministère','max':maximum}}
s=s.replace('</head>', '<script type="application/json" id="learning-metadata">'+json.dumps(meta,ensure_ascii=False)+'</script></head>')
dst.write_text(s);print(dst.relative_to(root))
