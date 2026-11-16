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

Consulter `suivi.json` pour les 70 jeux. Un jeu n’est terminé que lorsque ses tests passent et son code est sauvegardé sur cette branche. Les catégories non prêtes sont explicitement affichées « En préparation », sans lien cassé.

Terminé et vérifié : premier jeu des 5 ans, `prescolaire-5-ans-chiffre-ecoute.html` (« Les nombres qui parlent »). Quatre choix, nombres à deux chiffres correctement illustrés, paliers jusqu’à 31, essais libres et audio français.

Prochaine étape : adapter séparément les cinq jeux `prescolaire-4-ans-chiffre-*.html`, puis les cinq jeux `prescolaire-4-ans-quantite-*.html`. Ajouter ensuite les autres jeux des 5 ans, chacun avec une vérification et un commit distinct.

## Vérifications reproductibles

`node tests/prescolaire-nombres.cjs http://127.0.0.1:8123 NOM_DE_PAGE.html`

Lancer auparavant un serveur statique du dépôt, par exemple `python -m http.server 8123 --bind 127.0.0.1`. Le test utilise Playwright et Chromium (`/usr/bin/chromium` dans l’environnement d’origine). Adapter le chemin du navigateur sur une autre machine.

Les tests parcourent tous les paliers et vérifient que chaque nombre peut apparaître; ils résolvent les manches et contrôlent le retour après erreur, la fin, le redémarrage, le stockage indisponible et l’affichage mobile. La synthèse vocale est simulée pour contrôler les phrases émises : la qualité audible de la voix dépend de l’appareil et n’est pas certifiée par ces tests.

## Publication

La sauvegarde sur une branche GitHub ne publie pas automatiquement le site de production. Ne pas confondre code prêt, sauvegarde distante et déploiement vérifié. Éviter d’affirmer que les 70 jeux existent tant que le suivi ne le confirme pas.
