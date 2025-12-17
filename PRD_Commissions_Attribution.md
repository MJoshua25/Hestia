# 📋 PRD — GESTION DES COMMISSIONS & ATTRIBUTION ALÉATOIRE

**Produit :** Gestionnaire de Foyer pour Jeunes Filles  
**Feature :** Gestion des Commissions & Attribution Automatique/Manuelle  
**Version :** 1.0 (MVP)  
**Date :** Décembre 2025  
**Owner :** Product Architect

---

## 1. 📖 CONTEXTE & PROBLÈME

### Background
Chaque événement au foyer nécessite la constitution d'**équipes de travail** (commissions) pour assurer son bon déroulement. Actuellement, la répartition des membres dans ces commissions se fait :
- ✍️ Manuellement sur papier ou tableau blanc
- 🎲 "À la volée" sans méthode structurée
- 😤 Souvent les mêmes personnes dans les mêmes rôles
- ⏱️ Perte de temps pour équilibrer les équipes

### Problèmes à Résoudre
- **❌ Déséquilibre** : Certaines commissions surchargées, d'autres sous-effectif
- **⏱️ Temps de répartition** : 30-45 minutes pour attribuer manuellement 30 membres dans 5 commissions
- **🤷 Oublis** : Certaines membres ne sont jamais sollicitées, d'autres toujours
- **📊 Pas de traçabilité** : Impossible de savoir qui a fait quoi sur les événements passés

### Pourquoi maintenant ?
Avec la multiplication des événements (4-6 par mois) et la croissance du foyer (30+ membres), le système manuel atteint ses limites. L'équipe de direction a besoin de :
- Constituer rapidement des équipes équilibrées
- Respecter les contraintes d'effectifs (min/max)
- Conserver une flexibilité pour ajuster manuellement si besoin

### Impact Business Attendu
- **-80% du temps** passé à répartir les membres (de 30 min à 5 min)
- **100% de couverture** : Toutes les membres participent équitablement
- **Équité perçue** : Répartition aléatoire évite les favoritismes
- **Meilleure préparation** : Export immédiat des listes pour les chefs de commission

---

## 2. 🎯 OBJECTIFS & NON-OBJECTIFS

### ✅ Objectifs (Ce qu'on fait)

1. **Créer des commissions pour un événement**  
   Interface flexible permettant de créer une ou plusieurs commissions avec contraintes min/max

2. **Attribution automatique intelligente**  
   Algorithme d'attribution aléatoire respectant les contraintes et équilibrant les effectifs

3. **Attribution manuelle**  
   Permettre aux Admin/Déléguée d'attribuer manuellement des membres si nécessaire

4. **Modification post-attribution**  
   Déplacer, ajouter, retirer des membres après l'attribution initiale

5. **Réinitialisation flexible**  
   Possibilité de relancer l'algorithme ou de tout réinitialiser à zéro

6. **Visualisation claire**  
   Tableau récapitulatif toujours visible avec état de chaque commission

7. **Export multi-format**  
   Génération Excel et PDF des attributions par commission

8. **Warnings intelligents**  
   Alertes si contraintes non respectables (sans blocage)

### ❌ Non-Objectifs (Ce qu'on ne fait PAS dans ce MVP)

- ❌ Historique des participations (pour équilibrage sur plusieurs événements)
- ❌ Préférences des membres (choix de commission)
- ❌ Algorithme d'optimisation complexe (équilibrage sur compétences)
- ❌ Notifications automatiques aux membres assignés
- ❌ Système de validation/acceptation par les membres
- ❌ Gestion des disponibilités (calendrier)
- ❌ Drag & drop visuel entre commissions (V2)

---

## 3. 👥 USER STORIES & CRITÈRES D'ACCEPTATION

### 🔹 US-C01 : Créer une commission pour un événement

**En tant qu'** Admin ou Déléguée  
**Je veux** créer une ou plusieurs commissions pour un événement  
**Afin de** définir les équipes de travail nécessaires

#### Critères d'Acceptation

```gherkin
GIVEN je suis sur la page détail de l'événement "Soirée de Noël"
AND je clique sur "Gérer les commissions"
WHEN j'accède à la page de création
THEN je vois un formulaire avec les champs (tous optionnels) :
  - Nom (ex: "Décoration")
  - Description (textarea)
  - Capacité MIN (nombre)
  - Capacité MAX (nombre)
  - Responsable (dropdown liste des membres)

GIVEN je crée une commission avec uniquement le nom "Décoration"
WHEN je soumets le formulaire
THEN la commission est créée avec :
  - Nom : "Décoration"
  - Description : vide
  - MIN : 0 (par défaut)
  - MAX : illimité (par défaut)
  - Responsable : aucun

GIVEN je crée une commission avec MIN = 3 et MAX = 8
WHEN je soumets
THEN la commission est créée avec ces contraintes
AND je suis redirigée vers la liste des commissions de cet événement

GIVEN je veux créer 5 commissions d'un coup
WHEN je clique sur "Ajouter plusieurs commissions"
THEN un formulaire dynamique s'affiche avec :
  - 5 blocs de formulaire (un par commission)
  - Bouton "+" pour ajouter un bloc
  - Bouton "-" pour supprimer un bloc
  - Bouton "Créer toutes les commissions"

GIVEN je soumets 5 commissions en une fois
WHEN je valide
THEN les 5 commissions sont créées simultanément
AND je vois la liste des 5 commissions pour cet événement
```

---

### 🔹 US-C02 : Voir la liste des commissions d'un événement

**En tant qu'** n'importe quel utilisateur  
**Je veux** consulter la liste des commissions d'un événement  
**Afin de** voir l'organisation prévue

#### Critères d'Acceptation

```gherkin
GIVEN je suis sur la page détail de l'événement "Soirée de Noël"
AND cet événement a 3 commissions : Décoration, Cuisine, Animation
WHEN j'affiche la section "Commissions"
THEN je vois un tableau avec 3 lignes :
  | Nom         | Description | MIN | MAX | Membres | Responsable | Actions |
  | Décoration  | ...         | 3   | 8   | 0/8     | Non défini  | ✏️ 🗑️   |
  | Cuisine     | ...         | 4   | 6   | 0/6     | Alice D.    | ✏️ 🗑️   |
  | Animation   | ...         | 2   | 5   | 0/5     | Non défini  | ✏️ 🗑️   |

GIVEN je suis Admin ou Déléguée
WHEN j'affiche cette liste
THEN je vois en plus :
  - Bouton "Attribuer automatiquement"
  - Bouton "Attribuer manuellement"
  - Bouton "+ Ajouter une commission"

GIVEN je suis une Membre simple
WHEN j'affiche cette liste
THEN je vois uniquement les informations (lecture seule)
AND je ne vois PAS les boutons d'actions
```

---

### 🔹 US-C03 : Sélectionner les membres disponibles pour attribution

**En tant qu'** Admin ou Déléguée  
**Je veux** sélectionner les membres qui participeront à cet événement  
**Afin de** définir le pool de personnes à attribuer aux commissions

#### Critères d'Acceptation

```gherkin
GIVEN je clique sur "Attribuer automatiquement"
WHEN l'interface de sélection s'affiche
THEN je vois :
  - Liste de tous les membres actifs (42 membres)
  - Tous les membres sont pré-sélectionnés par défaut (checkbox cochée)
  - Bouton "Tout sélectionner" / "Tout désélectionner"
  - Compteur : "42 membres sélectionnés"
  - Bouton "Lancer l'attribution"

GIVEN je désélectionne 5 membres (absentes)
WHEN je mets à jour la sélection
THEN le compteur affiche : "37 membres sélectionnés"

GIVEN je suis sur mobile (viewport < 768px)
WHEN j'affiche la liste
THEN les membres s'affichent en cards
AND chaque card a une checkbox tactile (44px min)

GIVEN je recherche "Dupont" dans la barre de recherche
WHEN je tape le nom
THEN seuls les membres contenant "Dupont" s'affichent
AND les autres sont masqués (mais restent sélectionnés si déjà cochés)
```

---

### 🔹 US-C04 : Attribution automatique avec algorithme

**En tant qu'** Admin ou Déléguée  
**Je veux** lancer l'attribution automatique des membres aux commissions  
**Afin de** gagner du temps et assurer une répartition équitable

#### Critères d'Acceptation

```gherkin
GIVEN j'ai 3 commissions :
  - Décoration (MIN 3, MAX 8)
  - Cuisine (MIN 4, MAX 6)
  - Animation (MIN 2, MAX 5)
AND j'ai sélectionné 15 membres
WHEN je clique sur "Lancer l'attribution"
THEN l'algorithme s'exécute et :
  1. Vérifie que MIN de toutes les commissions ≤ total membres (3+4+2=9 ≤ 15) ✓
  2. Attribue aléatoirement en remplissant d'abord les MIN
  3. Répartit les membres restants pour équilibrer les effectifs
  4. Affiche un résumé :
     "✓ 15 membres répartis avec succès"
     - Décoration : 5 membres (5/8)
     - Cuisine : 5 membres (5/6)
     - Animation : 5 membres (5/5)

GIVEN la somme des MIN dépasse le nombre de membres sélectionnés
  (MIN total = 15, mais seulement 12 membres sélectionnés)
WHEN je tente de lancer l'attribution
THEN le système affiche un warning :
  "⚠️ Impossible de respecter tous les minimums
  Somme des MIN : 15 | Membres sélectionnés : 12
  Propositions :
  - Réduire les minimums
  - Sélectionner 3 membres supplémentaires
  - Forcer l'attribution (certains MIN ne seront pas respectés)"
AND je vois trois boutons :
  - "Annuler"
  - "Ajuster les MIN automatiquement"
  - "Forcer l'attribution"

GIVEN je clique sur "Forcer l'attribution"
WHEN l'algorithme s'exécute
THEN il attribue au mieux (best effort)
AND affiche :
  "⚠️ Attribution réalisée avec des minimums non respectés :
  - Décoration : 4/5 MIN (manque 1)
  - Cuisine : 4/6 MIN (respecté)
  - Animation : 4/4 MIN (respecté)"

GIVEN toutes les commissions ont MIN = 0 et je sélectionne 10 membres pour 5 commissions
WHEN l'algorithme s'exécute
THEN il répartit équitablement : 2-2-2-2-2
```

---

### 🔹 US-C05 : Visualiser le résultat de l'attribution

**En tant qu'** Admin ou Déléguée  
**Je veux** voir immédiatement le résultat de l'attribution  
**Afin de** vérifier la répartition et faire des ajustements si nécessaire

#### Critères d'Acceptation

```gherkin
GIVEN l'attribution automatique vient de se terminer
WHEN je consulte la page des commissions
THEN je vois un tableau récapitulatif :

┌─────────────────────────────────────────────────┐
│ COMMISSION DÉCORATION (5/8 membres)             │
├─────────────────────────────────────────────────┤
│ ✓ Alice DUPONT (Chambre 101)                    │
│ ✓ Bob MARTIN (Chambre 203)           [Retirer] │
│ ✓ Claire BERNARD (Chambre 102)       [Retirer] │
│ ✓ David LEROY (Chambre 104)          [Retirer] │
│ ✓ Emma PETIT (Chambre 205)           [Retirer] │
│ [+ Ajouter un membre]                           │
└─────────────────────────────────────────────────┘

GIVEN je vois ce tableau
THEN en haut de la page, je vois :
  - Résumé : "15 membres répartis dans 3 commissions"
  - Bouton "Relancer l'attribution"
  - Bouton "Réinitialiser tout"
  - Bouton "Exporter (Excel / PDF)"

GIVEN je suis sur mobile
WHEN j'affiche ce tableau
THEN chaque commission est une card empilée
AND je peux déplier/replier chaque card
```

---

### 🔹 US-C06 : Attribution manuelle d'un membre à une commission

**En tant qu'** Admin ou Déléguée  
**Je veux** attribuer manuellement un membre à une commission  
**Afin de** avoir un contrôle total même sans l'algorithme

#### Critères d'Acceptation

```gherkin
GIVEN je suis sur la page des commissions
AND aucune attribution automatique n'a encore été faite
WHEN je clique sur "Attribuer manuellement"
THEN je vois une interface avec :
  - Liste des commissions (colonnes)
  - Liste des membres disponibles (sidebar ou dropdown)
  - Pour chaque commission : bouton "Ajouter un membre"

GIVEN je clique sur "Ajouter un membre" dans la commission "Décoration"
WHEN un dropdown s'affiche
THEN je vois la liste de tous les membres
AND les membres déjà attribués à une autre commission sont grisés

GIVEN je sélectionne "Alice DUPONT" et valide
WHEN l'ajout est confirmé
THEN Alice apparaît dans la commission "Décoration"
AND Alice est retirée de la liste des membres disponibles
AND le compteur de la commission passe à 1/8

GIVEN je tente d'ajouter Alice à une 2ème commission
WHEN je cherche son nom dans le dropdown
THEN elle n'apparaît pas (déjà attribuée)
OR elle apparaît grisée avec mention "(Déjà dans : Décoration)"
```

---

### 🔹 US-C07 : Déplacer un membre d'une commission à une autre

**En tant qu'** Admin ou Déléguée  
**Je veux** déplacer un membre d'une commission vers une autre  
**Afin de** ajuster manuellement la répartition

#### Critères d'Acceptation

```gherkin
GIVEN Alice est actuellement dans "Décoration"
AND je veux la déplacer vers "Cuisine"
WHEN je clique sur le bouton "..." à côté de son nom dans "Décoration"
THEN je vois un menu déroulant :
  - "Déplacer vers une autre commission"
  - "Retirer de cette commission"

GIVEN je clique sur "Déplacer vers une autre commission"
WHEN un dropdown s'affiche
THEN je vois la liste des autres commissions :
  - Cuisine (4/6) [Sélectionnable]
  - Animation (5/5) [Grisé - pleine]

GIVEN je sélectionne "Cuisine" et valide
WHEN le déplacement s'exécute
THEN Alice est retirée de "Décoration" (4/8)
AND Alice est ajoutée à "Cuisine" (5/6)
AND un message s'affiche : "Alice DUPONT déplacée vers Cuisine"

GIVEN je tente de déplacer Alice vers "Animation" (déjà pleine 5/5)
WHEN je clique sur cette option
THEN un warning s'affiche :
  "⚠️ Animation a atteint sa capacité maximale (5/5)
  Voulez-vous quand même l'ajouter ?"
AND je peux confirmer ou annuler
```

---

### 🔹 US-C08 : Retirer un membre d'une commission

**En tant qu'** Admin ou Déléguée  
**Je veux** retirer un membre d'une commission  
**Afin de** libérer sa place ou corriger une erreur

#### Critères d'Acceptation

```gherkin
GIVEN Alice est dans "Décoration" (5/8)
WHEN je clique sur "Retirer" à côté de son nom
THEN une modale de confirmation s'affiche :
  "Retirer Alice DUPONT de la commission Décoration ?"
  [Annuler] [Confirmer]

GIVEN je confirme le retrait
WHEN l'action s'exécute
THEN Alice est retirée de "Décoration" (4/8)
AND Alice redevient disponible pour attribution
AND un message s'affiche : "Alice DUPONT retirée de Décoration"

GIVEN la commission "Décoration" a un MIN = 5 et contient 5 membres
WHEN je tente de retirer un membre
THEN un warning s'affiche :
  "⚠️ En retirant ce membre, le minimum (5) ne sera plus respecté (4/5)
  Continuer quand même ?"
AND je peux confirmer ou annuler
```

---

### 🔹 US-C09 : Relancer l'attribution automatique

**En tant qu'** Admin ou Déléguée  
**Je veux** relancer l'algorithme d'attribution  
**Afin de** obtenir une nouvelle répartition aléatoire

#### Critères d'Acceptation

```gherkin
GIVEN j'ai déjà réalisé une première attribution (15 membres répartis)
AND je veux obtenir une nouvelle répartition
WHEN je clique sur "Relancer l'attribution"
THEN une modale de confirmation s'affiche :
  "⚠️ L'attribution actuelle sera effacée et remplacée
  15 membres seront à nouveau répartis aléatoirement
  Continuer ?"
  [Annuler] [Confirmer]

GIVEN je confirme
WHEN l'algorithme se relance
THEN toutes les attributions actuelles sont effacées
AND l'algorithme réattribue les 15 membres (potentiellement différemment)
AND je vois le nouveau résultat

GIVEN j'ai modifié manuellement certaines attributions après l'algo initial
WHEN je relance l'attribution
THEN mes modifications manuelles sont perdues
AND l'algorithme repart de zéro
```

---

### 🔹 US-C10 : Réinitialiser toutes les attributions

**En tant qu'** Admin  
**Je veux** réinitialiser complètement les attributions  
**Afin de** repartir de zéro (vider toutes les commissions)

#### Critères d'Acceptation

```gherkin
GIVEN j'ai des attributions en cours (15 membres répartis)
WHEN je clique sur "Réinitialiser tout"
THEN une modale de confirmation s'affiche :
  "⚠️ ATTENTION : Toutes les attributions seront supprimées
  Les commissions resteront mais seront vidées
  Cette action est irréversible"
  [Annuler] [Confirmer la réinitialisation]

GIVEN je confirme
WHEN la réinitialisation s'exécute
THEN tous les membres sont retirés de toutes les commissions
AND les compteurs passent à 0/MAX
AND un message s'affiche : "Toutes les attributions ont été réinitialisées"
AND je reviens à l'état initial (commissions vides)

GIVEN je suis une Déléguée
WHEN j'essaie d'accéder à cette fonction
THEN je vois le bouton grisé avec tooltip : "Réservé aux Admin"
```

---

### 🔹 US-C11 : Supprimer une commission

**En tant qu'** Admin ou Déléguée  
**Je veux** supprimer une commission  
**Afin de** corriger une erreur ou retirer une commission inutile

#### Critères d'Acceptation

```gherkin
GIVEN je suis sur la liste des commissions
AND la commission "Animation" contient 5 membres
WHEN je clique sur l'icône "🗑️" de cette commission
THEN une modale de confirmation s'affiche :
  "Supprimer la commission Animation ?
  ⚠️ Les 5 membres attribués seront libérés pour réattribution"
  [Annuler] [Supprimer]

GIVEN je confirme la suppression
WHEN l'action s'exécute
THEN la commission "Animation" est supprimée de la base
AND les 5 membres deviennent à nouveau disponibles
AND un message s'affiche : "Commission Animation supprimée"

GIVEN cette commission était vide (0 membres)
WHEN je la supprime
THEN elle est supprimée sans warning supplémentaire
```

---

### 🔹 US-C12 : Export Excel des attributions

**En tant qu'** Admin ou Déléguée  
**Je veux** exporter les attributions au format Excel  
**Afin de** distribuer les listes aux chefs de commission

#### Critères d'Acceptation

```gherkin
GIVEN j'ai réalisé l'attribution pour l'événement "Soirée de Noël"
AND les commissions sont : Décoration (5), Cuisine (5), Animation (5)
WHEN je clique sur "Exporter" puis "Excel"
THEN un fichier Excel se télécharge : "Soiree_de_Noel_Commissions.xlsx"

GIVEN j'ouvre ce fichier Excel
THEN je vois une structure avec :
  - 1 onglet par commission : "Décoration", "Cuisine", "Animation"
  - Chaque onglet contient un tableau :
    | Prénom | Nom     | Chambre | Téléphone   |
    | Alice  | DUPONT  | 101     | 0612345678  |
    | Bob    | MARTIN  | 203     | 0698765432  |
    | ...

GIVEN une commission a un responsable défini
THEN dans l'onglet, la première ligne indique :
  "Responsable : Alice DUPONT"
```

---

### 🔹 US-C13 : Export PDF des attributions

**En tant qu'** Admin ou Déléguée  
**Je veux** exporter les attributions au format PDF  
**Afin de** afficher les listes au mur ou distribuer en version imprimée

#### Critères d'Acceptation

```gherkin
GIVEN j'ai réalisé l'attribution pour l'événement "Soirée de Noël"
WHEN je clique sur "Exporter" puis "PDF"
THEN un fichier PDF se télécharge : "Soiree_de_Noel_Commissions.pdf"

GIVEN j'ouvre ce fichier PDF
THEN je vois :
  - Page de garde :
    "SOIRÉE DE NOËL - 15 décembre 2024
    Répartition des commissions
    15 membres répartis dans 3 commissions"
  
  - Page 1 : Commission Décoration
    ┌──────────────────────────────────┐
    │ COMMISSION DÉCORATION (5 membres)│
    │ Responsable : Alice DUPONT       │
    ├──────────────────────────────────┤
    │ 1. Alice DUPONT (Chambre 101)    │
    │ 2. Bob MARTIN (Chambre 203)      │
    │ 3. Claire BERNARD (Chambre 102)  │
    │ ...                              │
    └──────────────────────────────────┘
  
  - Page 2 : Commission Cuisine
  - Page 3 : Commission Animation

GIVEN je suis sur mobile
WHEN je clique sur "Exporter PDF"
THEN le PDF s'ouvre dans le navigateur mobile
AND je peux le télécharger ou le partager
```

---

### 🔹 US-C14 : Modifier une commission existante

**En tant qu'** Admin ou Déléguée  
**Je veux** modifier les informations d'une commission  
**Afin de** corriger son nom, ses contraintes ou son responsable

#### Critères d'Acceptation

```gherkin
GIVEN je suis sur la liste des commissions
AND la commission "Décoration" a MIN=3, MAX=8
WHEN je clique sur l'icône "✏️" de cette commission
THEN un formulaire d'édition s'affiche avec les valeurs actuelles

GIVEN je modifie MIN de 3 à 5
AND je modifie le responsable de "Aucun" à "Alice DUPONT"
WHEN je soumets le formulaire
THEN la commission est mise à jour
AND un message s'affiche : "Commission modifiée avec succès"

GIVEN cette commission contient déjà 4 membres
AND je modifie MIN de 3 à 5
WHEN je soumets
THEN un warning s'affiche :
  "⚠️ Le minimum (5) est supérieur au nombre actuel de membres (4)
  Voulez-vous continuer ?"
AND je peux confirmer ou annuler

GIVEN je modifie MAX de 8 à 3 alors que 4 membres sont déjà attribués
WHEN je tente de soumettre
THEN un warning s'affiche :
  "⚠️ Le maximum (3) est inférieur au nombre actuel de membres (4)
  Voulez-vous continuer ? (Aucun membre ne sera retiré automatiquement)"
```

---

## 4. 🎨 UX/UI REQUIREMENTS

### User Flow : Attribution Automatique Complète

```
[Admin consulte événement "Soirée de Noël"]
    ↓ Clic "Gérer les commissions"
[Page Gestion Commissions]
    → Affiche 3 commissions créées (vides)
    ↓ Clic "Attribuer automatiquement"
[Interface Sélection Membres]
    → Liste 42 membres (tous pré-sélectionnés)
    → Admin désélectionne 3 absentes
    → Compteur : "39 membres sélectionnés"
    ↓ Clic "Lancer l'attribution"
[Algorithme s'exécute]
    → Vérification contraintes MIN
    → Attribution aléatoire
    → Équilibrage
    ↓ Résultat en 2-3 secondes
[Tableau Récapitulatif]
    → Commission Décoration : 13 membres
    → Commission Cuisine : 13 membres
    → Commission Animation : 13 membres
    → Message : "✓ 39 membres répartis"
    → Boutons : [Relancer] [Export]
```

### User Flow : Modification Manuelle Post-Attribution

```
[Admin consulte le tableau récapitulatif]
    → Voit que Alice est dans "Décoration"
    ↓ Clic menu "..." à côté d'Alice
[Menu contextuel]
    → "Déplacer vers une autre commission"
    → "Retirer de cette commission"
    ↓ Clic "Déplacer"
[Dropdown commissions]
    → Cuisine (13/15) [Sélectionnable]
    → Animation (15/15) [Pleine]
    ↓ Sélectionne "Cuisine"
[Confirmation visuelle]
    → Alice retirée de "Décoration" (12/15)
    → Alice ajoutée à "Cuisine" (14/15)
    → Toast : "Alice déplacée vers Cuisine"
```

### Wireframe Mobile : Page Gestion Commissions

```
┌─────────────────────────┐
│  ⬅️ SOIRÉE DE NOËL      │
├─────────────────────────┤
│ 📋 COMMISSIONS (3)      │
│                         │
│ [Attribuer auto]        │
│ [Attribuer manuel]      │
│ [+ Ajouter commission]  │
├─────────────────────────┤
│ ▼ DÉCORATION (5/8)      │
│ ┌─────────────────────┐ │
│ │ Alice DUPONT (101)  │ │
│ │ Bob MARTIN (203)    │ │
│ │ Claire BERNARD (102)│ │
│ │ ...                 │ │
│ │ [+ Ajouter]         │ │
│ └─────────────────────┘ │
│                         │
│ ▼ CUISINE (5/6)         │
│ ▼ ANIMATION (5/5) [MAX] │
├─────────────────────────┤
│ [Exporter Excel]        │
│ [Exporter PDF]          │
└─────────────────────────┘
```

### Wireframe Desktop : Tableau Récapitulatif

```
┌──────────────────────────────────────────────────────────────┐
│  Soirée de Noël > Gestion des Commissions                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  📊 Résumé : 15 membres répartis dans 3 commissions          │
│                                                              │
│  [Relancer l'attribution] [Réinitialiser] [Exporter ▼]      │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │ DÉCORATION (5/8)    │  │ CUISINE (5/6)       │          │
│  │ Resp: Alice DUPONT  │  │ Resp: Non défini    │          │
│  ├─────────────────────┤  ├─────────────────────┤          │
│  │ ☑ Alice DUPONT      │  │ ☑ Emma PETIT        │          │
│  │   Ch. 101  [...]    │  │   Ch. 205  [...]    │          │
│  │ ☑ Bob MARTIN        │  │ ☑ Fatima KANE       │          │
│  │   Ch. 203  [...]    │  │   Ch. 301  [...]    │          │
│  │ ☑ Claire BERNARD    │  │ ...                 │          │
│  │ ...                 │  │ [+ Ajouter]         │          │
│  │ [+ Ajouter]         │  └─────────────────────┘          │
│  └─────────────────────┘                                    │
│                                                              │
│  ┌─────────────────────┐                                    │
│  │ ANIMATION (5/5) MAX │                                    │
│  │ Resp: David LEROY   │                                    │
│  ├─────────────────────┤                                    │
│  │ ☑ David LEROY       │                                    │
│  │ ☑ ...               │                                    │
│  │ [Capacité atteinte] │                                    │
│  └─────────────────────┘                                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Wireframe : Interface Sélection Membres

```
┌──────────────────────────────────────────────────────────────┐
│  Sélectionner les membres à attribuer                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  🔍 [Rechercher un membre...]                                │
│                                                              │
│  [Tout sélectionner] [Tout désélectionner]                  │
│                                                              │
│  ✓ 39 membres sélectionnés sur 42                           │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ☑ Alice DUPONT (Chambre 101)                               │
│  ☑ Bob MARTIN (Chambre 203)                                 │
│  ☐ Claire BERNARD (Chambre 102) [Absente]                   │
│  ☑ David LEROY (Chambre 104)                                │
│  ☐ Emma PETIT (Chambre 205) [En congé]                      │
│  ☑ Fatima KANE (Chambre 301)                                │
│  ...                                                         │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  [Annuler]          [Lancer l'attribution automatique]      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### États d'Interface

| **État** | **Description** | **Visuel** |
|----------|----------------|-----------|
| **Commissions vides** | Aucune attribution | "0/8" grisé + bouton "Attribuer" |
| **En cours d'attribution** | Algorithme actif | Spinner + "Attribution en cours..." |
| **Attribution réussie** | Résultat visible | Cartes vertes + compteurs actualisés |
| **Warning MIN non respecté** | Contrainte violée | Badge orange "⚠️ MIN non atteint (4/5)" |
| **Commission pleine** | MAX atteint | Badge rouge "MAX atteint (8/8)" |
| **Membre déplacé** | Action manuelle | Animation de déplacement + toast |

---

## 5. 🤖 ALGORITHME D'ATTRIBUTION — SPÉCIFICATIONS DÉTAILLÉES

### Pseudo-Code de l'Algorithme

```python
def attribuer_membres_automatiquement(commissions, membres_selectionnes):
    """
    Attribution aléatoire des membres aux commissions
    avec respect des contraintes MIN et équilibrage
    """
    
    # ÉTAPE 1 : Vérifications préliminaires
    total_min = sum(commission.min for commission in commissions)
    total_membres = len(membres_selectionnes)
    
    if total_min > total_membres:
        return {
            'status': 'warning',
            'message': f'MIN total ({total_min}) > Membres ({total_membres})',
            'action': 'Proposer ajustement ou forcer'
        }
    
    # ÉTAPE 2 : Mélange aléatoire des membres
    import random
    membres_shuffled = random.sample(membres_selectionnes, len(membres_selectionnes))
    
    # ÉTAPE 3 : Initialisation
    attributions = {commission.id: [] for commission in commissions}
    membres_restants = membres_shuffled.copy()
    
    # ÉTAPE 4 : Remplissage des MIN en priorité
    for commission in commissions:
        for _ in range(commission.min):
            if membres_restants:
                membre = membres_restants.pop(0)
                attributions[commission.id].append(membre)
    
    # ÉTAPE 5 : Répartition équilibrée des membres restants
    while membres_restants:
        # Trouver la commission avec le moins de membres (qui n'a pas atteint son MAX)
        commission_cible = min(
            [c for c in commissions if len(attributions[c.id]) < c.max],
            key=lambda c: len(attributions[c.id])
        )
        
        membre = membres_restants.pop(0)
        attributions[commission_cible.id].append(membre)
    
    # ÉTAPE 6 : Vérification post-attribution
    warnings = []
    for commission in commissions:
        count = len(attributions[commission.id])
        if count < commission.min:
            warnings.append(f"{commission.nom}: {count}/{commission.min} MIN")
        if count > commission.max:
            warnings.append(f"{commission.nom}: {count}/{commission.max} MAX dépassé")
    
    return {
        'status': 'success' if not warnings else 'warning',
        'attributions': attributions,
        'warnings': warnings
    }
```

### Exemples de Scénarios

#### Scénario 1 : Attribution Standard

**Entrée :**
- 3 commissions : Déco (MIN 3, MAX 8), Cuisine (MIN 4, MAX 6), Animation (MIN 2, MAX 5)
- 15 membres sélectionnés

**Traitement :**
1. Vérification : 3+4+2 = 9 ≤ 15 ✓
2. Mélange aléatoire des 15 membres
3. Attribution MIN :
   - Déco : 3 membres
   - Cuisine : 4 membres
   - Animation : 2 membres
   - Total : 9 membres attribués, reste 6
4. Équilibrage des 6 restants :
   - Déco : +2 → 5 membres
   - Cuisine : +2 → 6 membres (MAX atteint)
   - Animation : +2 → 4 membres
   
**Résultat :**
- Déco : 5/8
- Cuisine : 6/6 (MAX)
- Animation : 4/5

---

#### Scénario 2 : MIN Non Respectables

**Entrée :**
- 3 commissions : Déco (MIN 5), Cuisine (MIN 6), Animation (MIN 4)
- 12 membres sélectionnés

**Traitement :**
1. Vérification : 5+6+4 = 15 > 12 ❌
2. Affichage warning avec 3 options :
   - Ajuster MIN automatiquement
   - Sélectionner 3 membres supplémentaires
   - Forcer l'attribution (best effort)

**Si "Forcer l'attribution" :**
1. Attribution proportionnelle :
   - Déco : 4 membres (4/5 MIN)
   - Cuisine : 5 membres (5/6 MIN)
   - Animation : 3 membres (3/4 MIN)

---

#### Scénario 3 : Équilibrage Parfait

**Entrée :**
- 5 commissions : toutes avec MIN 0, MAX 10
- 25 membres sélectionnés

**Traitement :**
1. Aucun MIN à respecter
2. Répartition équilibrée pure :
   - Chaque commission : 5 membres

**Résultat :**
- 5-5-5-5-5 (parfaitement équilibré)

---

## 6. 📊 MÉTRIQUES DE SUCCÈS (KPIs)

### Métriques Quantitatives

| **KPI** | **Objectif** | **Mesure** |
|---------|--------------|-----------|
| **Temps d'attribution** | < 5 minutes (vs 30 min manuellement) | Temps écoulé de "Gérer commissions" → "Export" |
| **Taux d'utilisation de l'algo** | 80% des attributions via algo | Ratio auto vs manuel |
| **Taux d'ajustement post-algo** | < 20% des attributions modifiées | Nombre de déplacements manuels |
| **Équilibre des commissions** | Écart-type ≤ 2 membres | Calcul statistique post-attribution |
| **Taux d'export** | 90% des événements exportés | Nombre d'exports / événements |

### Métriques Qualitatives

- **Feedback Admin** : "L'algorithme me fait gagner 25 minutes par événement"
- **Perception équité** : "Personne ne se plaint de faire toujours la même chose"
- **Satisfaction membres** : NPS ≥ 8/10 sur "Justice de la répartition"

---

## 7. ⚠️ RISQUES & MITIGATIONS

### Risque #1 : Algorithme produit des résultats déséquilibrés

**Probabilité :** Faible  
**Impact :** Moyen (perception d'inéquité)

**Causes possibles :**
- Bug dans la logique d'équilibrage
- Contraintes MIN/MAX mal gérées

**Mitigation :**
- ✅ Tests unitaires exhaustifs avec 20+ scénarios
- ✅ Calcul d'écart-type post-attribution (alerte si > 3)
- ✅ Possibilité de relancer l'algo jusqu'à satisfaction
- ✅ Modification manuelle toujours possible

---

### Risque #2 : Confusion entre attribution auto et manuelle

**Probabilité :** Moyenne  
**Impact :** Faible (UX dégradée)

**Causes possibles :**
- Admin ne comprend pas qu'il peut faire les deux
- Peur de "casser" l'attribution automatique

**Mitigation :**
- ✅ Interface claire avec deux boutons distincts
- ✅ Tooltip explicatif : "Vous pouvez ajuster manuellement après l'attribution automatique"
- ✅ Tutoriel vidéo de 2 minutes

---

### Risque #3 : Export illisible ou incomplet

**Probabilité :** Faible  
**Impact :** Moyen (inutilisable)

**Causes possibles :**
- PDF mal formaté sur mobile
- Excel avec encodage UTF-8 cassé (accents)

**Mitigation :**
- ✅ Tester l'export sur 5 devices différents
- ✅ Utiliser `openpyxl` pour Excel (gestion UTF-8)
- ✅ Utiliser `reportlab` pour PDF (fonts Unicode)
- ✅ Aperçu avant export

---

### Risque #4 : Membre attribuée à 2 commissions par bug

**Probabilité :** Très faible  
**Impact :** Critique (règle métier violée)

**Causes possibles :**
- Race condition dans l'ajout manuel simultané
- Bug dans l'algorithme

**Mitigation :**
- ✅ **Contrainte unique en base de données** : `(membre_id, événement_id)` UNIQUE
- ✅ Validation côté backend avant toute attribution
- ✅ Tests d'intégrité après chaque attribution

---

### Risque #5 : Performance avec 100+ membres

**Probabilité :** Faible  
**Impact :** Moyen (attente de 10s)

**Causes possibles :**
- Algorithme non optimisé (O(n²))
- Trop de requêtes SQL

**Mitigation :**
- ✅ Algorithme en O(n log n) maximum
- ✅ Bulk insert en base (une seule transaction)
- ✅ Tester avec 200 membres avant prod

---

## 8. 📌 NOTES POUR L'ÉQUIPE TECH

### Points d'Attention Backend (Django)

🔴 **Critique :**

**Modèles Django**
```python
# core/models.py

class Commission(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='commissions')
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    min_capacity = models.IntegerField(default=0)
    max_capacity = models.IntegerField(null=True, blank=True)  # NULL = illimité
    responsible = models.ForeignKey(Member, null=True, blank=True, on_delete=models.SET_NULL, related_name='responsible_commissions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def current_count(self):
        return self.assignments.count()
    
    def is_full(self):
        if self.max_capacity is None:
            return False
        return self.current_count() >= self.max_capacity
    
    class Meta:
        verbose_name_plural = "Commissions"


class Assignment(models.Model):
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name='assignments')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Traçabilité
    
    class Meta:
        # CONTRAINTE CRITIQUE : Un membre = 1 commission par événement
        unique_together = [['commission__event', 'member']]
        indexes = [
            models.Index(fields=['commission', 'member']),
        ]
```

**Service d'attribution**
```python
# core/services/assignment_service.py

import random

class AssignmentService:
    
    @staticmethod
    def assign_automatically(event, selected_member_ids, user):
        """
        Attribue automatiquement les membres sélectionnés aux commissions
        """
        commissions = event.commissions.all()
        members = Member.objects.filter(id__in=selected_member_ids)
        
        # Vérifications
        total_min = sum(c.min_capacity for c in commissions)
        if total_min > len(members):
            return {
                'status': 'error',
                'message': f'MIN total ({total_min}) > Membres disponibles ({len(members)})'
            }
        
        # Mélange aléatoire
        members_shuffled = list(members)
        random.shuffle(members_shuffled)
        
        # Attribution
        attributions = {c.id: [] for c in commissions}
        members_remaining = members_shuffled.copy()
        
        # Remplir les MIN
        for commission in commissions:
            for _ in range(commission.min_capacity):
                if members_remaining:
                    member = members_remaining.pop(0)
                    attributions[commission.id].append(member)
        
        # Équilibrage
        while members_remaining:
            # Commission avec le moins de membres (non pleine)
            target = min(
                [c for c in commissions if len(attributions[c.id]) < (c.max_capacity or float('inf'))],
                key=lambda c: len(attributions[c.id])
            )
            member = members_remaining.pop(0)
            attributions[target.id].append(member)
        
        # Enregistrement en base (transaction atomique)
        from django.db import transaction
        with transaction.atomic():
            # Supprimer les attributions existantes
            Assignment.objects.filter(commission__event=event).delete()
            
            # Créer les nouvelles attributions
            assignments_to_create = []
            for commission_id, members_list in attributions.items():
                for member in members_list:
                    assignments_to_create.append(
                        Assignment(
                            commission_id=commission_id,
                            member=member,
                            assigned_by=user
                        )
                    )
            Assignment.objects.bulk_create(assignments_to_create)
        
        return {
            'status': 'success',
            'attributions': attributions,
            'total': sum(len(m) for m in attributions.values())
        }
```

🟠 **Important :**
- **Logs** : Logger toutes les attributions (auto + manuelles) avec timestamp et user
- **Validation** : Vérifier les contraintes MIN/MAX côté backend (pas seulement frontend)
- **Performance** : Utiliser `select_related()` et `prefetch_related()` pour charger commissions + membres

🟢 **Nice to Have :**
- Cache des résultats d'attribution (5 min) pour éviter recalculs
- Endpoint API `/api/events/{id}/commissions/preview/` pour simuler avant d'enregistrer

---

### Points d'Attention Frontend (Vue.js + Tailwind)

🔴 **Critique :**

**Composant Tableau Commissions**
```javascript
// static/js/commissions.js
const { createApp } = Vue;

createApp({
    data() {
        return {
            commissions: [],
            selectedMembers: [],
            isAssigning: false
        }
    },
    async mounted() {
        await this.loadCommissions();
    },
    methods: {
        async loadCommissions() {
            const response = await fetch(`/api/events/${eventId}/commissions/`);
            this.commissions = await response.json();
        },
        
        async assignAutomatically() {
            this.isAssigning = true;
            
            const response = await fetch(`/api/events/${eventId}/assign-auto/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    member_ids: this.selectedMembers
                })
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                await this.loadCommissions();  // Recharger
                this.showToast('✓ Attribution réussie', 'success');
            } else {
                this.showToast(result.message, 'warning');
            }
            
            this.isAssigning = false;
        },
        
        async moveMember(memberId, fromCommissionId, toCommissionId) {
            // Déplacer un membre entre commissions
            const response = await fetch(`/api/assignments/move/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    member_id: memberId,
                    from_commission: fromCommissionId,
                    to_commission: toCommissionId
                })
            });
            
            if (response.ok) {
                await this.loadCommissions();
                this.showToast('Membre déplacé', 'success');
            }
        }
    }
}).mount('#commissions-app');
```

🟠 **Important :**
- **Loading states** : Afficher spinner pendant l'attribution (peut prendre 2-3s pour 100 membres)
- **Optimistic UI** : Mettre à jour l'interface avant la réponse serveur pour fluidité
- **Validation** : Empêcher double-clic sur "Lancer l'attribution"

🟢 **Nice to Have :**
- Animation de transition quand un membre est déplacé
- Drag & drop entre commissions (V2)

---

### Points d'Attention Export

🔴 **Critique :**

**Export Excel**
```python
# core/views/export.py
from openpyxl import Workbook
from django.http import HttpResponse

def export_commissions_excel(request, event_id):
    event = Event.objects.get(id=event_id)
    commissions = event.commissions.prefetch_related('assignments__member')
    
    wb = Workbook()
    wb.remove(wb.active)  # Supprimer la feuille par défaut
    
    for commission in commissions:
        ws = wb.create_sheet(title=commission.name or f"Commission {commission.id}")
        
        # En-tête
        ws.append(['Prénom', 'Nom', 'Chambre', 'Téléphone'])
        
        # Données
        for assignment in commission.assignments.all():
            member = assignment.member
            ws.append([
                member.first_name,
                member.last_name,
                member.room,
                member.phone_number
            ])
    
    # Génération de la réponse
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"{event.title.replace(' ', '_')}_Commissions.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    wb.save(response)
    return response
```

**Export PDF**
```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def export_commissions_pdf(request, event_id):
    event = Event.objects.get(id=event_id)
    commissions = event.commissions.prefetch_related('assignments__member')
    
    response = HttpResponse(content_type='application/pdf')
    filename = f"{event.title.replace(' ', '_')}_Commissions.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    
    # Page de garde
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width/2, height-100, event.title.upper())
    p.setFont("Helvetica", 12)
    p.drawCentredString(width/2, height-130, f"Date : {event.date or 'Non définie'}")
    
    y_position = height - 200
    
    for commission in commissions:
        # Nouvelle page si nécessaire
        if y_position < 150:
            p.showPage()
            y_position = height - 50
        
        # Titre commission
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, y_position, f"{commission.name} ({commission.current_count()} membres)")
        y_position -= 30
        
        # Membres
        p.setFont("Helvetica", 12)
        for assignment in commission.assignments.all():
            member = assignment.member
            p.drawString(70, y_position, f"• {member.first_name} {member.last_name} (Ch. {member.room})")
            y_position -= 20
        
        y_position -= 30  # Espacement entre commissions
    
    p.save()
    return response
```

---

## 9. 📅 TIMELINE ESTIMÉE (Développement)

| **Phase** | **Durée** | **Livrables** |
|-----------|-----------|---------------|
| **Models Commission & Assignment** | 1 jour | Models + migrations |
| **CRUD Commissions** | 2 jours | Créer, Modifier, Supprimer |
| **Algorithme d'attribution** | 3 jours | Service + logique métier |
| **Interface sélection membres** | 1 jour | UI checkbox + compteur |
| **Tableau récapitulatif** | 2 jours | Affichage résultat + actions |
| **Attribution manuelle** | 2 jours | Ajouter, Déplacer, Retirer |
| **Export Excel + PDF** | 2 jours | Génération fichiers |
| **Tests & Edge cases** | 2 jours | Tests unitaires + intégration |
| **Total** | **15 jours** (~3 semaines) |

---

## ✅ CHECKLIST DE VALIDATION

Avant de passer en production, vérifier :

- [ ] Création/modification/suppression de commissions fonctionne
- [ ] Contrainte UNIQUE (membre, événement) active en base
- [ ] Algorithme d'attribution testé avec 10+ scénarios
- [ ] Warnings affichés si MIN non respectables
- [ ] Attribution manuelle (ajout, déplacement, retrait) fonctionnelle
- [ ] Relancer l'attribution efface bien l'attribution précédente
- [ ] Réinitialisation totale vide toutes les commissions
- [ ] Export Excel contient bien 1 onglet par commission
- [ ] Export PDF lisible sur mobile et desktop
- [ ] Tests sur 100 membres (performance < 3s)
- [ ] Interface responsive (mobile + desktop)
- [ ] Logs des attributions enregistrés

---

## 🎉 CONCLUSION

Ce PRD définit le **cœur métier** du Gestionnaire de Foyer avec :

### ✅ Fonctionnalités Principales
- Création flexible de commissions (une par une ou en masse)
- Attribution automatique intelligente (algorithme détaillé fourni)
- Attribution manuelle complète (ajout, déplacement, retrait)
- Modification post-attribution à tout moment
- Export Excel et PDF professionnel

### 🎯 Architecture Technique
- Model `Commission` avec MIN/MAX optionnels
- Model `Assignment` avec contrainte UNIQUE critique
- Service `AssignmentService` avec algorithme en O(n log n)
- Bulk insert pour performance
- Exports avec `openpyxl` et `reportlab`

### 📊 Algorithme d'Attribution
1. Vérification des contraintes MIN
2. Mélange aléatoire des membres
3. Remplissage prioritaire des MIN
4. Équilibrage du reste
5. Validation post-attribution

### ⏱️ Impact Attendu
- **-80% du temps** de répartition (de 30 min à 5 min)
- **100% d'équité** perçue (aléatoire)
- **0 conflit** (modification manuelle possible)

---

**Statut :** PRD prêt pour validation et développement ! 🚀

**Prochaines étapes suggérées :**
1. Review avec l'équipe Dev + Design
2. Estimation détaillée des user stories
3. Kick-off développement avec démo de l'algorithme
