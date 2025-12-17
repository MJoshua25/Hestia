# 📋 PRD — GESTION DES ÉVÉNEMENTS & PAGE D'ACCUEIL

**Produit :** Gestionnaire de Foyer pour Jeunes Filles  
**Features :** Gestion des Événements + Page d'Accueil  
**Version :** 1.0 (MVP)  
**Date :** Décembre 2024  
**Owner :** Product Architect

---

# PARTIE 1 : GESTION DES ÉVÉNEMENTS

## 1. 📖 CONTEXTE & PROBLÈME

### Background
Les événements (fêtes, sorties culturelles, ateliers, réunions) sont au cœur de la vie du foyer. Actuellement, leur organisation repose sur :
- 📝 Cahiers papier ou Google Docs pour noter les dates
- 💬 Groupes WhatsApp pour communiquer les détails
- 🤷 Confusion sur "qui fait quoi" et "quand"

### Problèmes Actuels
- **⏱️ Perte d'informations** : Détails d'événements éparpillés entre notes, messages, emails
- **😤 Difficulté de planification** : Impossible de voir rapidement les événements à venir
- **❌ Absence de traçabilité** : Pas d'historique des événements passés
- **🔀 Communication inefficace** : Informations non centralisées

### Pourquoi maintenant ?
Avec 30+ membres et plusieurs événements par mois, la gestion manuelle devient chaotique. L'équipe de direction a besoin d'un outil centralisé pour :
- Créer et publier des événements visibles par tous
- Organiser les commissions associées aux événements
- Consulter l'historique des événements

### Impact Business Attendu
- **-60% du temps** passé à communiquer les détails d'événements
- **100% de visibilité** : Tous les membres voient les événements à venir
- **Meilleure préparation** : Vue anticipée pour constituer les commissions

---

## 2. 🎯 OBJECTIFS & NON-OBJECTIFS

### ✅ Objectifs (Ce qu'on fait)

1. **Créer des événements facilement**  
   Interface simple pour Admin/Déléguée avec champs essentiels (Titre, Date, Lieu, Description)

2. **Visualiser les événements à venir**  
   Liste chronologique accessible à tous les membres

3. **Gérer le cycle de vie**  
   Modifier ou supprimer un événement si nécessaire

4. **Associer des commissions**  
   Lier des commissions à un événement (étape suivante après création)

5. **Mobile-first**  
   Consultation et création optimisées pour smartphone

### ❌ Non-Objectifs (Ce qu'on ne fait PAS dans ce MVP)

- ❌ Duplication d'événement (version future)
- ❌ Événements récurrents (ex: réunion mensuelle automatique)
- ❌ Système de notification push (hors scope)
- ❌ Calendrier interactif avec vue mensuelle/hebdomadaire (liste simple suffit)
- ❌ Export iCal ou synchronisation Google Calendar
- ❌ Commentaires ou discussions sur un événement
- ❌ Inscription/désinscription individuelle aux événements

---

## 3. 👥 USER STORIES & CRITÈRES D'ACCEPTATION

### 🔹 US-E01 : Créer un événement

**En tant qu'** Admin ou Déléguée  
**Je veux** créer un nouvel événement  
**Afin de** informer tous les membres et préparer l'organisation

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée en tant qu'Admin ou Déléguée
WHEN j'accède à la page "Créer un événement"
THEN je vois un formulaire avec les champs :
  - Titre* (obligatoire)
  - Description (textarea, optionnel)
  - Date (date picker, optionnel)
  - Lieu (texte, optionnel)

GIVEN je remplis uniquement le champ "Titre" avec "Soirée de Noël"
WHEN je soumets le formulaire
THEN l'événement est créé avec succès
AND je suis redirigée vers la page détail de l'événement
AND un message s'affiche : "Événement créé avec succès"
AND je vois une option "Ajouter des commissions"

GIVEN je laisse le champ "Titre" vide
WHEN je tente de soumettre
THEN le formulaire affiche : "Le titre est obligatoire"
AND la soumission est bloquée

GIVEN je remplis tous les champs (Titre, Date, Lieu, Description)
WHEN je soumets le formulaire
THEN l'événement est créé avec toutes les informations
AND tous les membres peuvent voir cet événement dans la liste
```

---

### 🔹 US-E02 : Voir la liste des événements

**En tant que** n'importe quel utilisateur (Admin, Déléguée, Membre)  
**Je veux** consulter la liste de tous les événements  
**Afin de** savoir ce qui est prévu et quand

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée (n'importe quel rôle)
WHEN j'accède à la page "Événements"
THEN je vois une liste d'événements triés par date (du plus proche au plus éloigné)
AND chaque carte d'événement affiche : Titre | Date | Lieu (si renseigné)

GIVEN la liste contient 30 événements
WHEN j'affiche la page
THEN je vois 20 événements par page (pagination)
AND je vois les boutons de pagination en bas

GIVEN un événement n'a pas de date
WHEN je consulte la liste
THEN cet événement apparaît en bas de la liste (dans une section "Sans date")

GIVEN je suis sur mobile (viewport < 768px)
WHEN j'affiche la liste
THEN les événements s'affichent en cards empilées
AND chaque card est tactile (44px min de hauteur)

GIVEN il existe des événements passés (date < aujourd'hui)
WHEN j'affiche la liste
THEN je vois deux sections : "Événements à venir" et "Événements passés"
AND les événements passés sont repliés par défaut (accordéon)
```

---

### 🔹 US-E03 : Voir le détail d'un événement

**En tant que** n'importe quel utilisateur  
**Je veux** consulter tous les détails d'un événement  
**Afin de** connaître les informations complètes et voir les commissions associées

#### Critères d'Acceptation

```gherkin
GIVEN je clique sur un événement "Soirée de Noël"
WHEN la page de détail s'affiche
THEN je vois :
  - Titre : "Soirée de Noël"
  - Date : "15 décembre 2024" (ou "Date non définie")
  - Lieu : "Salle principale" (ou masqué si vide)
  - Description complète (ou "Aucune description")
  - Section "Commissions associées" (liste ou "Aucune commission")

GIVEN je suis Admin ou Déléguée
WHEN je consulte le détail
THEN je vois les boutons : "Modifier" | "Supprimer" | "Gérer les commissions"

GIVEN je suis une Membre simple
WHEN je consulte le détail
THEN je NE vois PAS les boutons de modification/suppression
AND je vois uniquement les informations en lecture seule
```

---

### 🔹 US-E04 : Modifier un événement

**En tant qu'** Admin ou Déléguée  
**Je veux** modifier les informations d'un événement  
**Afin de** corriger des erreurs ou mettre à jour les détails

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée en tant qu'Admin ou Déléguée
AND je suis sur la page détail de "Soirée de Noël"
WHEN je clique sur "Modifier"
THEN je suis redirigée vers un formulaire pré-rempli avec les données actuelles

GIVEN je modifie la date de "15 décembre" à "20 décembre"
WHEN je soumets le formulaire
THEN les modifications sont enregistrées
AND je suis redirigée vers la page détail
AND un message s'affiche : "Événement mis à jour avec succès"

GIVEN l'événement a déjà 3 commissions assignées
WHEN je modifie le titre ou la date
THEN les commissions restent attachées à l'événement
AND aucune commission n'est supprimée ou modifiée
```

---

### 🔹 US-E05 : Supprimer un événement

**En tant qu'** Admin  
**Je veux** supprimer un événement  
**Afin de** retirer les événements annulés ou créés par erreur

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée en tant qu'Admin
AND je suis sur la page détail de "Soirée de Noël"
WHEN je clique sur "Supprimer"
THEN une modale de confirmation s'affiche :
  "⚠️ Êtes-vous sûr de vouloir supprimer cet événement ?"
  "Cette action supprimera également toutes les commissions associées."
AND je vois deux options : "Annuler" | "Confirmer la suppression"

GIVEN je clique sur "Confirmer la suppression"
WHEN la suppression s'exécute
THEN l'événement est supprimé définitivement de la base de données
AND toutes les commissions liées sont également supprimées
AND toutes les assignations de membres sont supprimées
AND je suis redirigée vers la liste des événements
AND un message s'affiche : "Événement supprimé avec succès"

GIVEN je suis une Déléguée
WHEN je consulte un événement
THEN je ne vois PAS de bouton "Supprimer" (réservé Admin uniquement)
AND je vois uniquement le bouton "Modifier"
```

---

### 🔹 US-E06 : Lier des commissions à un événement

**En tant qu'** Admin ou Déléguée  
**Je veux** accéder à la gestion des commissions depuis un événement  
**Afin de** organiser les équipes de travail pour cet événement

#### Critères d'Acceptation

```gherkin
GIVEN je suis sur la page détail de "Soirée de Noël"
AND aucune commission n'est encore créée
WHEN je clique sur "Gérer les commissions"
THEN je suis redirigée vers la page "Créer des commissions"
AND le contexte de l'événement est pré-rempli (ID de l'événement)

GIVEN l'événement a déjà 3 commissions (Décoration, Cuisine, Animation)
WHEN je consulte le détail de l'événement
THEN je vois la liste des 3 commissions dans une section dédiée
AND chaque commission affiche : Nom | Nombre de membres assignés / Capacité max

GIVEN je clique sur une commission "Décoration"
WHEN la page s'affiche
THEN je vois le détail de cette commission
AND je peux gérer les membres assignés
```

---

## 4. 🎨 UX/UI REQUIREMENTS

### User Flow : Créer un événement

```
[Liste des Événements]
    ↓ Clic "Créer un événement"
[Formulaire Création]
    → Titre* | Description | Date | Lieu
    ↓ Validation côté client
    ↓ Soumission
[Page Détail Événement]
    → "Événement créé ✓"
    → Affichage des infos
    → Bouton "Gérer les commissions"
```

### User Flow : Consulter un événement

```
[Page d'Accueil ou Liste Événements]
    ↓ Clic sur carte événement
[Page Détail]
    → Titre, Date, Lieu, Description
    → Section Commissions (liste ou vide)
    → Actions (si Admin/Déléguée) : Modifier | Supprimer
```

### Wireframe Mobile : Liste des Événements

```
┌─────────────────────────┐
│  ☰  ÉVÉNEMENTS      🔍  │ ← Header sticky
├─────────────────────────┤
│ [+ Créer un événement]  │ ← Action principale
├─────────────────────────┤
│ ÉVÉNEMENTS À VENIR      │
│ ┌─────────────────────┐ │
│ │ 🎄 Soirée de Noël   │ │
│ │ 📅 15 déc 2024      │ │
│ │ 📍 Salle principale │ │
│ └─────────────────────┘ │
│                         │
│ ┌─────────────────────┐ │
│ │ 🎨 Atelier peinture │ │
│ │ 📅 22 déc 2024      │ │
│ │ 📍 Atelier          │ │
│ └─────────────────────┘ │
├─────────────────────────┤
│ ▼ ÉVÉNEMENTS PASSÉS     │
└─────────────────────────┘
```

### Wireframe Desktop : Détail d'un Événement

```
┌──────────────────────────────────────────────────┐
│  Gestionnaire de Foyer    [Modifier] [Supprimer] │
├──────────────────────────────────────────────────┤
│                                                  │
│  🎄 SOIRÉE DE NOËL                               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                  │
│  📅 Date : 15 décembre 2024, 19h00               │
│  📍 Lieu : Salle principale                      │
│                                                  │
│  📝 Description :                                │
│  Grande soirée festive pour célébrer Noël avec  │
│  repas, animations et spectacle.                │
│                                                  │
│  ───────────────────────────────────────────────│
│                                                  │
│  👥 COMMISSIONS ASSOCIÉES (3)                    │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │ 🎨 Décoration       5/8 membres          │   │
│  │ 🍽️ Cuisine          4/6 membres          │   │
│  │ 🎭 Animation        3/5 membres          │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  [+ Gérer les commissions]                      │
│                                                  │
└──────────────────────────────────────────────────┘
```

### États d'Interface

| **État** | **Description** | **Visuel** |
|----------|----------------|-----------|
| **Loading** | Chargement des événements | Skeleton cards (3 placeholders) |
| **Empty State** | Aucun événement | Illustration + "Créer votre premier événement" |
| **Past Events** | Événements terminés | Section repliée avec accordéon |
| **No Date** | Événement sans date | Badge "Date à définir" |
| **Success Toast** | Création/modification | "✓ Événement créé/modifié avec succès" |

---

## 5. 📊 MÉTRIQUES DE SUCCÈS (KPIs)

### Métriques Quantitatives

| **KPI** | **Objectif** | **Mesure** |
|---------|--------------|-----------|
| **Temps de création d'un événement** | < 1 minute | Analytics formulaire → validation |
| **Taux d'adoption** | 100% des événements dans l'app | 0 événement géré hors système |
| **Consultation événements** | 80% des membres consultent les événements | Analytics pages vues |
| **Taux de complétion formulaire** | > 90% | Soumissions réussies / tentatives |

### Métriques Qualitatives

- **Feedback Admin/Déléguée** : "Je ne perds plus de temps à envoyer les détails par message"
- **Feedback Membres** : "Je sais toujours ce qui est prévu"

---

## 6. ⚠️ RISQUES & MITIGATIONS

### Risque #1 : Suppression accidentelle d'événement avec commissions

**Probabilité :** Moyenne  
**Impact :** Critique (perte de données)

**Mitigation :**
- ✅ Modale de confirmation claire mentionnant la suppression des commissions
- ✅ Log des suppressions dans Django Admin
- ✅ Soft delete en V2 si besoin

---

### Risque #2 : Confusion sur les événements sans date

**Probabilité :** Faible  
**Impact :** Faible (UX dégradée)

**Mitigation :**
- ✅ Section dédiée "Sans date" en bas de liste
- ✅ Badge visuel "Date à définir"

---

## 7. 📌 NOTES POUR L'ÉQUIPE TECH

### Backend (Django)

🔴 **Critique :**
- **Cascade DELETE** : Supprimer un événement doit supprimer commissions + assignations (tester avec transactions)
- **Validation dates** : Accepter NULL pour le champ date, gérer le tri en SQL

🟠 **Important :**
- Ajouter un champ `status` (draft/published) pour V2
- Index sur `date` pour performance

### Frontend (Vue.js + Tailwind)

🔴 **Critique :**
- **Mobile-first** : Tester les cards tactiles
- **Empty states** : Gérer visuellement les événements sans commissions

---

# PARTIE 2 : PAGE D'ACCUEIL

## 1. 📖 CONTEXTE & PROBLÈME

### Background
La page d'accueil est le **point d'entrée** de l'application. Elle doit :
- Donner une vision d'ensemble de l'activité du foyer
- Permettre un accès rapide aux actions fréquentes
- Adapter le contenu selon le rôle de l'utilisateur

### Problèmes Actuels
- Pas de dashboard centralisé
- Perte de temps à naviguer pour trouver les infos importantes
- Pas de vision d'ensemble de l'activité

---

## 2. 🎯 OBJECTIFS & NON-OBJECTIFS

### ✅ Objectifs

1. **Dashboard adaptatif** selon le rôle (Admin/Déléguée vs Membre)
2. **Stats clés** pour Admin/Déléguée
3. **Prochains événements** visibles par tous
4. **Actions rapides** pour Admin/Déléguée
5. **Navigation fluide** vers toutes les sections

### ❌ Non-Objectifs

- ❌ Graphiques avancés (courbes, camemberts)
- ❌ Export PDF du dashboard
- ❌ Personnalisation des widgets

---

## 3. 👥 USER STORIES & CRITÈRES D'ACCEPTATION

### 🔹 US-H01 : Page d'accueil pour Admin/Déléguée

**En tant qu'** Admin ou Déléguée  
**Je veux** voir un dashboard avec des stats et actions rapides  
**Afin de** piloter l'activité du foyer efficacement

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée en tant qu'Admin ou Déléguée
WHEN j'accède à la page d'accueil
THEN je vois 4 widgets principaux :
  1. 📊 Statistiques (cartes métriques)
  2. 📅 Prochains événements (liste des 5 prochains)
  3. ⚡ Actions rapides (boutons CTA)
  4. 🧭 Navigation principale (menu)

GIVEN je consulte le widget "Statistiques"
WHEN la page charge
THEN je vois 3 cartes :
  - "X Membres actifs"
  - "X Événements à venir"
  - "X Commissions en cours"

GIVEN je consulte le widget "Prochains événements"
WHEN la page charge
THEN je vois les 5 prochains événements triés par date
AND chaque événement affiche : Titre | Date | Nombre de commissions

GIVEN je consulte le widget "Actions rapides"
WHEN la page charge
THEN je vois 3 boutons :
  - "+ Créer un événement"
  - "+ Ajouter un membre"
  - "📥 Importer des membres"

GIVEN je clique sur "+ Créer un événement"
WHEN l'action s'exécute
THEN je suis redirigée vers le formulaire de création d'événement
```

---

### 🔹 US-H02 : Page d'accueil pour Membre

**En tant que** Membre  
**Je veux** voir mes prochains événements et mes commissions  
**Afin de** savoir ce qui m'attend

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée en tant que Membre
WHEN j'accède à la page d'accueil
THEN je vois 2 widgets principaux :
  1. 📅 Mes prochains événements (où je suis assignée)
  2. 👥 Mes commissions (liste de mes assignations)

GIVEN je n'ai aucune commission assignée
WHEN j'affiche la page d'accueil
THEN je vois le message : "Vous n'avez pas encore de commission assignée"

GIVEN je suis assignée à 2 commissions
WHEN j'affiche la page d'accueil
THEN je vois la liste de mes 2 commissions avec :
  - Nom de l'événement
  - Nom de la commission
  - Membres de l'équipe
```

---

### 🔹 US-H03 : Navigation principale

**En tant que** n'importe quel utilisateur  
**Je veux** accéder facilement aux différentes sections  
**Afin de** naviguer dans l'application

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée
WHEN j'affiche la page d'accueil
THEN je vois un menu de navigation avec :
  - 🏠 Accueil
  - 👥 Membres
  - 📅 Événements
  - 📋 Commissions
  - 📤 Exports
  - 👤 Mon Profil

GIVEN je suis une Membre simple
WHEN j'affiche le menu
THEN les liens "Membres" et "Exports" sont grisés (accès interdit)
AND je vois une info-bulle : "Réservé aux Admin/Déléguées"

GIVEN je suis sur mobile
WHEN j'affiche la page
THEN le menu est un burger menu (☰)
AND il s'ouvre en overlay latéral
```

---

## 4. 🎨 UX/UI REQUIREMENTS

### Wireframe Mobile : Accueil Admin/Déléguée

```
┌─────────────────────────┐
│  ☰  ACCUEIL         👤  │
├─────────────────────────┤
│                         │
│ 📊 STATISTIQUES         │
│ ┌───────────────────┐   │
│ │ 👥 42 Membres     │   │
│ └───────────────────┘   │
│ ┌───────────────────┐   │
│ │ 📅 5 Événements   │   │
│ └───────────────────┘   │
│ ┌───────────────────┐   │
│ │ 📋 12 Commissions │   │
│ └───────────────────┘   │
│                         │
│ ⚡ ACTIONS RAPIDES      │
│ [+ Créer événement]     │
│ [+ Ajouter membre]      │
│ [📥 Importer]           │
│                         │
│ 📅 PROCHAINS ÉVÉNEMENTS │
│ ┌───────────────────┐   │
│ │ Soirée de Noël    │   │
│ │ 15 déc · 3 comm.  │   │
│ └───────────────────┘   │
│ ┌───────────────────┐   │
│ │ Atelier peinture  │   │
│ │ 22 déc · 2 comm.  │   │
│ └───────────────────┘   │
└─────────────────────────┘
```

### Wireframe Desktop : Accueil Admin/Déléguée

```
┌────────────────────────────────────────────────────────┐
│  Gestionnaire de Foyer                         [👤 ▼] │
├────────────────────────────────────────────────────────┤
│  🏠 Accueil  │  👥 Membres  │  📅 Événements  │ ...   │
├────────────────────────────────────────────────────────┤
│                                                        │
│  📊 STATISTIQUES                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ 👥       │  │ 📅       │  │ 📋       │            │
│  │ 42       │  │ 5        │  │ 12       │            │
│  │ Membres  │  │ Événem.  │  │ Commiss. │            │
│  └──────────┘  └──────────┘  └──────────┘            │
│                                                        │
│  ⚡ ACTIONS RAPIDES                                    │
│  [+ Créer événement]  [+ Ajouter membre]  [📥 Import] │
│                                                        │
│  📅 PROCHAINS ÉVÉNEMENTS                               │
│  ┌──────────────────────────────────────────────┐     │
│  │ Soirée de Noël       15 déc · 3 commissions │     │
│  │ Atelier peinture     22 déc · 2 commissions │     │
│  │ Réunion mensuelle    30 déc · 0 commission  │     │
│  └──────────────────────────────────────────────┘     │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Wireframe Mobile : Accueil Membre

```
┌─────────────────────────┐
│  ☰  ACCUEIL         👤  │
├─────────────────────────┤
│                         │
│ 📅 MES ÉVÉNEMENTS       │
│ ┌───────────────────┐   │
│ │ Soirée de Noël    │   │
│ │ Commission: Déco  │   │
│ │ 15 déc 2024       │   │
│ └───────────────────┘   │
│                         │
│ 👥 MES COMMISSIONS      │
│ ┌───────────────────┐   │
│ │ Décoration        │   │
│ │ Soirée de Noël    │   │
│ │ 5 membres         │   │
│ └───────────────────┘   │
│ ┌───────────────────┐   │
│ │ Cuisine           │   │
│ │ Atelier peinture  │   │
│ │ 4 membres         │   │
│ └───────────────────┘   │
└─────────────────────────┘
```

---

## 5. 📊 MÉTRIQUES DE SUCCÈS (KPIs)

| **KPI** | **Objectif** | **Mesure** |
|---------|--------------|-----------|
| **Temps de chargement** | < 1 seconde | Core Web Vitals (LCP) |
| **Utilisation actions rapides** | 70% des créations via accueil | Analytics clics CTA |
| **Taux de rebond** | < 20% | Google Analytics |

---

## 6. 📌 NOTES POUR L'ÉQUIPE TECH

### Backend (Django)

🔴 **Critique :**
- **Requêtes optimisées** : Utiliser `select_related()` pour charger stats + événements en 1-2 queries
- **Cache** : Mettre en cache les stats (5 min) pour Admin

### Frontend (Vue.js + Tailwind)

🔴 **Critique :**
- **Skeleton loading** : Afficher des placeholders pendant le chargement des stats
- **Responsive** : Tester sur iPhone SE et iPad

---

## 7. 📅 TIMELINE ESTIMÉE

| **Phase** | **Durée** | **Livrables** |
|-----------|-----------|---------------|
| **Models Événements** | 1 jour | Model + migrations |
| **CRUD Événements** | 4 jours | Vues Liste, Détail, Créer, Modifier, Supprimer |
| **Page d'accueil** | 3 jours | Dashboard adaptatif + stats |
| **Navigation** | 1 jour | Menu responsive |
| **Tests** | 2 jours | Tests unitaires + corrections |
| **Total** | **11 jours** (~2 semaines) |

---

## ✅ CHECKLIST DE VALIDATION

- [ ] Création/modification/suppression d'événements fonctionnelle
- [ ] Liste événements triée par date
- [ ] Dashboard affiche les bonnes stats selon le rôle
- [ ] Actions rapides redirigent correctement
- [ ] Navigation responsive (burger menu sur mobile)
- [ ] Tests sur iOS et Android
- [ ] Performance < 1s sur 4G

---

## 🎉 CONCLUSION

Ce PRD couvre :
1. **Gestion des Événements** : CRUD complet, lien avec commissions
2. **Page d'Accueil** : Dashboard adaptatif, stats, navigation

**Prochaine étape :** PRD pour la **Gestion des Commissions & Attribution** ! 🎯
