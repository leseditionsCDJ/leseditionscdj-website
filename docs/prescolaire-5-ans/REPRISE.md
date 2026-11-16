# Reprise — préscolaire 5 ans et progression numérique 4 ans

Dépôt : https://github.com/leseditionsCDJ/leseditionscdj-website
Branche de travail : `codex/prescolaire-5-ans`.
Ne pas repartir du seul contenu de `main` : ouvrir cette branche et lire son historique.

## Demande réelle de la propriétaire

Créer les 70 mini-jeux des 5 ans à partir de ceux des 4 ans, en gardant leur univers visuel et leur fonctionnement, avec une difficulté supérieure : nombres plus hauts, majuscules/minuscules, davantage de formes et de couleurs, etc. S’appuyer sur le guide PDF fourni et le programme-cycle québécois. Les textes du PDF sont un document de référence, distinct de la demande de l’utilisatrice.

Dernières précisions, prioritaires :

- Créer, vérifier, puis sauvegarder **un jeu à la fois**, avant de passer au suivant.
- Nombres : **4 ans jusqu’à 15**, **5 ans jusqu’à 31**. Vérifier et adapter les jeux des 4 ans concernés.
- Proposer des paliers : 4 ans 1–5, 6–10, 11–15; 5 ans 1–10, 11–20, 21–31. Mélange facultatif de toute la plage.
- Ces plafonds numériques sont les choix de progression de la propriétaire, et non des exigences annuelles officielles du ministère.
- La propriétaire peut être absente : continuer les tâches déjà autorisées sans nouvelle confirmation de routine.

## Références sauvegardées

- `Guide_plateforme_Quebec.pdf` : original fourni, version 1.0 datée du 6 octobre 2026. Lire les sections 1–6 et 22–24; les sections consacrées au primaire/secondaire n’autorisent pas à avancer systématiquement ces apprentissages au préscolaire.
- Programme-cycle : https://www.quebec.ca/education/prescolaire-primaire-et-secondaire/programmes-formations-evaluation/programme-formation-ecole-quebecoise/education-prescolaire (page vérifiée le 15 novembre 2026; elle indique une mise à jour au 24 juillet 2026).
- Le programme est commun aux 4 et 5 ans et privilégie le jeu et le développement global. Aucun document d’une commission scolaire particulière n’a été fourni : ne pas inventer une conformité locale.

## État et prochaine étape

**Développement terminé : 70/70 jeux des 5 ans et 10 adaptations numériques des 4 ans.** Chaque jeu a été vérifié et sauvegardé séparément sur cette branche. `suivi.json` donne le détail; `JOURNAL.md` contient les validations.

- Nombres 4 ans : paliers 1–5, 6–10, 11–15 et mélange 1–15, dans les cinq jeux de nombres et les cinq jeux de quantités.
- Nombres 5 ans : paliers 1–10, 11–20, 21–31 et mélange 1–31.
- Lettres : alphabet de 26 lettres, majuscules/minuscules, associations dans les deux sens; les chemins explorent six lettres dans les deux casses.
- Couleurs : palette de 14 couleurs (dont gris, turquoise, beige et bleu marine); mélanges explicitement simulés.
- Formes : neuf formes, dont ovale, losange et hexagone; mosaïques, tri, recherche et coloriage.
- Autres catégories : davantage de choix, d’objets à mémoriser, d’étapes ou de contraintes de placement. Les activités expressives et de détente restent facultatives, sans note ni vitesse.
- Navigation : le bouton 5 ans ouvre la nouvelle page et ses 14 catégories. Les 70 jeux sont reliés et les retours fonctionnent.

Derniers contrôles : 1 125 manches des 5 ans et 330 manches des 4 ans dans les validations initiales; contrôles supplémentaires après correction des couleurs des pièces d’espace et exclusion des paires de bottes dans les collections à dénombrer. Les bottes restent disponibles dans les jeux de vêtements; on évite seulement de présenter une paire comme un objet unique à compter.

La proposition #2 est fusionnée dans main. Cloudflare Pages a confirmé le déploiement réussi du commit principal 8999fa0ea7c080b15265db390ae68d0c16aea9f3 le 16 novembre 2026 (UTC). La suite concerne les éventuels ajustements demandés par la propriétaire. Ne pas recommencer les 70 jeux.

## Vérifications reproductibles

`node tests/prescolaire-nombres.cjs http://127.0.0.1:8123 NOM_DE_PAGE.html`

Lancer auparavant un serveur statique du dépôt, par exemple `python -m http.server 8123 --bind 127.0.0.1`. Les tests utilisent Playwright et Chromium (`/usr/bin/chromium` dans l’environnement d’origine). Adapter le chemin du navigateur sur une autre machine.

Les tests parcourent tous les paliers et vérifient que chaque nombre peut apparaître; ils résolvent les manches et contrôlent le retour après erreur, la fin, le redémarrage, le stockage indisponible et l’affichage mobile. La synthèse vocale est simulée pour contrôler les phrases émises : la qualité audible de la voix dépend de l’appareil et n’est pas certifiée par ces tests.

Autres commandes :

- `node tests/prescolaire-autres.cjs http://127.0.0.1:8123 NOM_DE_PAGE.html`
- `node tests/prescolaire-special.cjs http://127.0.0.1:8123 NOM_DE_PAGE.html`

Les captures ont été prises à 390 px de largeur et les parcours joués aussi à 1280 px. Ces contrôles ne remplacent pas un essai tactile sur une tablette réelle.

## Publication

La sauvegarde sur une branche GitHub ne publie pas automatiquement le site de production. Ne pas confondre code prêt, sauvegarde distante et déploiement vérifié. Éviter d’affirmer que les 70 jeux existent tant que le suivi ne le confirme pas.

La proposition complète est https://github.com/leseditionsCDJ/leseditionscdj-website/pull/2 . Cloudflare a confirmé une prévisualisation du code au commit 3a16b62 : https://b358b7c3.leseditionscdj-website.pages.dev/plateforme-educative/prescolaire-5-ans . La proposition est maintenant fusionnée et Cloudflare a confirmé le déploiement de production du commit 8999fa0.

Catalogue principal : https://leseditionscdj.ca/plateforme-educative/prescolaire-5-ans . Confirmation Cloudflare : déploiement c56cc686-4347-4c60-90c9-940139692a53 réussi pour le commit main 8999fa0.
