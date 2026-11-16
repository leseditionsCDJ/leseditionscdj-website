# Livraison — 70 jeux du préscolaire 5 ans

## Résultat

70 jeux jouables, répartis dans les 14 catégories de la page des 4 ans. Le sélecteur « Préscolaire · 5 ans » ouvre la nouvelle page d’accueil. Chaque création a été vérifiée puis sauvegardée par un commit distinct avant de passer au jeu suivant.

Les cinq jeux de nombres et les cinq jeux de quantités des 4 ans ont aussi été adaptés jusqu’à 15. Les nombres des 5 ans vont jusqu’à 31. Ces plafonds sont les choix de progression demandés par la propriétaire, pas des exigences annuelles ministérielles.

La progression comprend les majuscules et minuscules, 14 couleurs, 9 formes, quatre grandeurs à comparer, davantage d’objets à mémoriser et plusieurs étapes ou contraintes de placement. Les consignes s’écoutent en français; les essais restent libres, sans chronomètre ni note. Les pauses et activités expressives n’ont pas de réponse unique imposée.

Les nouveaux jeux reprennent le thème, les composants et les illustrations vectorielles des jeux existants. Les jeux couleurs/formes/espace proposent des versions adaptées des mécanismes de reconnaissance, tri, recherche, reproduction, mélange et parcours; ils ne sont pas des copies graphiques identiques de toutes les grandes scènes illustrées des 4 ans.

## Vérifications effectuées

- 1 125 manches résolues dans les validations initiales des 70 jeux des 5 ans.
- 330 manches résolues dans les validations initiales des 10 jeux numériques des 4 ans.
- 12 vérifications supplémentaires à la borne supérieure (15 ou 31) après exclusion des images de paires de bottes dans les collections à compter.
- Deux parcours supplémentaires de 7 manches pour vérifier la cohérence des couleurs des pièces d’espace avec leur modèle.
- Navigation réelle : année → 14 catégories → 70 jeux → retours; aucun échec JavaScript ou HTTP local.
- 720 liens et ressources locaux contrôlés; identifiants HTML uniques, métadonnées pédagogiques présentes, scripts JavaScript analysés sans erreur de syntaxe.
- Parcours sur navigateur à 1280 px et contrôles à 390 px; captures mobiles produites pendant les tests. Pas de débordement horizontal détecté.
- Paliers numériques : chaque nombre de chaque plage peut apparaître; erreurs, réécoute, progression, fin, nouvelle partie, stockage indisponible et persistance contrôlés.

## Limites de la validation

La synthèse vocale est simulée dans les tests pour contrôler les phrases et les parcours sans dépendre des voix du système. La qualité audible réelle et le toucher sur une tablette physique restent à vérifier. La référence pédagogique est le guide fourni et le programme-cycle québécois; aucun document d’une commission scolaire particulière n’a été fourni et aucune certification locale n’est revendiquée.

La lecture HTTP du domaine de production depuis cet environnement renvoie 403. Cloudflare Pages a confirmé le déploiement de prévisualisation du commit 3a16b62 : https://b358b7c3.leseditionscdj-website.pages.dev . Les lectures HTTP du domaine de production et de cette prévisualisation depuis cet environnement renvoient 403; la confirmation de déploiement provient du contrôle Cloudflare sur GitHub, et non d’un test distant du navigateur. La branche n’est pas fusionnée dans main et la production n’a pas été modifiée.

## Reprise

Lire d’abord `REPRISE.md`, puis `suivi.json` et `JOURNAL.md`. Les 70 entrées du suivi sont terminées; ne pas les recréer à partir des anciens messages de clavardage. La branche est `codex/prescolaire-5-ans`.

## Liens de livraison

- Proposition GitHub : https://github.com/leseditionsCDJ/leseditionscdj-website/pull/2
- Catalogue en prévisualisation : https://b358b7c3.leseditionscdj-website.pages.dev/plateforme-educative/prescolaire-5-ans
- Prévisualisation de la branche : https://codex-prescolaire-5-ans.leseditionscdj-website.pages.dev/plateforme-educative/prescolaire-5-ans
