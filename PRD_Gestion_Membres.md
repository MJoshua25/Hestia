# 📋 PRD — GESTION DES MEMBRES

**Produit :** Gestionnaire de Foyer pour Jeunes Filles  
**Feature :** Gestion des Membres  
**Version :** 1.0 (MVP)  
**Date :** Décembre 2025  
**Owner :** Product Architect

---

## 1. 📖 CONTEXTE & PROBLÈME

### Background
Les foyers pour jeunes filles organisent régulièrement des événements nécessitant la constitution de commissions de travail. La répartition des tâches repose actuellement sur une gestion manuelle (cahiers, Excel, tableaux blancs) qui génère :

- **⏱️ Perte de temps** : Mise à jour fastidieuse des listes de membres
- **❌ Erreurs** : Doublons, informations obsolètes, oublis
- **😤 Frustrations** : Difficulté à identifier rapidement les membres disponibles pour les événements

### Pourquoi maintenant ?
La croissance du nombre de résidentes (30+ membres) rend la gestion papier inefficace. L'équipe de direction (Admin + Déléguées) a besoin d'un système centralisé pour :
- Maintenir une base de données à jour des résidentes
- Faciliter la sélection des membres lors de la création de commissions
- Permettre un accès rapide aux informations de contact

### Impact Business Attendu
- **Gain de temps** : -80% du temps passé à chercher les informations des membres
- **Réduction d'erreurs** : Élimination des doublons et informations périmées
- **Meilleure expérience** : Interface mobile-first accessible depuis smartphone

---

## 2. 🎯 OBJECTIFS & NON-OBJECTIFS

### ✅ Objectifs (Ce qu'on fait)

1. **Centraliser les données membres**  
   Créer une base de données unique et fiable des résidentes du foyer

2. **Faciliter les opérations CRUD**  
   Permettre aux Admin et Déléguées de gérer facilement les membres (ajout, modification, suppression)

3. **Importer en masse**  
   Accélérer l'onboarding initial via import Excel

4. **Sécuriser l'accès**  
   Authentification passwordless pour les membres simples, login classique pour les Admin

5. **Optimiser pour mobile**  
   Interface responsive, touch-friendly, rapide sur 4G

### ❌ Non-Objectifs (Ce qu'on ne fait PAS dans ce MVP)

- ❌ Historique de participation aux événements (version future)
- ❌ Gestion du statut actif/inactif ou archivage (version future)
- ❌ Notifications par email/SMS (hors scope MVP)
- ❌ Export de la liste des membres (priorisation basse)
- ❌ Photo de profil (simple, pas critique)
- ❌ Gestion des allergies ou préférences alimentaires

---

## 3. 👥 USER STORIES & CRITÈRES D'ACCEPTATION

### 🔹 US-M01 : Créer un membre manuellement

**En tant qu'** Admin ou Déléguée  
**Je veux** ajouter une nouvelle membre via un formulaire  
**Afin de** maintenir la liste à jour quand une nouvelle fille arrive au foyer

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée en tant qu'Admin ou Déléguée
WHEN j'accède à la page "Ajouter un membre"
THEN je vois un formulaire avec les champs : Prénom*, Nom*, Numéro*, Chambre*

GIVEN je remplis tous les champs obligatoires
WHEN je soumets le formulaire
THEN le membre est créé avec succès
AND je suis redirigée vers la liste des membres
AND un message de confirmation s'affiche : "Membre ajouté avec succès"

GIVEN je soumets le formulaire avec un champ obligatoire vide
WHEN je clique sur "Enregistrer"
THEN le formulaire n'est pas soumis
AND un message d'erreur s'affiche : "Veuillez remplir tous les champs obligatoires"

GIVEN deux membres ont le même nom ET prénom
WHEN je crée le deuxième membre
THEN le système accepte la création (pas de contrainte d'unicité sur nom/prénom)
BUT affiche un avertissement : "Attention : un membre avec ce nom existe déjà"
```

---

### 🔹 US-M02 : Importer des membres via Excel

**En tant qu'** Admin  
**Je veux** importer une liste de membres via un fichier Excel  
**Afin de** gagner du temps lors de l'initialisation du système ou des inscriptions de masse

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée en tant qu'Admin
WHEN j'accède à la page "Importer des membres"
THEN je vois un bouton "Télécharger le modèle Excel"
AND je vois un champ de type "file upload" acceptant .xlsx et .xls

GIVEN je clique sur "Télécharger le modèle"
WHEN le fichier se télécharge
THEN il contient les colonnes : Prénom | Nom | Numéro | Chambre
AND il contient 2 lignes d'exemples pré-remplies

GIVEN je téléverse un fichier Excel valide avec 10 membres
WHEN je clique sur "Importer"
THEN le système valide chaque ligne
AND affiche un récapitulatif : "10 membres prêts à être importés"
AND je confirme l'import
AND les 10 membres sont créés en base de données

GIVEN le fichier contient des erreurs (numéro manquant ligne 5)
WHEN je clique sur "Importer"
THEN le système affiche : "Erreur ligne 5 : Numéro manquant"
AND l'import est bloqué jusqu'à correction

GIVEN le fichier contient plus de 100 lignes
WHEN je tente l'import
THEN le système affiche : "Maximum 100 membres par import"
AND je dois diviser mon fichier
```

---

### 🔹 US-M03 : Voir la liste des membres

**En tant qu'** Admin, Déléguée ou Membre  
**Je veux** consulter la liste de toutes les résidentes  
**Afin de** avoir une vue d'ensemble et trouver rapidement une personne

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée (n'importe quel rôle)
WHEN j'accède à la page "Membres"
THEN je vois un tableau avec les colonnes : Prénom | Nom | Numéro | Chambre | Actions
AND les membres sont affichés par ordre alphabétique (Nom A→Z)
AND je vois 20 membres par page (pagination)

GIVEN la liste contient 50 membres
WHEN je suis sur la première page
THEN je vois les membres 1 à 20
AND je vois des boutons "Page suivante" et "Première page"

GIVEN je suis sur mobile (viewport < 768px)
WHEN j'affiche la liste
THEN le tableau passe en mode "cards" empilées
AND chaque carte affiche : Prénom Nom | Chambre X | 📞 Numéro

GIVEN je tape "Dupont" dans la barre de recherche
WHEN je valide
THEN seuls les membres dont le nom OU prénom contient "Dupont" s'affichent
AND le compteur indique : "3 résultats sur 50 membres"
```

---

### 🔹 US-M04 : Modifier un membre

**En tant qu'** Admin ou Déléguée  
**Je veux** modifier les informations d'un membre existant  
**Afin de** corriger des erreurs ou mettre à jour ses données (changement de chambre, nouveau numéro)

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée en tant qu'Admin ou Déléguée
AND je suis sur la page "Détail du membre Alice Dupont"
WHEN je clique sur le bouton "Modifier"
THEN je suis redirigée vers un formulaire pré-rempli avec ses données actuelles

GIVEN je modifie la chambre de "101" à "203"
WHEN je soumets le formulaire
THEN les modifications sont enregistrées
AND je suis redirigée vers la page détail
AND un message s'affiche : "Membre mis à jour avec succès"

GIVEN je suis une Membre (rôle basique)
WHEN je consulte la fiche d'un autre membre
THEN je ne vois PAS de bouton "Modifier" (read-only)
```

---

### 🔹 US-M05 : Supprimer un membre

**En tant qu'** Admin  
**Je veux** supprimer un membre de la base  
**Afin de** retirer les personnes qui ont quitté définitivement le foyer

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée en tant qu'Admin
AND je suis sur la fiche d'Alice Dupont
WHEN je clique sur "Supprimer"
THEN une modale de confirmation s'affiche : "Êtes-vous sûr de vouloir supprimer Alice Dupont ?"
AND je vois deux options : "Annuler" | "Confirmer la suppression"

GIVEN je clique sur "Confirmer la suppression"
WHEN la suppression s'exécute
THEN le membre est supprimé définitivement de la base de données
AND je suis redirigée vers la liste des membres
AND un message s'affiche : "Alice Dupont a été supprimée"

GIVEN Alice est assignée à une commission active
WHEN je tente de la supprimer
THEN le système affiche un warning : "Ce membre est assigné à 2 commissions. Suppression impossible."
AND je dois d'abord retirer ses assignations

GIVEN je suis une Déléguée
WHEN je consulte une fiche membre
THEN je ne vois PAS de bouton "Supprimer" (réservé Admin uniquement)
```

---

### 🔹 US-M06 : Attribuer le rôle de Déléguée

**En tant qu'** Admin  
**Je veux** promouvoir un membre au rôle de Déléguée  
**Afin de** lui donner des droits d'administration (création d'événements, attribution de commissions)

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée en tant qu'Admin
AND je consulte la fiche de "Marie Martin" (actuellement Membre)
WHEN je clique sur "Promouvoir en Déléguée"
THEN une modale s'affiche : "Confirmer : Marie Martin deviendra Déléguée et pourra gérer les événements"
AND je confirme

WHEN la promotion est validée
THEN le rôle de Marie passe de "Membre" à "Déléguée"
AND Marie peut désormais créer/modifier des événements et attribuer des commissions
AND un badge "Déléguée" apparaît sur sa fiche

GIVEN Marie est déjà Déléguée
WHEN je clique sur "Révoquer le statut de Déléguée"
THEN son rôle repasse à "Membre"
AND elle perd ses droits d'administration
```

---

### 🔹 US-M07 : Authentification Passwordless (Membres)

**En tant que** Membre (rôle basique)  
**Je veux** me connecter sans mot de passe via un code envoyé par SMS  
**Afin de** accéder rapidement à l'application sans gérer de credentials

#### Critères d'Acceptation

```gherkin
GIVEN je suis sur la page de connexion
AND je suis un Membre (pas Admin/Déléguée)
WHEN je saisis mon numéro de téléphone
AND je clique sur "Recevoir un code"
THEN je reçois un SMS avec un code à 6 chiffres
AND le code est valide pendant 5 minutes

GIVEN je saisis le code reçu
WHEN je le valide
THEN je suis connectée et redirigée vers la page d'accueil
AND une session est créée (valable 7 jours)

GIVEN le code est expiré (>5 minutes)
WHEN je tente de le valider
THEN le système affiche : "Code expiré. Veuillez en demander un nouveau"

GIVEN je suis Admin ou Déléguée
WHEN j'accède à la page de connexion
THEN je vois un formulaire classique : Email + Mot de passe
AND l'option passwordless n'est PAS disponible (sécurité renforcée pour les admins)
```

---

## 4. 🎨 UX/UI REQUIREMENTS

### User Flow : Créer un membre

```
[Liste des Membres] 
    ↓ Clic "Ajouter un membre"
[Formulaire Ajout]
    → Prénom* | Nom* | Numéro* | Chambre*
    ↓ Validation côté client (champs requis)
    ↓ Soumission
[Confirmation]
    → "Membre créé ✓"
    ↓ Redirection automatique (2s)
[Liste des Membres actualisée]
```

### User Flow : Importer via Excel

```
[Liste des Membres]
    ↓ Clic "Importer depuis Excel"
[Page Import]
    → Bouton "Télécharger le modèle"
    → Zone de drag & drop ou bouton "Parcourir"
    ↓ Upload fichier .xlsx
[Validation en cours...]
    → Spinner + "Analyse du fichier..."
[Récapitulatif]
    → "✓ 45 lignes valides | ⚠️ 2 erreurs détectées"
    → Tableau des erreurs : "Ligne 12 : Numéro manquant"
    ↓ Correction fichier ou ignorer erreurs
    ↓ Clic "Confirmer l'import"
[Import réussi]
    → "45 membres importés avec succès"
    ↓ Redirection vers la liste
```

### Wireframe Mobile (Liste des Membres)

```
┌─────────────────────────┐
│  ☰  MEMBRES         🔍  │ ← Header sticky
├─────────────────────────┤
│ [+ Ajouter] [📥 Importer]│ ← Actions principales
├─────────────────────────┤
│ ┌─────────────────────┐ │
│ │ 👤 Alice DUPONT     │ │ ← Card tactile (44px min)
│ │ Chambre 101         │ │
│ │ 📞 06 12 34 56 78   │ │
│ │ [Modifier] [Détails]│ │
│ └─────────────────────┘ │
│                         │
│ ┌─────────────────────┐ │
│ │ 👤 Bob MARTIN       │ │
│ │ Chambre 203         │ │
│ │ 📞 07 98 76 54 32   │ │
│ │ [Modifier] [Détails]│ │
│ └─────────────────────┘ │
├─────────────────────────┤
│ ← 1 2 3 ... 10 →        │ ← Pagination
└─────────────────────────┘
```

### Wireframe Desktop (Tableau)

```
┌────────────────────────────────────────────────────────┐
│  Gestionnaire de Foyer          [+ Ajouter] [📥 Import]│
├────────────────────────────────────────────────────────┤
│  Membres (87)                         🔍 [Recherche...]│
├─────────┬─────────┬────────────┬─────────┬────────────┤
│ Prénom  │ Nom     │ Numéro     │ Chambre │ Actions    │
├─────────┼─────────┼────────────┼─────────┼────────────┤
│ Alice   │ DUPONT  │ 0612345678 │ 101     │ ✏️ 🗑️ 👁️  │
│ Bob     │ MARTIN  │ 0798765432 │ 203     │ ✏️ 🗑️ 👁️  │
│ Claire  │ BERNARD │ 0611223344 │ 102     │ ✏️ 🗑️ 👁️  │
├─────────┴─────────┴────────────┴─────────┴────────────┤
│                  Affichage 1-20 sur 87                 │
│                   ← 1 2 3 ... 5 →                      │
└────────────────────────────────────────────────────────┘
```

### États d'Interface

| **État** | **Description** | **Visuel** |
|----------|----------------|-----------|
| **Loading** | Chargement de la liste | Skeleton cards (3-4 placeholders animés) |
| **Empty State** | Aucun membre en base | Illustration + CTA "Ajouter votre premier membre" |
| **Error State** | Échec de chargement | Message d'erreur + bouton "Réessayer" |
| **Success Toast** | Action réussie | Notification verte 3s : "✓ Membre ajouté" |
| **Error Toast** | Action échouée | Notification rouge 5s : "❌ Erreur : veuillez réessayer" |

---

## 5. 📊 MÉTRIQUES DE SUCCÈS (KPIs)

### Métriques Quantitatives

| **KPI** | **Objectif** | **Mesure** |
|---------|--------------|-----------|
| **Temps moyen d'ajout d'un membre** | < 30 secondes | Analytics sur temps formulaire → validation |
| **Taux d'adoption de l'import Excel** | 60% des admins l'utilisent | Ratio imports Excel / créations manuelles |
| **Erreurs lors de l'import** | < 5% de fichiers rejetés | Logs d'erreurs d'import |
| **Taux de complétion du formulaire** | > 95% | Soumissions réussies / tentatives |
| **Temps de chargement liste** | < 1 seconde | Core Web Vitals (LCP) |

### Métriques Qualitatives (User Feedback)

- **NPS (Net Promoter Score)** sur la facilité d'utilisation : Objectif ≥ 8/10
- **Feedback post-import** : "L'import Excel m'a fait gagner 2 heures" ✅
- **Signalements d'erreurs** : < 2 bugs reportés par mois

### Signals de Succès (6 mois post-lancement)

- ✅ 100% des membres du foyer sont enregistrés dans le système
- ✅ 0 utilisation de fichiers Excel externes pour gérer les membres
- ✅ Les Déléguées créent des événements en autonomie sans l'Admin
- ✅ Temps de setup d'un événement réduit de 70%

---

## 6. ⚠️ RISQUES & MITIGATIONS

### Risque #1 : Adoption faible de l'import Excel

**Probabilité :** Moyenne  
**Impact :** Moyen (onboarding plus lent)

**Causes possibles :**
- Fichier modèle pas assez explicite
- Erreurs techniques bloquantes (encodage, format)

**Mitigation :**
- ✅ Créer un tutoriel vidéo (1 min) sur l'import
- ✅ Pré-remplir le modèle avec 3 exemples concrets
- ✅ Validation en temps réel avec messages d'erreur clairs

---

### Risque #2 : Authentification passwordless défaillante

**Probabilité :** Faible  
**Impact :** Critique (blocage des membres)

**Causes possibles :**
- Service SMS non fiable (délais, non-réception)
- Problèmes de réseau mobile

**Mitigation :**
- ✅ Utiliser un provider SMS fiable (Twilio, OVH)
- ✅ Fallback : Code de secours valable 24h envoyé à l'Admin
- ✅ Logs détaillés des échecs d'envoi SMS

---

### Risque #3 : Suppression accidentelle de membres

**Probabilité :** Moyenne  
**Impact :** Élevé (perte de données)

**Causes possibles :**
- Clic accidentel sur "Supprimer"
- Pas de confirmation suffisamment claire

**Mitigation :**
- ✅ Modale de confirmation avec case à cocher "Je confirme la suppression"
- ✅ Log des suppressions dans Django Admin (audit trail)
- ✅ Soft delete (marquer comme supprimé sans effacer) en V2 si besoin récurrent

---

### Risque #4 : Performance avec 100+ membres

**Probabilité :** Faible  
**Impact :** Moyen (expérience dégradée)

**Causes possibles :**
- Requêtes SQL non optimisées
- Pagination inefficace

**Mitigation :**
- ✅ Utiliser `select_related()` et `prefetch_related()` dans les vues Django
- ✅ Tester avec un dataset de 200 membres avant prod
- ✅ Activer le cache Django pour la liste des membres

---

## 7. 📌 NOTES POUR L'ÉQUIPE TECH

### Points d'Attention Backend (Django)

🔴 **Critique :**
- **Validation du numéro de téléphone** : Utiliser une librairie (`phonenumbers`) pour valider les formats internationaux
- **Import Excel** : Gérer l'encodage UTF-8 (noms avec accents), limiter à 100 lignes/import pour éviter les timeouts
- **Passwordless SMS** : Stocker les codes avec expiration (TTL 5 min), rate limiting (3 tentatives max)

🟠 **Important :**
- **Suppression en cascade** : Vérifier que supprimer un membre ne casse pas les assignations (ajouter contrainte `on_delete=PROTECT`)
- **Permissions** : Tester rigoureusement la matrice Admin/Déléguée/Membre (unittest pour chaque endpoint)

🟢 **Nice to Have :**
- Ajouter un champ `date_joined` automatique (audit)
- Logger toutes les modifications de rôle (qui a promu qui)

---

### Points d'Attention Frontend (Vue.js + Tailwind)

🔴 **Critique :**
- **Mobile-first** : Tester sur iPhone SE (375px) et Galaxy Fold (280px)
- **Touch targets** : Boutons "Modifier" / "Supprimer" doivent faire au moins 44x44px
- **Loading states** : Afficher un skeleton pendant le fetch de la liste (éviter le flash blanc)

🟠 **Important :**
- **Validation front** : Empêcher la soumission si champs vides (pas seulement côté serveur)
- **Debounce search** : 300ms sur la barre de recherche pour éviter trop de requêtes

🟢 **Nice to Have :**
- Animation douce lors de l'ajout d'un membre (fade-in)
- Autofocus sur le champ "Prénom" à l'ouverture du formulaire

---

### Points d'Attention Design

🔴 **Critique :**
- **Accessibilité** : Labels visibles pour tous les champs (pas seulement placeholder)
- **Contraste** : Respecter WCAG AA (4.5:1 minimum pour les textes)

🟠 **Important :**
- **Feedback visuel** : Toast de confirmation doit être visible mais non bloquant
- **Hiérarchie** : Bouton "Ajouter" doit être plus visible que "Importer"

---

## 8. 📅 TIMELINE ESTIMÉE (Développement)

| **Phase** | **Durée** | **Livrables** |
|-----------|-----------|---------------|
| **Setup & Models** | 2 jours | Models Member créé + migrations |
| **CRUD Views** | 3 jours | Vues Liste, Détail, Ajout, Modif, Suppression |
| **Import Excel** | 2 jours | Feature d'import avec validation |
| **Passwordless Auth** | 3 jours | Intégration SMS + login |
| **Frontend UI** | 4 jours | Templates + Vue.js + Tailwind |
| **Tests & Bug Fixes** | 2 jours | Tests unitaires + corrections |
| **Total** | **16 jours** (~3 semaines) |

---

## ✅ CHECKLIST DE VALIDATION

Avant de passer en production, vérifier :

- [ ] Tous les critères d'acceptation des User Stories sont validés
- [ ] Tests unitaires passent à 100%
- [ ] Import Excel testé avec 50+ membres réels
- [ ] Passwordless fonctionne sur 3 opérateurs téléphoniques différents
- [ ] Interface testée sur mobile (iOS + Android)
- [ ] Performance : Liste de 100 membres charge en < 1s
- [ ] Audit de sécurité : Permissions testées pour chaque rôle
- [ ] Documentation Admin rédigée (comment gérer les membres)

---

## 🎉 CONCLUSION

Ce PRD définit la **Gestion des Membres** comme la pierre angulaire du Gestionnaire de Foyer. Une fois cette fonctionnalité solide, elle servira de base pour les modules **Événements** et **Commissions**.

**Prochaines étapes suggérées :**
1. Review de ce PRD avec l'équipe Dev + Design
2. Estimation détaillée (story points)
3. Kick-off Sprint avec démo de la maquette mobile

---

**Questions ou ajustements nécessaires ?** 🚀  
Si ce PRD est validé, nous pouvons passer au suivant : **Gestion des Événements** ! 🎯
