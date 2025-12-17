# 📋 PRD — AMÉLIORATIONS UX/UI & FEATURES V1.5

**Produit :** Gestionnaire de Foyer pour Jeunes Filles  
**Features :** Package Amélioration Post-MVP  
**Version :** 1.5 (Post-MVP)  
**Date :** Décembre 2024  
**Owner :** Product Architect

---

## 1. 📖 CONTEXTE & PROBLÈME

### Background
Le MVP (v1.0) du Gestionnaire de Foyer est fonctionnel avec les modules core :
- ✅ Gestion des membres
- ✅ Authentification multi-méthodes
- ✅ Gestion des événements
- ✅ Attribution des commissions

Cependant, après les premiers retours utilisateurs, **5 pain points majeurs** ont été identifiés :

### Problèmes Actuels

#### 1. **UX/UI Basique**
- 😤 Date picker natif HTML peu ergonomique sur mobile
- 🤷 Dropdowns standards peu intuitifs avec 50+ membres
- 📝 Champ texte simple pour descriptions (pas de formatting)
- 📤 Upload Excel sans drag & drop
- **Impact :** Interface perçue comme "trop basique" vs apps modernes

#### 2. **Pas de Page Profil**
- 😤 Impossible pour les membres de voir leurs propres infos
- 🔐 Changement de password via process complexe
- 📊 Aucune visibilité sur mes statistiques de participation
- 📸 Pas de personnalisation (photo)
- **Impact :** Sentiment d'impersonnalité, manque d'engagement

#### 3. **Visibilité Limitée des Commissions**
- 😤 Membres simples ne voient QUE leur propre commission
- 🤷 Impossible de savoir qui fait quoi dans les autres commissions
- 👥 Pas de vue d'ensemble de l'organisation d'un événement
- **Impact :** Manque de transparence, sentiment d'exclusion

#### 4. **Absence de Notifications**
- 😤 Membres ne savent pas qu'elles ont été assignées
- 📧 Admin doit envoyer manuellement des messages WhatsApp/SMS
- ⏰ Pas d'alerte pour événements à venir
- **Impact :** Communication manuelle chronophage, oublis fréquents

#### 5. **Suppression Définitive Risquée**
- 😤 Supprimer un membre = perte irréversible de données
- 🗑️ Pas de moyen de gérer les départs temporaires (congés, absence longue)
- 📊 Historique perdu si suppression accidentelle
- **Impact :** Stress lors des suppressions, erreurs irréversibles

### Pourquoi maintenant ?
Ces 5 améliorations sont **bloquantes pour l'adoption à grande échelle** :
- Sans notifications, la charge admin reste élevée
- Sans profil, pas d'engagement individuel
- Sans soft delete, risque de perte de données critique

### Impact Business Attendu
- **+50% d'engagement** : Profil personnalisé + stats visibles
- **-70% de charge admin** : Notifications automatiques
- **+40% de transparence** : Visibilité complète des commissions
- **0 perte de données** : Archivage au lieu de suppression

---

## 2. 🎯 OBJECTIFS & NON-OBJECTIFS

### ✅ Objectifs (Ce qu'on fait)

1. **Moderniser l'interface avec des composants externes**  
   Intégrer des packages UI modernes pour améliorer drastiquement l'UX

2. **Créer la page "Mon Profil"**  
   Permettre à chaque utilisatrice de gérer ses informations et voir ses statistiques

3. **Ouvrir la visibilité des commissions**  
   Membres simples peuvent consulter toutes les commissions (lecture seule)

4. **Implémenter un système de notifications internes**  
   Centre de notifications avec badge, dropdown et historique 60 jours

5. **Activer le soft delete (archivage)**  
   Archiver au lieu de supprimer définitivement les membres

### ❌ Non-Objectifs (Ce qu'on ne fait PAS dans cette version)

- ❌ Notifications push mobile (PWA notifications en V2)
- ❌ Notifications SMS/Email externes (hors scope)
- ❌ Personnalisation avancée du profil (bio, centres d'intérêt)
- ❌ Système de chat/messagerie interne
- ❌ Modification des commissions par les membres simples
- ❌ Soft delete pour événements et commissions (seulement membres)
- ❌ Thème clair/sombre personnalisable
- ❌ Gamification (badges, points)

---

## 3. 👥 USER STORIES & CRITÈRES D'ACCEPTATION

# PARTIE A : AMÉLIORATION DESIGN & PACKAGES EXTERNES

## 🔹 US-D01 : Date Picker Moderne

**En tant qu'** Admin ou Déléguée  
**Je veux** un sélecteur de date intuitif et tactile  
**Afin de** créer/modifier des événements rapidement sur mobile

### Critères d'Acceptation

```gherkin
GIVEN je crée un événement
AND je clique sur le champ "Date de l'événement"
WHEN le date picker s'affiche
THEN je vois un calendrier visuel moderne avec :
  - Mois/Année navigable avec flèches
  - Dates cliquables (44px min touch target)
  - Date du jour mise en évidence
  - Possibilité de saisir manuellement (format JJ/MM/AAAA)

GIVEN je suis sur mobile
WHEN le date picker s'ouvre
THEN il occupe tout l'écran (fullscreen)
AND je vois les boutons "Annuler" | "Valider"

GIVEN je sélectionne "25 décembre 2024"
WHEN je valide
THEN la date s'affiche dans le champ : "25/12/2024"
AND le picker se ferme automatiquement

GIVEN le champ date est optionnel
WHEN je valide sans sélectionner de date
THEN le formulaire est accepté (pas d'erreur)
```

**Package recommandé :** Flatpickr (léger, mobile-friendly, i18n)

---

## 🔹 US-D02 : Time Picker pour Heure des Événements

**En tant qu'** Admin ou Déléguée  
**Je veux** définir une heure précise pour un événement  
**Afin de** communiquer l'horaire exact aux membres

### Critères d'Acceptation

```gherkin
GIVEN je crée/modifie un événement
AND je clique sur le champ "Heure de début"
WHEN le time picker s'affiche
THEN je vois :
  - Sélecteur d'heures (00-23)
  - Sélecteur de minutes (00, 15, 30, 45)
  - Format 24h
  - Bouton "Maintenant" (raccourci)

GIVEN je sélectionne "19:30"
WHEN je valide
THEN le champ affiche "19h30"

GIVEN le champ heure est optionnel
WHEN je laisse vide
THEN seule la date s'affiche (ex: "25 décembre 2024" sans heure)
```

**Package recommandé :** Flatpickr avec option `enableTime: true`

---

## 🔹 US-D03 : Select Amélioré pour Sélection Multiple

**En tant qu'** Admin ou Déléguée  
**Je veux** sélectionner plusieurs membres facilement  
**Afin de** constituer rapidement des listes (attribution, import)

### Critères d'Acceptation

```gherkin
GIVEN je suis sur l'interface d'attribution automatique
AND je dois sélectionner les membres disponibles
WHEN j'ouvre le select multiple
THEN je vois :
  - Barre de recherche en haut
  - Liste des 42 membres avec checkbox
  - Bouton "Tout sélectionner" / "Tout désélectionner"
  - Compteur : "15 sélectionnés"
  - Scroll infini si >20 membres

GIVEN je tape "Dup" dans la recherche
WHEN je valide
THEN seuls "Alice DUPONT" et "Bob DUPONT" s'affichent
AND les autres sont masqués mais restent sélectionnés si déjà cochés

GIVEN je sélectionne 5 membres
WHEN je ferme le dropdown
THEN je vois 5 "pills" avec les prénoms : [Alice ×] [Bob ×] [Claire ×]...
AND je peux cliquer sur × pour retirer un membre

GIVEN le select est utilisé pour "Responsable de commission" (choix unique)
WHEN j'ouvre le dropdown
THEN je vois une liste simple sans checkbox (radio buttons)
AND la recherche fonctionne de la même manière
```

**Package recommandé :** Choices.js (léger, accessible, customisable)

---

## 🔹 US-D04 : Rich Text Editor pour Descriptions

**En tant qu'** Admin ou Déléguée  
**Je veux** formater les descriptions d'événements/commissions  
**Afin de** rendre les informations plus claires et structurées

### Critères d'Acceptation

```gherkin
GIVEN je crée un événement
AND je clique dans le champ "Description"
WHEN l'éditeur s'affiche
THEN je vois une toolbar avec :
  - Gras | Italique | Souligné
  - Liste à puces | Liste numérotée
  - Lien hypertexte
  - Pas d'options avancées (pas d'images, pas de couleurs)

GIVEN je tape du texte et applique du gras
WHEN je soumets le formulaire
THEN le HTML généré est sécurisé (sanitized)
AND seules les balises autorisées sont conservées : <b>, <i>, <u>, <ul>, <ol>, <li>, <a>

GIVEN je consulte la description depuis mon profil Membre
WHEN j'affiche la description
THEN le formatting est préservé (gras, listes, liens cliquables)

GIVEN je suis sur mobile
WHEN j'utilise l'éditeur
THEN la toolbar est responsive (icônes empilées si nécessaire)
```

**Package recommandé :** Quill (léger, moderne, customisable)

---

## 🔹 US-D05 : File Uploader avec Drag & Drop

**En tant qu'** Admin  
**Je veux** glisser-déposer un fichier Excel pour l'import  
**Afin de** simplifier le processus d'import en masse

### Critères d'Acceptation

```gherkin
GIVEN je suis sur la page "Importer des membres"
WHEN j'affiche la zone d'upload
THEN je vois :
  - Zone en pointillés "Glissez votre fichier ici"
  - Icône 📁 au centre
  - Texte : "ou cliquez pour parcourir"
  - Formats acceptés : .xlsx, .xls (affichés en gris)

GIVEN je glisse un fichier "membres.xlsx" dans la zone
WHEN je relâche le fichier
THEN la zone change de couleur (bleu)
AND je vois : "membres.xlsx (125 KB) - Prêt à importer"
AND je vois un bouton "× Retirer"

GIVEN je glisse un fichier .pdf (format non supporté)
WHEN je relâche
THEN la zone devient rouge
AND un message s'affiche : "⚠️ Format non supporté. Seuls .xlsx et .xls sont acceptés"

GIVEN je clique sur la zone (au lieu de glisser)
WHEN l'explorateur de fichiers s'ouvre
THEN je peux sélectionner un fichier .xlsx
AND le comportement est identique au drag & drop
```

**Package recommandé :** Dropzone.js (simple, léger)

---

## 🔹 US-D06 : Toasts pour Feedback Utilisateur

**En tant qu'** n'importe quelle utilisatrice  
**Je veux** des notifications visuelles pour mes actions  
**Afin de** savoir immédiatement si mon action a réussi ou échoué

### Critères d'Acceptation

```gherkin
GIVEN je crée un membre avec succès
WHEN la création est confirmée
THEN un toast vert apparaît en haut à droite :
  "✓ Membre créé avec succès"
AND il disparaît automatiquement après 3 secondes
AND je peux cliquer sur × pour le fermer manuellement

GIVEN j'essaie de créer un membre avec un champ manquant
WHEN l'erreur est retournée
THEN un toast rouge apparaît :
  "❌ Erreur : Le numéro de téléphone est obligatoire"
AND il reste visible 5 secondes (erreurs = plus long)

GIVEN je suis sur mobile
WHEN un toast apparaît
THEN il s'affiche en pleine largeur en haut de l'écran
AND il ne masque pas le contenu important

GIVEN 3 toasts s'affichent simultanément
WHEN ils apparaissent
THEN ils s'empilent verticalement (max 3 visibles)
AND les plus anciens disparaissent en premier
```

**Package recommandé :** Toastify.js (léger, customisable)

---

# PARTIE B : PAGE "MON PROFIL"

## 🔹 US-P01 : Accéder à ma page profil

**En tant que** n'importe quelle utilisatrice  
**Je veux** accéder à ma page profil  
**Afin de** consulter et modifier mes informations personnelles

### Critères d'Acceptation

```gherkin
GIVEN je suis connectée
WHEN je clique sur l'icône profil (👤) dans la navbar
THEN un dropdown s'affiche avec :
  - "Mon profil"
  - "Se déconnecter"

GIVEN je clique sur "Mon profil"
WHEN la page se charge
THEN je vois ma page profil avec 4 sections :
  1. Informations personnelles
  2. Sécurité
  3. Photo de profil
  4. Mes statistiques

GIVEN je suis sur mobile
WHEN j'affiche la page profil
THEN les sections sont empilées verticalement
AND chaque section est un accordéon déplié par défaut
```

---

## 🔹 US-P02 : Section Informations Personnelles

**En tant que** Membre  
**Je veux** voir et modifier mes informations personnelles  
**Afin de** maintenir mes données à jour

### Critères d'Acceptation

```gherkin
GIVEN je consulte la section "Informations personnelles"
WHEN la section s'affiche
THEN je vois un formulaire avec mes données actuelles :
  - Prénom (pré-rempli)
  - Nom (pré-rempli)
  - Numéro de téléphone (pré-rempli)
  - Chambre (pré-rempli)
  - Bouton "Enregistrer les modifications"

GIVEN je modifie mon numéro de téléphone de "0612345678" à "0698765432"
WHEN je clique sur "Enregistrer"
THEN mes modifications sont sauvegardées
AND un toast vert s'affiche : "✓ Informations mises à jour"

GIVEN je suis Admin et je consulte le profil d'un autre membre
WHEN j'accède à la page profil de "Alice DUPONT"
THEN je vois les mêmes informations
AND je peux également modifier son rôle (Admin/Déléguée/Membre)
AND je vois un bouton supplémentaire "Archiver ce membre"

GIVEN je suis une Membre simple
WHEN je consulte mon propre profil
THEN je ne vois PAS l'option "Rôle" (non modifiable par moi)
```

---

## 🔹 US-P03 : Section Sécurité (Password & Code PIN)

**En tant que** n'importe quelle utilisatrice  
**Je veux** gérer mes identifiants de connexion  
**Afin de** sécuriser mon compte et utiliser la connexion rapide

### Critères d'Acceptation

```gherkin
GIVEN je consulte la section "Sécurité"
WHEN la section s'affiche
THEN je vois deux sous-sections :
  1. Changer mon password
  2. Gérer mon code PIN

# Sous-section 1 : Changer Password
GIVEN je clique sur "Changer mon password"
WHEN le formulaire s'affiche
THEN je vois 3 champs :
  - Password actuel (masqué)
  - Nouveau password (masqué, min 8 car)
  - Confirmer nouveau password (masqué)
  - Bouton "Modifier le password"

GIVEN je saisis mon password actuel correct
AND je saisis un nouveau password valide "MonNouveauPass123!"
AND je confirme ce password
WHEN je soumets
THEN mon password est mis à jour
AND un toast s'affiche : "✓ Password modifié avec succès"
AND je suis déconnectée automatiquement
AND je dois me reconnecter avec le nouveau password

GIVEN je saisis un password actuel incorrect
WHEN je tente de soumettre
THEN un message d'erreur s'affiche : "Password actuel incorrect"

# Sous-section 2 : Gérer Code PIN
GIVEN je n'ai pas encore de code PIN défini
WHEN j'affiche cette section
THEN je vois :
  - "Code PIN : Non défini"
  - Bouton "Définir un code PIN"

GIVEN je clique sur "Définir un code PIN"
WHEN le formulaire s'affiche
THEN je vois :
  - Champ "Nouveau code PIN" (6 chiffres, masqué)
  - Champ "Confirmer code PIN" (6 chiffres, masqué)
  - Champ "Password actuel" (pour validation)
  - Bouton "Activer le code PIN"

GIVEN j'ai déjà un code PIN actif
WHEN j'affiche cette section
THEN je vois :
  - "Code PIN : Actif ******"
  - Bouton "Modifier le code PIN"
  - Bouton "Supprimer le code PIN"
```

---

## 🔹 US-P04 : Section Photo de Profil

**En tant que** n'importe quelle utilisatrice  
**Je veux** ajouter/modifier ma photo de profil  
**Afin de** personnaliser mon compte

### Critères d'Acceptation

```gherkin
GIVEN je consulte la section "Photo de profil"
AND je n'ai pas encore de photo
WHEN la section s'affiche
THEN je vois :
  - Avatar par défaut (initiales : "AD" pour Alice Dupont)
  - Bouton "Ajouter une photo"

GIVEN je clique sur "Ajouter une photo"
WHEN l'uploader s'affiche
THEN je peux :
  - Glisser-déposer une image
  - Cliquer pour parcourir
  - Formats acceptés : .jpg, .jpeg, .png (max 5 MB)

GIVEN je téléverse une photo "profil.jpg"
WHEN l'upload réussit
THEN je vois un aperçu de ma photo (crop circulaire)
AND je vois deux options :
  - "Enregistrer"
  - "Changer de photo"

GIVEN ma photo fait 8 MB (trop lourde)
WHEN je tente de l'uploader
THEN un message d'erreur s'affiche :
  "⚠️ Fichier trop lourd. Maximum 5 MB"

GIVEN j'ai déjà une photo
WHEN j'affiche cette section
THEN je vois :
  - Ma photo actuelle
  - Bouton "Modifier la photo"
  - Bouton "Supprimer la photo"

GIVEN je clique sur "Supprimer la photo"
WHEN je confirme
THEN ma photo est supprimée
AND l'avatar par défaut (initiales) réapparaît
```

---

## 🔹 US-P05 : Section Mes Statistiques

**En tant que** n'importe quelle utilisatrice  
**Je veux** voir mes statistiques de participation  
**Afin de** suivre mon engagement au foyer

### Critères d'Acceptation

```gherkin
GIVEN je consulte la section "Mes statistiques"
WHEN la section s'affiche
THEN je vois 4 cartes métriques :

┌─────────────────────────┐
│ 📅 ÉVÉNEMENTS           │
│ 12                      │
│ participations          │
└─────────────────────────┘

┌─────────────────────────┐
│ 📋 COMMISSIONS          │
│ 8 commissions différentes│
└─────────────────────────┘

┌─────────────────────────┐
│ 👑 RESPONSABILITÉS      │
│ 3 fois responsable      │
└─────────────────────────┘

┌─────────────────────────┐
│ 🎯 DERNIÈRE PARTICIPATION│
│ Soirée de Noël          │
│ il y a 5 jours          │
└─────────────────────────┘

GIVEN je n'ai jamais participé à aucun événement
WHEN j'affiche mes statistiques
THEN toutes les cartes affichent "0" ou "Aucune participation"
AND un message s'affiche : "Vous serez bientôt assignée à votre première commission !"

GIVEN je suis Admin et je consulte le profil d'Alice
WHEN j'affiche ses statistiques
THEN je vois les mêmes métriques pour Alice
```

---

# PARTIE C : DÉTAILS DES COMMISSIONS (VISIBILITÉ MEMBRES)

## 🔹 US-V01 : Voir toutes les commissions d'un événement (Membre)

**En tant que** Membre simple  
**Je veux** voir toutes les commissions d'un événement  
**Afin de** savoir qui fait quoi et comment l'événement est organisé

### Critères d'Acceptation

```gherkin
GIVEN je suis une Membre simple connectée
AND je consulte l'événement "Soirée de Noël"
WHEN j'affiche la page détail de l'événement
THEN je vois :
  - Titre, date, lieu, description (comme avant)
  - Section "Commissions (3)" (NOUVEAU)
  - Liste des 3 commissions avec aperçu :
    • Décoration (5/8 membres)
    • Cuisine (6/6 membres)
    • Animation (4/5 membres)

GIVEN je clique sur "Décoration"
WHEN la page détail de la commission s'affiche
THEN je vois :
  - Nom de la commission
  - Description (si renseignée)
  - Responsable : Alice DUPONT (si défini)
  - Liste complète des 5 membres assignés :
    ✓ Alice DUPONT (Ch. 101)
    ✓ Bob MARTIN (Ch. 203)
    ✓ Claire BERNARD (Ch. 102)
    ✓ David LEROY (Ch. 104)
    ✓ Emma PETIT (Ch. 205)

GIVEN je suis une Membre simple
WHEN je consulte le détail d'une commission
THEN je ne vois AUCUN bouton d'action :
  - Pas de "Modifier"
  - Pas de "Supprimer"
  - Pas de "Ajouter un membre"
  - Tout est en lecture seule

GIVEN je suis Admin ou Déléguée
WHEN je consulte le détail d'une commission
THEN je vois en plus les boutons d'action :
  - "Modifier la commission"
  - "Gérer les membres"
  - "Supprimer la commission"
```

---

## 🔹 US-V02 : Vue d'ensemble des commissions (Tableau récap)

**En tant que** Membre simple  
**Je veux** une vue d'ensemble de toutes les commissions  
**Afin de** voir rapidement l'organisation complète

### Critères d'Acceptation

```gherkin
GIVEN je suis sur la page "Soirée de Noël"
AND je clique sur l'onglet "Commissions"
WHEN le tableau s'affiche
THEN je vois un tableau récapitulatif :

┌────────────────────────────────────────────────┐
│ COMMISSION    │ MEMBRES  │ RESPONSABLE       │
├────────────────────────────────────────────────┤
│ Décoration    │ 5/8      │ Alice DUPONT      │
│ Cuisine       │ 6/6      │ Non défini        │
│ Animation     │ 4/5      │ David LEROY       │
└────────────────────────────────────────────────┘

GIVEN je clique sur une ligne du tableau
WHEN l'action s'exécute
THEN je suis redirigée vers la page détail de cette commission
```

---

# PARTIE D : SYSTÈME DE NOTIFICATIONS INTERNES

## 🔹 US-N01 : Badge de notifications non lues

**En tant que** n'importe quelle utilisatrice  
**Je veux** voir en un coup d'œil si j'ai des notifications  
**Afin de** ne rien manquer d'important

### Critères d'Acceptation

```gherkin
GIVEN j'ai 3 notifications non lues
WHEN j'affiche la navbar
THEN je vois une icône 🔔 avec un badge rouge "3"

GIVEN je clique sur l'icône 🔔
WHEN le dropdown s'affiche
THEN je vois :
  - En-tête "Notifications (3 non lues)"
  - Liste des 5 dernières notifications
  - Bouton "Tout marquer comme lu"
  - Lien "Voir toutes les notifications"

GIVEN je n'ai aucune notification non lue
WHEN j'affiche la navbar
THEN l'icône 🔔 est visible mais SANS badge
```

---

## 🔹 US-N02 : Types de notifications

**En tant que** n'importe quelle utilisatrice  
**Je veux** recevoir différents types de notifications  
**Afin de** être informée de tout ce qui me concerne

### Critères d'Acceptation

```gherkin
# Type 1 : Attribution à une commission
GIVEN je suis assignée à la commission "Décoration"
WHEN l'attribution est finalisée
THEN je reçois une notification :
  Type : Attribution
  Icône : 📋
  Titre : "Nouvelle commission !"
  Message : "Vous avez été assignée à la commission Décoration pour l'événement Soirée de Noël"
  Date : "Il y a 2 minutes"
  Status : Non lu (pastille bleue)

# Type 2 : Événement créé
GIVEN un Admin crée un événement "Atelier peinture"
WHEN l'événement est publié
THEN toutes les membres reçoivent une notification :
  Type : Événement
  Icône : 📅
  Titre : "Nouvel événement !"
  Message : "Atelier peinture - 15 janvier 2025"

# Type 3 : Événement modifié
GIVEN l'événement "Soirée de Noël" est modifié (date changée)
WHEN la modification est enregistrée
THEN toutes les membres assignées à cet événement reçoivent :
  Type : Modification
  Icône : ✏️
  Titre : "Événement modifié"
  Message : "Soirée de Noël : La date a été modifiée au 20 décembre"

# Type 4 : Changement de commission
GIVEN je suis dans "Décoration"
AND un Admin me déplace vers "Cuisine"
WHEN le déplacement est effectué
THEN je reçois :
  Type : Modification
  Icône : 🔄
  Titre : "Commission modifiée"
  Message : "Vous avez été déplacée de Décoration vers Cuisine"

# Type 5 : Message système Admin
GIVEN un Admin envoie un message global
WHEN le message est publié
THEN toutes les membres reçoivent :
  Type : Système
  Icône : 📢
  Titre : "Message important"
  Message : "[Texte du message]"
```

---

## 🔹 US-N03 : Dropdown des notifications

**En tant que** n'importe quelle utilisatrice  
**Je veux** consulter mes notifications récentes sans quitter ma page  
**Afin de** rester informée tout en naviguant

### Critères d'Acceptation

```gherkin
GIVEN je clique sur l'icône 🔔
WHEN le dropdown s'affiche
THEN je vois :
  - Titre "Notifications (3 non lues)"
  - Liste des 5 dernières notifications triées par date (plus récente en haut)
  - Chaque notification affiche :
    • Icône (selon type)
    • Titre (gras si non lu)
    • Message (tronqué à 50 caractères)
    • Date relative ("Il y a 2 heures")
    • Pastille bleue si non lu

GIVEN je clique sur une notification
WHEN l'action s'exécute
THEN :
  - La notification est marquée comme lue automatiquement
  - Je suis redirigée vers la page concernée (événement ou commission)
  - Le dropdown se ferme

GIVEN je clique sur "Tout marquer comme lu"
WHEN l'action s'exécute
THEN toutes les notifications deviennent lues
AND le badge disparaît de l'icône 🔔
AND un toast s'affiche : "✓ Toutes les notifications marquées comme lues"
```

---

## 🔹 US-N04 : Page dédiée "Mes Notifications"

**En tant que** n'importe quelle utilisatrice  
**Je veux** accéder à l'historique complet de mes notifications  
**Afin de** retrouver une notification ancienne ou consulter plus de détails

### Critères d'Acceptation

```gherkin
GIVEN je clique sur "Voir toutes les notifications" dans le dropdown
WHEN la page se charge
THEN je vois :
  - Titre "Mes Notifications"
  - Filtre : [Toutes] [Non lues] [Attribution] [Événements] [Système]
  - Liste paginée (20 par page) de toutes mes notifications (60 jours max)

GIVEN je sélectionne le filtre "Non lues"
WHEN le filtre s'applique
THEN seules les notifications non lues s'affichent

GIVEN je clique sur une notification dans la liste
WHEN je consulte ses détails
THEN je vois :
  - Titre complet
  - Message complet (non tronqué)
  - Date complète (JJ/MM/AAAA à HH:MM)
  - Bouton "Marquer comme lu/non lu"
  - Bouton "Supprimer"
  - Lien vers la page concernée (si applicable)

GIVEN je clique sur "Supprimer"
WHEN je confirme
THEN la notification est supprimée de mon historique
AND elle disparaît immédiatement de la liste
```

---

## 🔹 US-N05 : Gestion des notifications (Marquer lu/non lu, Supprimer)

**En tant que** n'importe quelle utilisatrice  
**Je veux** gérer mes notifications  
**Afin de** garder mon centre de notifications organisé

### Critères d'Acceptation

```gherkin
GIVEN je consulte une notification non lue
WHEN je clique dessus (dropdown ou page)
THEN elle passe automatiquement en "Lu"
AND la pastille bleue disparaît

GIVEN je veux marquer une notification lue comme "Non lue"
WHEN je clique sur l'icône "Marquer comme non lu"
THEN la notification redevient non lue
AND une pastille bleue réapparaît

GIVEN je clique sur "Supprimer" sur une notification
WHEN je confirme
THEN la notification est supprimée définitivement
AND elle disparaît de mon historique

GIVEN je ne fais aucune action pendant 60 jours
WHEN le système nettoie automatiquement
THEN les notifications de plus de 60 jours sont supprimées automatiquement
```

---

## 🔹 US-N06 : Notifications en temps réel (Polling)

**En tant que** n'importe quelle utilisatrice  
**Je veux** recevoir les notifications sans recharger la page  
**Afin de** être informée immédiatement

### Critères d'Acceptation

```gherkin
GIVEN je suis sur la page d'accueil depuis 2 minutes
AND un Admin m'assigne à une commission
WHEN l'attribution est finalisée
THEN après 30 secondes max :
  - Le badge 🔔 se met à jour (1 notification)
  - Un toast bleu s'affiche : "🔔 Nouvelle notification"
  - Je peux cliquer sur le toast pour voir la notification

GIVEN je suis connectée
WHEN le système vérifie les nouvelles notifications
THEN il effectue un polling toutes les 30 secondes
AND ne charge que les notifications depuis ma dernière vérification
```

**Note technique :** Utiliser polling HTTP toutes les 30s (pas de WebSocket pour MVP)

---

# PARTIE E : SOFT DELETE (ARCHIVAGE)

## 🔹 US-A01 : Archiver un membre

**En tant qu'** Admin  
**Je veux** archiver un membre au lieu de le supprimer  
**Afin de** conserver l'historique et pouvoir le restaurer si besoin

### Critères d'Acceptation

```gherkin
GIVEN je consulte la fiche d'Alice DUPONT
AND je suis Admin
WHEN je clique sur le bouton "Actions" puis "Archiver"
THEN une modale de confirmation s'affiche :
  "⚠️ Archiver Alice DUPONT ?
  Le membre ne sera plus visible dans la liste active
  mais son historique sera conservé.
  Vous pourrez le restaurer à tout moment."
  [Annuler] [Archiver]

GIVEN je confirme l'archivage
WHEN l'action s'exécute
THEN :
  - Alice passe en statut "Archivé" (is_active = False)
  - Elle disparaît de la liste des membres actifs
  - Son compte utilisateur est désactivé (ne peut plus se connecter)
  - Son historique de participations est conservé
  - Un toast s'affiche : "✓ Alice DUPONT archivée"

GIVEN Alice est assignée à 2 commissions actives
WHEN je tente de l'archiver
THEN un warning s'affiche :
  "⚠️ Alice est actuellement assignée à 2 commissions :
  - Décoration (Soirée de Noël)
  - Cuisine (Atelier peinture)
  
  Elle sera automatiquement retirée de ces commissions.
  Continuer ?"
  [Annuler] [Archiver quand même]

GIVEN je suis Déléguée
WHEN j'essaie d'archiver un membre
THEN je vois le bouton "Archiver" grisé
AND un tooltip s'affiche : "Réservé aux Admin"
```

---

## 🔹 US-A02 : Consulter les membres archivés

**En tant qu'** Admin  
**Je veux** voir la liste des membres archivés  
**Afin de** retrouver un membre et potentiellement le restaurer

### Critères d'Acceptation

```gherkin
GIVEN je suis sur la page "Membres"
WHEN j'affiche les onglets
THEN je vois deux onglets :
  - "Actifs (42)" [par défaut]
  - "Archivés (5)"

GIVEN je clique sur l'onglet "Archivés"
WHEN la liste s'affiche
THEN je vois les 5 membres archivés avec :
  - Prénom | Nom | Chambre | Date d'archivage | Actions
  - Badge gris "Archivé" sur chaque ligne

GIVEN je recherche "Dupont" dans la barre de recherche
WHEN je suis sur l'onglet "Actifs"
THEN seuls les membres actifs nommés Dupont s'affichent
AND les membres archivés ne sont PAS inclus dans la recherche

GIVEN je veux chercher dans les archivés aussi
WHEN je coche "Inclure les archivés"
THEN la recherche inclut les deux listes
```

---

## 🔹 US-A03 : Restaurer un membre archivé

**En tant qu'** Admin  
**Je veux** restaurer un membre archivé  
**Afin de** le réactiver après un retour (congés, absence longue)

### Critères d'Acceptation

```gherkin
GIVEN je suis sur l'onglet "Archivés"
AND je consulte la ligne d'Alice DUPONT
WHEN je clique sur "Restaurer"
THEN une modale de confirmation s'affiche :
  "Restaurer Alice DUPONT ?
  Elle redeviendra active et pourra se reconnecter.
  Ses anciennes participations seront toujours visibles."
  [Annuler] [Restaurer]

GIVEN je confirme la restauration
WHEN l'action s'exécute
THEN :
  - Alice passe en statut "Actif" (is_active = True)
  - Elle réapparaît dans la liste des membres actifs
  - Son compte utilisateur est réactivé
  - Elle peut se reconnecter avec ses anciens identifiants
  - Un toast s'affiche : "✓ Alice DUPONT restaurée"

GIVEN Alice avait un historique de 12 participations avant archivage
WHEN elle est restaurée
THEN son historique est toujours intact
AND ses statistiques affichent toujours "12 participations"
```

---

## 🔹 US-A04 : Suppression définitive (Admin uniquement)

**En tant qu'** Admin  
**Je veux** supprimer définitivement un membre archivé  
**Afin de** nettoyer la base de données (cas extrêmes)

### Critères d'Acceptation

```gherkin
GIVEN je suis sur l'onglet "Archivés"
AND je consulte Alice DUPONT (archivée depuis 6 mois)
WHEN je clique sur "..." puis "Supprimer définitivement"
THEN une modale TRÈS explicite s'affiche :
  "🚨 ATTENTION : SUPPRESSION DÉFINITIVE
  
  Cette action est IRRÉVERSIBLE.
  Alice DUPONT sera supprimée de la base de données :
  - Son compte utilisateur
  - Ses informations personnelles
  - Son historique de participations
  
  Êtes-vous absolument certain(e) ?
  Pour confirmer, tapez : SUPPRIMER"
  
  [Champ texte]
  [Annuler] [Supprimer définitivement]

GIVEN je tape "SUPPRIMER" dans le champ
AND je clique sur "Supprimer définitivement"
WHEN l'action s'exécute
THEN :
  - Alice est supprimée définitivement
  - Toutes ses données sont effacées
  - Son historique disparaît (mais les événements/commissions restent)
  - Un toast rouge s'affiche : "Alice DUPONT supprimée définitivement"

GIVEN je tape autre chose que "SUPPRIMER"
WHEN je tente de valider
THEN le bouton "Supprimer définitivement" reste grisé
AND je dois taper exactement "SUPPRIMER" pour activer le bouton
```

---

## 🔹 US-A05 : Historique conservé même après archivage

**En tant qu'** Admin  
**Je veux** que l'historique des participations soit conservé même après archivage  
**Afin de** maintenir la cohérence des données événements/commissions

### Critères d'Acceptation

```gherkin
GIVEN Alice a participé à 12 événements
AND elle est dans la commission "Décoration" de "Soirée de Noël"
WHEN je l'archive
THEN :
  - Son profil indique toujours "12 participations" (si je consulte les archivés)
  - L'événement "Soirée de Noël" affiche toujours son nom dans la commission Décoration
  - BUT avec un badge gris "(Archivée)" à côté de son nom

GIVEN je consulte l'événement "Soirée de Noël" (événement passé)
AND Alice y avait participé avant d'être archivée
WHEN je consulte la commission Décoration
THEN je vois toujours "Alice DUPONT (Archivée)" dans la liste
AND son nom est grisé pour indiquer qu'elle n'est plus active

GIVEN je veux attribuer des membres à un nouvel événement
WHEN j'ouvre la liste de sélection
THEN Alice N'apparaît PAS (elle est archivée)
AND seuls les membres actifs sont sélectionnables
```

---

## 4. 🎨 UX/UI REQUIREMENTS

### Wireframe Mobile : Page "Mon Profil"

```
┌─────────────────────────┐
│  ⬅️ MON PROFIL          │
├─────────────────────────┤
│                         │
│    ┌───────────┐        │
│    │  [Photo]  │        │
│    │   Alice   │        │
│    └───────────┘        │
│                         │
│  Alice DUPONT           │
│  Déléguée               │
│                         │
├─────────────────────────┤
│ ▼ INFOS PERSONNELLES    │
│   Prénom : [Alice    ]  │
│   Nom : [DUPONT      ]  │
│   Téléphone : [06...]   │
│   Chambre : [101     ]  │
│   [Enregistrer]         │
├─────────────────────────┤
│ ▼ SÉCURITÉ              │
│   🔒 Changer password   │
│   🔢 Gérer code PIN     │
├─────────────────────────┤
│ ▼ PHOTO DE PROFIL       │
│   [Modifier photo]      │
├─────────────────────────┤
│ ▼ MES STATISTIQUES      │
│   ┌─────┐ ┌─────┐       │
│   │ 12  │ │  8  │       │
│   │Évén.│ │Comm.│       │
│   └─────┘ └─────┘       │
└─────────────────────────┘
```

---

### Wireframe Desktop : Centre de Notifications

```
┌──────────────────────────────────────────────────┐
│  Gestionnaire de Foyer              🔔 3    [👤▼]│
├──────────────────────────────────────────────────┤
│                                                  │
│  [Dropdown 🔔 ouvert]                            │
│  ┌────────────────────────────────────────┐     │
│  │ Notifications (3 non lues)             │     │
│  │ [Tout marquer comme lu]                │     │
│  ├────────────────────────────────────────┤     │
│  │ ● 📋 Nouvelle commission !             │     │
│  │   Décoration - Soirée de Noël          │     │
│  │   Il y a 2 heures                      │     │
│  ├────────────────────────────────────────┤     │
│  │ ● 📅 Nouvel événement !                │     │
│  │   Atelier peinture - 15 janvier        │     │
│  │   Il y a 5 heures                      │     │
│  ├────────────────────────────────────────┤     │
│  │ ● ✏️ Événement modifié                 │     │
│  │   Date changée pour Soirée de Noël     │     │
│  │   Hier                                 │     │
│  ├────────────────────────────────────────┤     │
│  │   🔄 Commission modifiée               │     │
│  │   Déplacée vers Cuisine                │     │
│  │   Il y a 2 jours                       │     │
│  ├────────────────────────────────────────┤     │
│  │   📢 Message important                 │     │
│  │   Réunion générale samedi              │     │
│  │   Il y a 3 jours                       │     │
│  ├────────────────────────────────────────┤     │
│  │ [Voir toutes les notifications]        │     │
│  └────────────────────────────────────────┘     │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

### Wireframe : Page Notifications Complète

```
┌──────────────────────────────────────────────────┐
│  MES NOTIFICATIONS                                │
├──────────────────────────────────────────────────┤
│                                                  │
│  Filtres : [Toutes] [Non lues] [Attribution]    │
│            [Événements] [Système]                │
│                                                  │
├──────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │ ● 📋 Nouvelle commission !                 │ │
│  │ Vous avez été assignée à la commission     │ │
│  │ Décoration pour l'événement Soirée de Noël │ │
│  │ 15 décembre 2024 à 14h30                   │ │
│  │ [Marquer comme lu] [Supprimer] [Détails]   │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │   📅 Nouvel événement !                    │ │
│  │ Atelier peinture - 15 janvier 2025         │ │
│  │ 14 décembre 2024 à 09h15                   │ │
│  │ [Marquer comme non lu] [Supprimer]         │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  ... (18 autres notifications)                  │
│                                                  │
│  ← 1 2 3 4 5 →                                   │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

### Wireframe : Onglet "Archivés"

```
┌──────────────────────────────────────────────────┐
│  MEMBRES                                          │
├──────────────────────────────────────────────────┤
│                                                  │
│  [Actifs (42)] [Archivés (5)] ← Onglets         │
│                                                  │
├──────────────────────────────────────────────────┤
│                                                  │
│  🔍 [Rechercher...] ☑ Inclure archivés           │
│                                                  │
├──────────────────────────────────────────────────┤
│                                                  │
│  Prénom  │ Nom     │ Chambre │ Archivé le │     │
├──────────────────────────────────────────────────┤
│  Alice   │ DUPONT  │ 101     │ 01/12/2024 │ 🔄 🗑│
│  Bob     │ MARTIN  │ 203     │ 15/11/2024 │ 🔄 🗑│
│  Claire  │ BERNARD │ 102     │ 20/10/2024 │ 🔄 🗑│
│  ...                                             │
│                                                  │
│  🔄 = Restaurer                                   │
│  🗑 = Supprimer définitivement                   │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 5. 📊 MÉTRIQUES DE SUCCÈS (KPIs)

### Métriques Quantitatives

| **KPI** | **Objectif** | **Mesure** |
|---------|--------------|-----------|
| **Adoption page profil** | 80% consultent leur profil dans les 7 jours | Analytics page views |
| **Upload photo profil** | 60% ajoutent une photo | Compteur uploads |
| **Taux d'utilisation notifications** | 90% cliquent sur notif dans les 24h | Analytics clics notif |
| **Suppression vs Archivage** | 100% archivage, 0% suppression directe | Logs suppressions |
| **Restaurations** | <10% des archivés restaurés | Logs restaurations |
| **Satisfaction UX** | NPS ≥ 8/10 sur "Interface moderne" | Survey post-déploiement |

### Métriques Qualitatives

- **Feedback Membres** : "J'adore voir mes stats de participation"
- **Feedback Admin** : "L'archivage sécurise mes suppressions"
- **Support** : -80% de demandes de changement de password (self-service)

---

## 6. ⚠️ RISQUES & MITIGATIONS

### Risque #1 : Performance des notifications (Polling)

**Probabilité :** Moyenne  
**Impact :** Moyen (latence, charge serveur)

**Causes possibles :**
- Polling toutes les 30s = 120 requêtes/heure/utilisateur
- 50 utilisateurs connectés = 6000 requêtes/heure

**Mitigation :**
- ✅ Endpoint optimisé : ne renvoyer que les nouvelles notifs (since_id)
- ✅ Cache Redis pour les notifications récentes (5 min)
- ✅ Rate limiting : 1 requête/30s max par user
- ✅ V2 : passer à WebSocket/SSE si scaling nécessaire

---

### Risque #2 : Upload photos volumineuses

**Probabilité :** Élevée  
**Impact :** Moyen (stockage, performance)

**Causes possibles :**
- Photos 10-20 MB uploadées depuis mobile
- Pas de compression côté client

**Mitigation :**
- ✅ Limite stricte : 5 MB (bloquant)
- ✅ Compression backend automatique (Pillow)
- ✅ Resize automatique : 300x300px (suffisant pour avatar)
- ✅ Format WebP (50% plus léger)
- ✅ Stockage S3/Cloudinary en production

---

### Risque #3 : Archivage accidentel

**Probabilité :** Faible  
**Impact :** Moyen (disruption)

**Causes possibles :**
- Admin archive par erreur un membre actif
- Membre retirée de commissions en cours

**Mitigation :**
- ✅ Modale de confirmation explicite
- ✅ Warning si assignations actives
- ✅ Restauration facile (1 clic)
- ✅ Logs d'audit (qui a archivé qui et quand)

---

### Risque #4 : Notifications spam

**Probabilité :** Moyenne  
**Impact :** Élevé (UX dégradée)

**Causes possibles :**
- Admin modifie 10 fois un événement = 10 notifs
- Membres noyées sous les notifications

**Mitigation :**
- ✅ Grouper les notifications similaires (ex: "3 événements modifiés")
- ✅ Option "Ne pas me notifier pour cet événement"
- ✅ Préférences de notifications (V2)
- ✅ Limite : max 5 notifications/jour/utilisateur

---

### Risque #5 : Packages externes obsolètes

**Probabilité :** Moyenne  
**Impact :** Moyen (dépendances)

**Causes possibles :**
- Flatpickr, Choices.js, etc. non maintenus
- Vulnérabilités de sécurité

**Mitigation :**
- ✅ Choisir des packages activement maintenus
- ✅ Vérifier les releases récentes (<6 mois)
- ✅ Audit Snyk/Dependabot automatique
- ✅ Plan B : composants Vue.js custom si abandon

---

## 7. 📌 NOTES POUR L'ÉQUIPE TECH

### Points d'Attention Backend (Django)

🔴 **Critique :**

**Soft Delete (Modèle Member)**
```python
# core/models.py

class Member(models.Model):
    # ... champs existants
    is_active = models.BooleanField(default=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    archived_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='archived_members')
    
    objects = models.Manager()  # Manager par défaut (tous)
    active_objects = ActiveMemberManager()  # Manager custom (actifs seulement)
    
    def archive(self, user):
        """Archive ce membre"""
        self.is_active = False
        self.archived_at = timezone.now()
        self.archived_by = user
        self.save()
        
        # Retirer de toutes les commissions actives
        self.assignments.filter(commission__event__date__gte=timezone.now()).delete()
    
    def restore(self):
        """Restaure ce membre"""
        self.is_active = True
        self.archived_at = None
        self.archived_by = None
        self.save()


class ActiveMemberManager(models.Manager):
    """Manager qui retourne uniquement les membres actifs"""
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
```

**Système de Notifications**
```python
# core/models.py

class Notification(models.Model):
    TYPES = [
        ('attribution', 'Attribution'),
        ('event', 'Événement'),
        ('modification', 'Modification'),
        ('system', 'Système'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL)
    related_commission = models.ForeignKey(Commission, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
        ]
    
    @staticmethod
    def create_attribution_notification(assignment, user):
        """Crée une notification d'attribution"""
        Notification.objects.create(
            user=user,
            type='attribution',
            title='Nouvelle commission !',
            message=f"Vous avez été assignée à la commission {assignment.commission.name} pour l'événement {assignment.commission.event.title}",
            related_commission=assignment.commission,
            related_event=assignment.commission.event
        )
    
    @staticmethod
    def cleanup_old_notifications():
        """Supprime les notifications >60 jours"""
        cutoff_date = timezone.now() - timedelta(days=60)
        Notification.objects.filter(created_at__lt=cutoff_date).delete()
```

**API Notifications (Polling)**
```python
# core/views/api.py

@require_http_methods(["GET"])
@login_required
def get_new_notifications(request):
    """
    Endpoint polling pour récupérer les nouvelles notifications
    Paramètre : since_id (optionnel)
    """
    since_id = request.GET.get('since_id', None)
    
    queryset = request.user.notifications.all()
    
    if since_id:
        queryset = queryset.filter(id__gt=since_id)
    
    notifications = queryset[:10]  # Max 10 nouvelles
    
    return JsonResponse({
        'notifications': [
            {
                'id': n.id,
                'type': n.type,
                'title': n.title,
                'message': n.message,
                'is_read': n.is_read,
                'created_at': n.created_at.isoformat(),
            }
            for n in notifications
        ],
        'unread_count': request.user.notifications.filter(is_read=False).count()
    })
```

**Upload Photo de Profil**
```python
# core/models.py

class Member(models.Model):
    # ... champs existants
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    def save_profile_picture(self, uploaded_file):
        """Sauvegarde et compresse la photo de profil"""
        from PIL import Image
        from io import BytesIO
        from django.core.files.uploadedfile import InMemoryUploadedFile
        
        img = Image.open(uploaded_file)
        
        # Resize to 300x300
        img.thumbnail((300, 300), Image.LANCZOS)
        
        # Convert to WebP
        output = BytesIO()
        img.save(output, format='WEBP', quality=85)
        output.seek(0)
        
        # Save
        self.profile_picture = InMemoryUploadedFile(
            output, 'ImageField',
            f"{self.id}_profile.webp",
            'image/webp',
            output.getbuffer().nbytes, None
        )
        self.save()
```

🟠 **Important :**
- **Index** : Créer index sur `Member.is_active` pour performance
- **Migration** : Data migration pour ajouter `is_active=True` à tous les membres existants
- **Cron Job** : Tâche quotidienne pour nettoyer notifications >60 jours
- **Cache** : Redis cache pour notifications récentes (5 min TTL)

🟢 **Nice to Have :**
- Signal `post_save` sur Assignment pour créer automatiquement la notification
- Command Django `python manage.py cleanup_notifications` (manuel)

---

### Points d'Attention Frontend (Vue.js + Tailwind)

🔴 **Critique :**

**Intégration Flatpickr**
```html
<!-- templates/base.html -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">
<script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
<script src="https://cdn.jsdelivr.net/npm/flatpickr/dist/l10n/fr.js"></script>
```

```javascript
// static/js/components/date-picker.js
flatpickr("#event-date", {
    locale: "fr",
    dateFormat: "d/m/Y",
    allowInput: true,
    minDate: "today",
    onChange: function(selectedDates, dateStr, instance) {
        // Callback si nécessaire
    }
});

flatpickr("#event-time", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true
});
```

**Intégration Choices.js**
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/choices.js/public/assets/styles/choices.min.css">
<script src="https://cdn.jsdelivr.net/npm/choices.js/public/assets/scripts/choices.min.js"></script>
```

```javascript
// static/js/components/select-multiple.js
const choices = new Choices('#member-select', {
    removeItemButton: true,
    searchEnabled: true,
    searchPlaceholderValue: 'Rechercher un membre...',
    noResultsText: 'Aucun membre trouvé',
    itemSelectText: 'Cliquer pour sélectionner',
});
```

**Polling Notifications**
```javascript
// static/js/notifications.js
const { createApp } = Vue;

createApp({
    data() {
        return {
            notifications: [],
            unreadCount: 0,
            lastNotificationId: null
        }
    },
    mounted() {
        this.startPolling();
    },
    methods: {
        async fetchNotifications() {
            const url = `/api/notifications/new/${this.lastNotificationId ? '?since_id=' + this.lastNotificationId : ''}`;
            
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.notifications.length > 0) {
                // Nouvelles notifications
                this.notifications = [...data.notifications, ...this.notifications];
                this.lastNotificationId = data.notifications[0].id;
                
                // Toast pour la plus récente
                this.showToast(data.notifications[0].title);
            }
            
            this.unreadCount = data.unread_count;
        },
        
        startPolling() {
            // Polling toutes les 30 secondes
            setInterval(() => {
                this.fetchNotifications();
            }, 30000);
            
            // Premier fetch immédiat
            this.fetchNotifications();
        }
    }
}).mount('#notifications-app');
```

🟠 **Important :**
- **Lazy Loading** : Charger Flatpickr/Choices.js uniquement sur les pages concernées
- **Touch Events** : Tester tous les composants sur iPad/iPhone
- **Accessibility** : Vérifier que date picker fonctionne au clavier

🟢 **Nice to Have :**
- Animation smooth lors de l'apparition des toasts
- Préchargement des images de profil (lazy loading)

---

### Points d'Attention Design

🔴 **Critique :**
- **Cohérence visuelle** : Tous les packages doivent s'intégrer au design Tailwind
- **Customisation Flatpickr** : Utiliser les variables CSS pour matcher les couleurs du thème
- **Icons** : Utiliser la même bibliothèque d'icônes partout (Heroicons recommandé)

🟠 **Important :**
- **Loading states** : Skeleton pour photo de profil pendant upload
- **Empty states** : Design spécifique pour "Aucune notification"

---

## 8. 📅 TIMELINE ESTIMÉE (Développement)

| **Phase** | **Durée** | **Livrables** |
|-----------|-----------|---------------|
| **Design : Intégration packages** | 3 jours | Flatpickr, Choices, Quill, Dropzone, Toastify |
| **Page "Mon Profil"** | 4 jours | 4 sections complètes + upload photo |
| **Visibilité commissions** | 2 jours | Page détail + permissions lecture seule |
| **Notifications : Backend** | 3 jours | Model + API + création auto |
| **Notifications : Frontend** | 3 jours | Badge + dropdown + page + polling |
| **Soft Delete** | 2 jours | Archivage + restauration + onglet |
| **Tests & Polish** | 3 jours | Tests + corrections + responsive |
| **Total** | **20 jours** (~4 semaines) |

---

## ✅ CHECKLIST DE VALIDATION

Avant de passer en production, vérifier :

### Design & Packages
- [ ] Date picker fonctionne sur mobile (touch-friendly)
- [ ] Time picker affiche format 24h
- [ ] Select multiple avec recherche opérationnel
- [ ] Rich text editor n'autorise que balises sécurisées
- [ ] Drag & drop fichiers fonctionne sur desktop + mobile
- [ ] Toasts s'affichent et disparaissent correctement

### Page Profil
- [ ] Upload photo ≤ 5MB avec compression automatique
- [ ] Changement password force reconnexion
- [ ] Statistiques affichent données correctes
- [ ] Admin peut modifier rôle d'autres membres

### Visibilité Commissions
- [ ] Membres voient toutes les commissions (lecture seule)
- [ ] Aucun bouton d'action visible pour Membres
- [ ] Admin/Déléguée voient boutons d'action

### Notifications
- [ ] Badge se met à jour en temps réel (30s max)
- [ ] Clic sur notification redirige vers bonne page
- [ ] Marquer comme lu/non lu fonctionne
- [ ] Suppression retire bien la notification
- [ ] Cleanup >60 jours actif (cron job)

### Soft Delete
- [ ] Archivage désactive le compte (impossibilité connexion)
- [ ] Membre archivé retiré des commissions actives
- [ ] Onglet "Archivés" visible uniquement Admin
- [ ] Restauration réactive le compte
- [ ] Suppression définitive demande confirmation stricte

### Performance
- [ ] Polling notifications ne surcharge pas le serveur
- [ ] Upload photo compresse à 300x300 WebP
- [ ] Page profil charge en <1s

---

## 🎉 CONCLUSION

Ce PRD couvre **5 améliorations majeures** post-MVP :

### ✅ Améliorations Livrées
1. **Design moderne** avec 6 packages externes (date, time, select, editor, upload, toasts)
2. **Page "Mon Profil"** complète (infos, sécurité, photo, stats)
3. **Visibilité commissions** pour tous (transparence totale)
4. **Notifications internes** (badge, dropdown, page, 4 types, 60 jours)
5. **Soft delete** (archivage, restauration, suppression définitive)

### 🎯 Impact Attendu
- **+50% engagement** : Profil + stats visibles
- **-70% charge admin** : Notifications automatiques
- **+40% transparence** : Commissions visibles par tous
- **0 perte de données** : Archivage au lieu de suppression
- **UX moderne** : Interface au niveau des apps 2024

### 📊 Métriques Clés
- 80% consultent leur profil dans 7 jours
- 60% ajoutent une photo
- 90% cliquent sur notifications dans 24h
- 100% archivage, 0% suppression directe

### ⏱️ Développement
**20 jours (~4 semaines)** pour implémenter les 5 features

---

**Statut :** PRD prêt pour validation et développement ! 🚀

**Prochaines étapes suggérées :**
1. Review avec l'équipe Dev + Design
2. Choix définitif des packages externes
3. Kick-off développement V1.5
