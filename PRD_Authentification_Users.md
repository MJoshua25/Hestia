# 📋 PRD — AUTHENTIFICATION & GESTION DES UTILISATEURS

**Produit :** Gestionnaire de Foyer pour Jeunes Filles  
**Feature :** Authentification Multi-Méthodes & Gestion Users  
**Version :** 1.0 (MVP)  
**Date :** Décembre 2025  
**Owner :** Product Architect

---

## 1. 📖 CONTEXTE & PROBLÈME

### Background
Pour utiliser le Gestionnaire de Foyer, chaque membre doit disposer d'un compte utilisateur. Le système doit gérer :
- La création automatique des comptes utilisateurs (User Django) lors de l'ajout d'un membre
- L'authentification sécurisée avec plusieurs méthodes adaptées à l'usage mobile
- La gestion du cycle de vie des identifiants (changement de password, définition d'un code PIN)

### Problèmes à Résoudre
- **🔐 Sécurité vs Simplicité** : Trouver l'équilibre entre un système sécurisé et une expérience fluide sur mobile
- **📱 Mobile-first** : Les membres accèdent majoritairement depuis leur smartphone
- **👥 Onboarding** : Simplifier la première connexion pour 30+ membres
- **🔄 Gestion des accès** : Admin/Déléguée doivent pouvoir réinitialiser les identifiants

### Pourquoi maintenant ?
Sans système d'authentification robuste, impossible de :
- Garantir la confidentialité des données
- Attribuer les bonnes permissions (Admin/Déléguée/Membre)
- Tracer les actions utilisateurs

### Impact Business Attendu
- **Adoption rapide** : Onboarding de 30 membres en < 1 heure (import Excel)
- **Taux de connexion** : 90% des membres se connectent au moins 1x/semaine
- **Support réduit** : < 5% de demandes de réinitialisation de password par mois

---

## 2. 🎯 OBJECTIFS & NON-OBJECTIFS

### ✅ Objectifs (Ce qu'on fait)

1. **Création automatique User ↔ Membre**  
   Chaque membre créé génère automatiquement un utilisateur Django avec credentials par défaut

2. **Triple méthode d'authentification**  
   - Username + Password (classique)
   - Numéro de téléphone + Password
   - Numéro de téléphone + Code PIN à 6 chiffres (passwordless)

3. **Première connexion sécurisée**  
   Forcer le changement du password par défaut et permettre la définition d'un code PIN

4. **Sessions longues**  
   Maximiser la durée des sessions pour éviter les reconnexions fréquentes

5. **Réinitialisation par Admin/Déléguée**  
   Permettre aux administrateurs de reset les identifiants des membres

6. **Import Excel avec génération automatique**  
   Créer massivement des users avec credentials par défaut

### ❌ Non-Objectifs (Ce qu'on ne fait PAS dans ce MVP)

- ❌ Authentification par OTP SMS (le code PIN est stocké, pas temporaire)
- ❌ Authentification biométrique (empreinte, Face ID)
- ❌ Authentification à deux facteurs (2FA)
- ❌ "Mot de passe oublié" en self-service (reset uniquement par Admin)
- ❌ Connexion via réseaux sociaux (Google, Facebook)
- ❌ Changement de numéro de téléphone en autonomie
- ❌ Historique des connexions détaillé

---

## 3. 👥 USER STORIES & CRITÈRES D'ACCEPTATION

### 🔹 US-A01 : Création automatique d'un User lors de l'ajout d'un Membre

**En tant qu'** Admin ou Déléguée  
**Je veux** qu'un compte utilisateur soit créé automatiquement quand j'ajoute un membre  
**Afin que** la membre puisse se connecter immédiatement à l'application

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée en tant qu'Admin ou Déléguée
AND je crée un membre "Alice DUPONT" avec :
  - Prénom : Alice
  - Nom : DUPONT
  - Numéro : 0612345678
  - Chambre : 101
WHEN je soumets le formulaire
THEN un User Django est créé automatiquement avec :
  - Username : "alice.dupont" (prénom.nom en minuscules)
  - Password : "pass_Default1" (password par défaut connu)
  - Numéro de téléphone : 0612345678 (stocké dans le profil User)
  - Role : "Membre" (par défaut)
  - Statut : require_password_change = True

GIVEN deux membres ont le même prénom ET nom (Alice DUPONT)
WHEN je crée le deuxième "Alice DUPONT"
THEN le username généré est "alice.dupont2"
AND le système incrémente automatiquement le suffixe

GIVEN je crée un membre sans numéro de téléphone
WHEN le User est créé
THEN l'authentification passwordless est désactivée pour ce user
AND seules les méthodes username + password sont disponibles
```

---

### 🔹 US-A02 : Page de connexion avec 3 méthodes

**En tant que** n'importe quelle utilisatrice  
**Je veux** une page de connexion unique avec plusieurs méthodes  
**Afin de** choisir la méthode la plus pratique pour moi

#### Critères d'Acceptation

```gherkin
GIVEN je suis sur la page de connexion
THEN je vois 3 onglets/options :
  1. "Username + Password"
  2. "Téléphone + Password"
  3. "Téléphone + Code PIN" (badgé "Connexion rapide")

GIVEN je sélectionne l'onglet "Username + Password"
WHEN l'onglet s'affiche
THEN je vois deux champs :
  - Username (placeholder: "prenom.nom")
  - Password (masqué)
AND un bouton "Se connecter"

GIVEN je sélectionne l'onglet "Téléphone + Password"
WHEN l'onglet s'affiche
THEN je vois deux champs :
  - Numéro de téléphone (format: 06 12 34 56 78)
  - Password (masqué)
AND un bouton "Se connecter"

GIVEN je sélectionne l'onglet "Téléphone + Code PIN"
WHEN l'onglet s'affiche
THEN je vois deux champs :
  - Numéro de téléphone
  - Code PIN (6 chiffres, masqué)
AND un message : "Vous devez avoir défini un code PIN au préalable"

GIVEN je suis sur mobile (viewport < 768px)
WHEN j'affiche la page de connexion
THEN les onglets deviennent des boutons radio empilés
AND le clavier numérique s'ouvre automatiquement pour le champ téléphone
```

---

### 🔹 US-A03 : Connexion avec Username + Password

**En tant qu'** utilisatrice  
**Je veux** me connecter avec mon username et mon password  
**Afin d'** accéder à l'application (méthode classique)

#### Critères d'Acceptation

```gherkin
GIVEN je saisis :
  - Username : "alice.dupont"
  - Password : "MonNouveauPass123!"
WHEN je clique sur "Se connecter"
THEN l'authentification réussit
AND je suis redirigée vers la page d'accueil
AND une session est créée (durée : 30 jours)

GIVEN je saisis un username incorrect
WHEN je tente de me connecter
THEN le système affiche : "Identifiants incorrects"
AND le formulaire n'est pas vidé (le username reste pré-rempli)

GIVEN je saisis un password incorrect (3 fois de suite)
WHEN la 3ème tentative échoue
THEN le système affiche : "Compte temporairement bloqué. Contactez un administrateur"
AND le compte est verrouillé pendant 15 minutes

GIVEN c'est ma première connexion (require_password_change = True)
WHEN l'authentification réussit
THEN je suis redirigée vers la page "Changer mon password"
AND je ne peux pas accéder à l'application avant d'avoir changé mon password
```

---

### 🔹 US-A04 : Connexion avec Numéro + Password

**En tant qu'** utilisatrice  
**Je veux** me connecter avec mon numéro de téléphone au lieu du username  
**Afin de** ne pas avoir à mémoriser mon username

#### Critères d'Acceptation

```gherkin
GIVEN je saisis :
  - Numéro : "0612345678" (ou "06 12 34 56 78" avec espaces)
  - Password : "MonNouveauPass123!"
WHEN je clique sur "Se connecter"
THEN le système recherche le User associé à ce numéro
AND l'authentification réussit
AND je suis connectée de la même manière qu'avec le username

GIVEN je saisis un numéro non enregistré
WHEN je tente de me connecter
THEN le système affiche : "Identifiants incorrects"
AND aucune indication sur l'existence ou non du numéro (sécurité)

GIVEN mon numéro est enregistré mais je n'ai pas de password (uniquement code PIN)
WHEN je tente de me connecter avec téléphone + password
THEN le système affiche : "Identifiants incorrects"
AND je suis invitée à utiliser la méthode "Téléphone + Code PIN"
```

---

### 🔹 US-A05 : Connexion Passwordless avec Code PIN

**En tant qu'** utilisatrice  
**Je veux** me connecter avec mon numéro et un code PIN à 6 chiffres  
**Afin de** me connecter rapidement sur mobile sans saisir de password complexe

#### Critères d'Acceptation

```gherkin
GIVEN j'ai préalablement défini un code PIN "123456"
AND je saisis :
  - Numéro : "0612345678"
  - Code PIN : "123456"
WHEN je clique sur "Se connecter"
THEN le système vérifie le code PIN associé à mon numéro
AND l'authentification réussit
AND je suis connectée avec une session de 30 jours

GIVEN je saisis un code PIN incorrect
WHEN je tente de me connecter
THEN le système affiche : "Code PIN incorrect"
AND après 5 tentatives, le système affiche : "Trop de tentatives. Utilisez votre password ou contactez un administrateur"

GIVEN je n'ai pas encore défini de code PIN
WHEN je tente de me connecter avec cette méthode
THEN le système affiche : "Aucun code PIN défini. Connectez-vous avec votre password pour en créer un"

GIVEN mon code PIN est "000000" ou "123456" (codes faibles)
WHEN je le définis la première fois
THEN le système affiche un avertissement : "⚠️ Code PIN faible. Choisissez une combinaison moins évidente"
BUT permet quand même de l'enregistrer (pas bloquant)
```

---

### 🔹 US-A06 : Première connexion et changement de password obligatoire

**En tant que** nouvelle utilisatrice  
**Je veux** être forcée de changer mon password par défaut  
**Afin de** sécuriser mon compte dès la première utilisation

#### Critères d'Acceptation

```gherkin
GIVEN c'est ma première connexion
AND je me connecte avec :
  - Username : "alice.dupont"
  - Password : "pass_Default1"
WHEN l'authentification réussit
THEN je suis redirigée vers la page "Première connexion"
AND je vois un formulaire avec :
  - "Nouveau password" (champ requis)
  - "Confirmer le password" (champ requis)
  - "Définir un code PIN (optionnel)" (champ à 6 chiffres)

GIVEN je saisis un nouveau password "MonPass123!"
AND je confirme ce password
AND je laisse le champ "Code PIN" vide
WHEN je soumets le formulaire
THEN mon password est mis à jour
AND require_password_change passe à False
AND je suis redirigée vers la page d'accueil
AND un message s'affiche : "Bienvenue ! Votre compte est configuré"

GIVEN je saisis également un code PIN "147258"
WHEN je soumets le formulaire
THEN mon password ET mon code PIN sont enregistrés
AND je peux désormais utiliser les 3 méthodes de connexion

GIVEN je tente de définir un password trop faible ("123456")
WHEN je soumets
THEN le système affiche : "Password trop faible. Min 8 caractères, 1 majuscule, 1 chiffre"
AND la soumission est bloquée

GIVEN je tente de contourner cette page (navigation directe vers /accueil)
WHEN je tente d'accéder
THEN je suis automatiquement redirigée vers la page de changement de password
AND je ne peux accéder à aucune autre page tant que ce n'est pas fait
```

---

### 🔹 US-A07 : Définir ou modifier son code PIN

**En tant qu'** utilisatrice déjà connectée  
**Je veux** définir ou modifier mon code PIN  
**Afin de** activer/changer ma connexion rapide passwordless

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée et j'accède à "Mon Profil"
WHEN j'affiche la section "Sécurité"
THEN je vois :
  - "Code PIN actuel : Non défini" (ou "Code PIN actif : ****")
  - Bouton "Définir un code PIN" (ou "Modifier le code PIN")

GIVEN je clique sur "Définir un code PIN"
WHEN le formulaire s'affiche
THEN je vois :
  - "Nouveau code PIN" (6 chiffres)
  - "Confirmer le code PIN" (6 chiffres)
  - "Password actuel" (pour confirmation)

GIVEN je saisis un nouveau code PIN "789012"
AND je confirme ce code
AND je saisis mon password actuel pour valider
WHEN je soumets
THEN le code PIN est enregistré (hashé en base)
AND un message s'affiche : "Code PIN activé. Vous pouvez maintenant l'utiliser pour vous connecter"

GIVEN je veux modifier mon code PIN existant
WHEN j'accède au formulaire
THEN je dois saisir :
  - "Code PIN actuel" (pour vérification)
  - "Nouveau code PIN"
  - "Confirmer le nouveau code PIN"

GIVEN je saisis un code PIN non numérique ou < 6 chiffres
WHEN je tente de valider
THEN le système affiche : "Le code PIN doit contenir exactement 6 chiffres"
```

---

### 🔹 US-A08 : Réinitialisation d'identifiants par Admin/Déléguée

**En tant qu'** Admin ou Déléguée  
**Je veux** réinitialiser le password ou le code PIN d'une membre  
**Afin de** débloquer son accès en cas d'oubli

#### Critères d'Acceptation

```gherkin
GIVEN je suis connectée en tant qu'Admin ou Déléguée
AND je consulte la fiche de "Alice DUPONT"
WHEN j'accède à la section "Sécurité"
THEN je vois deux boutons :
  - "Réinitialiser le password"
  - "Supprimer le code PIN"

GIVEN je clique sur "Réinitialiser le password"
WHEN la modale s'affiche
THEN je vois le message :
  "Le password de Alice DUPONT sera réinitialisé à : pass_Default1"
  "Elle devra le changer lors de sa prochaine connexion"
AND je vois deux options : "Annuler" | "Confirmer"

GIVEN je confirme la réinitialisation
WHEN l'action s'exécute
THEN le password de Alice est remis à "pass_Default1"
AND require_password_change est remis à True
AND un message s'affiche : "Password réinitialisé. Informez Alice qu'elle doit se reconnecter"

GIVEN je clique sur "Supprimer le code PIN"
WHEN je confirme
THEN le code PIN de Alice est supprimé de la base
AND elle ne peut plus utiliser la méthode passwordless
AND elle doit en définir un nouveau depuis son profil

GIVEN je suis une Membre (rôle basique)
WHEN je consulte le profil d'une autre membre
THEN je ne vois PAS les options de réinitialisation
```

---

### 🔹 US-A09 : Import Excel avec génération automatique de Users

**En tant qu'** Admin  
**Je veux** importer des membres en masse et créer automatiquement leurs comptes  
**Afin de** onboarder rapidement 30+ membres

#### Critères d'Acceptation

```gherkin
GIVEN je téléverse un fichier Excel avec 50 membres
AND chaque ligne contient : Prénom | Nom | Numéro | Chambre
WHEN l'import s'exécute
THEN 50 Users Django sont créés automatiquement avec :
  - Username généré : "prenom.nom" (ou "prenom.nom2" si doublon)
  - Password par défaut : "pass_Default1"
  - Numéro de téléphone : celui du fichier
  - Statut : require_password_change = True

GIVEN le fichier contient des doublons (2x "Alice DUPONT")
WHEN l'import s'exécute
THEN les usernames générés sont : "alice.dupont" et "alice.dupont2"
AND un rapport d'import affiche :
  "✓ 50 membres importés avec succès"
  "⚠️ 2 doublons détectés : suffixes ajoutés automatiquement"

GIVEN je télécharge le rapport d'import après traitement
WHEN je l'ouvre
THEN je vois un tableau avec :
  - Nom complet
  - Username généré
  - Password par défaut : "pass_Default1"
  - Statut : "À activer" (première connexion requise)

GIVEN certaines lignes n'ont pas de numéro de téléphone
WHEN l'import s'exécute
THEN les Users sont créés quand même
AND la méthode passwordless est désactivée pour ces users
```

---

### 🔹 US-A10 : Session longue durée

**En tant qu'** utilisatrice  
**Je veux** rester connectée le plus longtemps possible  
**Afin de** ne pas avoir à me reconnecter à chaque visite

#### Critères d'Acceptation

```gherkin
GIVEN je me connecte avec succès
WHEN je ne coche pas "Rester connecté(e)"
THEN une session de 30 jours est créée automatiquement

GIVEN je coche la case "Rester connecté(e)" (si affichée)
WHEN je me connecte
THEN une session de 90 jours est créée

GIVEN je ferme complètement mon navigateur mobile
WHEN je rouvre l'app 7 jours plus tard
THEN je suis toujours connectée
AND je peux naviguer sans redemander mes identifiants

GIVEN ma session expire après 30 jours
WHEN je tente d'accéder à une page
THEN je suis redirigée vers la page de connexion
AND un message s'affiche : "Votre session a expiré. Veuillez vous reconnecter"

GIVEN je clique sur "Se déconnecter" (menu profil)
WHEN je confirme
THEN ma session est détruite immédiatement
AND je suis redirigée vers la page de connexion
```

---

## 4. 🎨 UX/UI REQUIREMENTS

### User Flow : Première connexion d'une nouvelle membre

```
[Membre créée par Admin]
    → User généré : username="alice.dupont", password="pass_Default1"
    
[Alice reçoit l'info (SMS/WhatsApp/en personne)]
    → "Ton username : alice.dupont"
    → "Password temporaire : pass_Default1"
    
[Alice ouvre l'app]
    ↓
[Page de Connexion]
    → Saisit username + password par défaut
    ↓
[Détection première connexion]
    ↓
[Page "Première Connexion"]
    → Formulaire :
      - Nouveau password* (min 8 char, 1 maj, 1 chiffre)
      - Confirmer password*
      - Code PIN (optionnel, 6 chiffres)
    ↓ Validation
[Redirection vers Accueil]
    → "Bienvenue Alice ! Votre compte est activé"
```

### User Flow : Connexion passwordless (membre déjà configurée)

```
[Marie ouvre l'app]
    ↓
[Page de Connexion]
    → Sélectionne onglet "Téléphone + Code PIN"
    → Saisit : 0698765432
    → Saisit : 147258 (son code PIN)
    ↓ Clic "Se connecter"
[Vérification code PIN]
    ↓
[Redirection vers Accueil]
    → Session créée (30 jours)
```

### User Flow : Réinitialisation par Admin

```
[Admin consulte fiche de "Marie"]
    ↓
[Section Sécurité]
    → Clic "Réinitialiser le password"
    ↓
[Modale de confirmation]
    → "Password sera remis à pass_Default1"
    → [Annuler] [Confirmer]
    ↓ Clic "Confirmer"
[Password réinitialisé]
    → "✓ Password réinitialisé. Informez Marie"
    
[Admin informe Marie]
    → "Reconnecte-toi avec pass_Default1"
    
[Marie se reconnecte]
    → Détection require_password_change = True
    → Forcée de changer son password
```

### Wireframe Mobile : Page de Connexion

```
┌─────────────────────────┐
│                         │
│   🏠 FOYER MANAGER      │
│                         │
├─────────────────────────┤
│                         │
│ ⚪ Username + Password  │
│ ⚪ Téléphone + Password │
│ ⚫ Téléphone + Code PIN │
│     [Connexion rapide]  │
│                         │
├─────────────────────────┤
│                         │
│ 📱 Numéro de téléphone │
│ ┌─────────────────────┐│
│ │ 06 12 34 56 78      ││
│ └─────────────────────┘│
│                         │
│ 🔢 Code PIN (6 chiffres)│
│ ┌─────────────────────┐│
│ │ ● ● ● ● ● ●         ││
│ └─────────────────────┘│
│                         │
│ ℹ️ Vous devez avoir     │
│    défini un code PIN  │
│                         │
│ [   Se connecter   ]    │
│                         │
└─────────────────────────┘
```

### Wireframe Desktop : Page de Connexion

```
┌────────────────────────────────────────────┐
│                                            │
│           🏠 FOYER MANAGER                 │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  ┌────────┬────────────┬──────────────┐   │
│  │Username│ Téléphone  │ Téléphone +  │   │
│  │   +    │     +      │   Code PIN   │   │
│  │Password│  Password  │  [Rapide] ✓  │   │
│  └────────┴────────────┴──────────────┘   │
│                                            │
│  📱 Numéro de téléphone                    │
│  ┌──────────────────────────────────────┐ │
│  │ 06 12 34 56 78                       │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  🔢 Code PIN (6 chiffres)                  │
│  ┌──────────────────────────────────────┐ │
│  │ ● ● ● ● ● ●                          │ │
│  └──────────────────────────────────────┘ │
│                                            │
│  ℹ️ Vous devez avoir défini un code PIN    │
│     lors de votre première connexion       │
│                                            │
│  ┌────────────────────────────────────┐   │
│  │       Se connecter                 │   │
│  └────────────────────────────────────┘   │
│                                            │
└────────────────────────────────────────────┘
```

### Wireframe Mobile : Première Connexion

```
┌─────────────────────────┐
│  ⬅️ PREMIÈRE CONNEXION  │
├─────────────────────────┤
│                         │
│ 👋 Bienvenue Alice !    │
│                         │
│ Configurez votre compte │
│                         │
│ 🔒 Nouveau password*    │
│ ┌─────────────────────┐│
│ │                     ││
│ └─────────────────────┘│
│ Min 8 caractères       │
│                         │
│ 🔒 Confirmer password* │
│ ┌─────────────────────┐│
│ │                     ││
│ └─────────────────────┘│
│                         │
│ 🔢 Code PIN (optionnel)│
│ ┌─────────────────────┐│
│ │ ● ● ● ● ● ●         ││
│ └─────────────────────┘│
│ Pour connexion rapide  │
│                         │
│ [  Valider mon compte] │
│                         │
└─────────────────────────┘
```

### États d'Interface

| **État** | **Description** | **Visuel** |
|----------|----------------|-----------|
| **Champs vides** | État initial | Placeholders visibles |
| **Saisie en cours** | Focus actif | Bordure bleue sur champ actif |
| **Erreur de saisie** | Identifiants incorrects | Champ rouge + message "Identifiants incorrects" |
| **Compte bloqué** | 3 tentatives échouées | Message rouge "Compte bloqué 15 min" |
| **Loading** | Vérification en cours | Spinner sur bouton "Se connecter..." |
| **Succès** | Connexion validée | Redirection immédiate (pas de toast) |

---

## 5. 📊 MÉTRIQUES DE SUCCÈS (KPIs)

### Métriques Quantitatives

| **KPI** | **Objectif** | **Mesure** |
|---------|--------------|-----------|
| **Taux d'activation** | 95% des membres se connectent dans les 48h | Logs première connexion |
| **Adoption passwordless** | 60% des membres utilisent le code PIN | Méthode d'auth utilisée |
| **Durée moyenne de connexion** | < 10 secondes | Analytics temps formulaire → accueil |
| **Taux de réinitialisation** | < 5% par mois | Logs actions Admin |
| **Durée session moyenne** | > 20 jours | Analytics sessions actives |

### Métriques Qualitatives

- **NPS connexion** : "Facilité de connexion" ≥ 8/10
- **Feedback membres** : "Je préfère le code PIN, c'est plus rapide"
- **Support** : < 3 demandes d'aide connexion par mois

---

## 6. ⚠️ RISQUES & MITIGATIONS

### Risque #1 : Adoption faible du code PIN

**Probabilité :** Moyenne  
**Impact :** Moyen (objectif non atteint)

**Causes possibles :**
- Les membres ne savent pas que cette option existe
- Crainte d'oublier le code

**Mitigation :**
- ✅ Mettre en avant le code PIN avec badge "Connexion rapide"
- ✅ Tutoriel vidéo de 30s sur la première connexion
- ✅ Message incitatif : "Définissez un code PIN pour vous connecter en 5 secondes"

---

### Risque #2 : Sécurité du password par défaut

**Probabilité :** Élevée  
**Impact :** Critique (accès non autorisé)

**Causes possibles :**
- Password "pass_Default1" connu de tous
- Membre ne change pas son password immédiatement

**Mitigation :**
- ✅ **OBLIGATOIRE** : Forcer le changement de password dès la première connexion (bloquant)
- ✅ Flag `require_password_change` vérifié à chaque requête
- ✅ Impossible d'accéder à l'app avant changement de password
- ✅ Logs des tentatives de connexion avec password par défaut

---

### Risque #3 : Confusion entre les 3 méthodes

**Probabilité :** Moyenne  
**Impact :** Faible (UX dégradée)

**Causes possibles :**
- Trop de choix sur la page de connexion
- Membres essaient la mauvaise méthode

**Mitigation :**
- ✅ Design clair avec onglets ou boutons radio visuellement distincts
- ✅ Messages d'aide contextuels ("Vous devez avoir un code PIN défini")
- ✅ Mémoriser la dernière méthode utilisée (cookie local)

---

### Risque #4 : Oubli du code PIN sans fallback

**Probabilité :** Moyenne  
**Impact :** Moyen (blocage utilisateur)

**Causes possibles :**
- Membre oublie son code PIN
- Pas d'option "Code PIN oublié" en self-service

**Mitigation :**
- ✅ Message clair : "En cas d'oubli, utilisez votre password ou contactez un administrateur"
- ✅ Admin peut supprimer le code PIN rapidement
- ✅ Documentation : "Choisissez un code facile à mémoriser"

---

### Risque #5 : Sécurité des codes PIN faibles

**Probabilité :** Élevée  
**Impact :** Moyen (accès facilité)

**Causes possibles :**
- Codes évidents : 000000, 123456, 111111
- Pas de validation stricte

**Mitigation :**
- ✅ Avertissement (non bloquant) pour codes faibles
- ✅ Limitation des tentatives : 5 essais max puis blocage
- ✅ Recommandation : "Évitez les suites ou répétitions"
- ⚠️ Ne PAS bloquer les codes faibles (trop contraignant pour le MVP)

---

## 7. 📌 NOTES POUR L'ÉQUIPE TECH

### Points d'Attention Backend (Django)

🔴 **Critique :**

**Modèle User étendu**
```python
# core/models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    pin_code = models.CharField(max_length=128, null=True, blank=True)  # Hashé avec make_password()
    require_password_change = models.BooleanField(default=True)
    role = models.CharField(max_length=10, choices=[
        ('admin', 'Admin'),
        ('delegate', 'Déléguée'),
        ('member', 'Membre')
    ], default='member')
    
    def set_pin(self, pin):
        """Hash et stocke le code PIN"""
        from django.contrib.auth.hashers import make_password
        self.pin_code = make_password(pin)
        self.save()
    
    def check_pin(self, pin):
        """Vérifie le code PIN"""
        from django.contrib.auth.hashers import check_password
        return check_password(pin, self.pin_code)
```

**Génération automatique username**
```python
# core/utils.py
def generate_username(first_name, last_name):
    """Génère un username unique : prenom.nom ou prenom.nom2"""
    base_username = f"{first_name.lower()}.{last_name.lower()}"
    username = base_username
    counter = 2
    
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    
    return username
```

**Backend d'authentification custom**
```python
# core/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhonePasswordBackend(ModelBackend):
    """Authentification par numéro + password"""
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

class PhonePINBackend(ModelBackend):
    """Authentification par numéro + code PIN"""
    def authenticate(self, request, phone_number=None, pin_code=None, **kwargs):
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.pin_code and user.check_pin(pin_code):
                return user
        except User.DoesNotExist:
            return None

# settings.py
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Username + Password
    'core.backends.PhonePasswordBackend',         # Phone + Password
    'core.backends.PhonePINBackend',              # Phone + PIN
]
```

**Middleware pour forcer changement de password**
```python
# core/middleware.py
from django.shortcuts import redirect

class RequirePasswordChangeMiddleware:
    """Force la redirection vers /change-password si require_password_change=True"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.require_password_change and request.path != '/change-password/':
                return redirect('change_password')
        return self.get_response(request)
```

🟠 **Important :**
- Sessions : `SESSION_COOKIE_AGE = 2592000` (30 jours)
- Rate limiting sur tentatives de connexion (django-ratelimit)
- Logs détaillés des authentifications (qui, quand, méthode utilisée)
- Index sur `phone_number` pour performance

🟢 **Nice to Have :**
- Dashboard Admin Django pour voir les users avec `require_password_change=True`
- Signal post_save sur Member pour créer automatiquement le User

---

### Points d'Attention Frontend (Vue.js + Tailwind)

🔴 **Critique :**

**Composant Login avec onglets**
```javascript
// static/js/login.js
const { createApp } = Vue;

createApp({
    data() {
        return {
            loginMethod: 'phone_pin',  // Par défaut : méthode la plus simple
            username: '',
            phone: '',
            password: '',
            pin: ''
        }
    },
    methods: {
        async login() {
            let credentials = {};
            
            if (this.loginMethod === 'username_password') {
                credentials = { username: this.username, password: this.password };
            } else if (this.loginMethod === 'phone_password') {
                credentials = { phone_number: this.phone, password: this.password };
            } else if (this.loginMethod === 'phone_pin') {
                credentials = { phone_number: this.phone, pin_code: this.pin };
            }
            
            const response = await fetch('/api/auth/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(credentials)
            });
            
            if (response.ok) {
                window.location.href = '/';
            } else {
                // Gérer l'erreur
            }
        }
    }
}).mount('#login-app');
```

**Validation code PIN (6 chiffres uniquement)**
```javascript
// Composant PIN input
<input 
    type="text" 
    inputmode="numeric" 
    maxlength="6" 
    pattern="[0-9]{6}"
    @input="validatePin"
>

methods: {
    validatePin(event) {
        // Autoriser uniquement les chiffres
        event.target.value = event.target.value.replace(/[^0-9]/g, '');
    }
}
```

🟠 **Important :**
- Auto-focus sur premier champ au chargement
- Clavier numérique sur mobile (inputmode="numeric")
- Message d'erreur contextualisé selon la méthode
- Débounce sur la saisie pour éviter requêtes inutiles

🟢 **Nice to Have :**
- Animation de transition entre onglets
- Masquer/afficher password avec icône œil
- Sauvegarde de la dernière méthode utilisée (localStorage)

---

### Points d'Attention Design

🔴 **Critique :**
- **Contraste élevé** : Textes lisibles sur fond clair (WCAG AA)
- **Touch targets** : Boutons ≥ 44px de hauteur sur mobile
- **Feedback visuel** : Bordure rouge sur erreur, verte sur succès

🟠 **Important :**
- **Hiérarchie visuelle** : Méthode "Téléphone + Code PIN" mise en avant (badge "Rapide")
- **Empty states** : Placeholder explicite ("06 12 34 56 78")
- **Loading states** : Spinner sur bouton pendant vérification

---

## 8. 📅 TIMELINE ESTIMÉE (Développement)

| **Phase** | **Durée** | **Livrables** |
|-----------|-----------|---------------|
| **Model User étendu** | 1 jour | Model + migrations |
| **Backends d'authentification** | 2 jours | 3 backends custom |
| **Page de connexion** | 2 jours | UI avec 3 onglets + logique |
| **Première connexion** | 1 jour | Formulaire changement password + PIN |
| **Middleware force password** | 1 jour | Redirection automatique |
| **Réinitialisation Admin** | 1 jour | Vues Admin pour reset |
| **Import Excel + Users** | 1 jour | Génération automatique users |
| **Sessions longues** | 0.5 jour | Configuration Django |
| **Tests & sécurité** | 2 jours | Tests unitaires + rate limiting |
| **Total** | **11.5 jours** (~2.5 semaines) |

---

## ✅ CHECKLIST DE VALIDATION

Avant de passer en production, vérifier :

- [ ] User créé automatiquement lors de l'ajout d'un membre
- [ ] Username généré respecte le pattern `prenom.nom` (+ suffixe si doublon)
- [ ] Les 3 méthodes de connexion fonctionnent
- [ ] Changement de password obligatoire à la première connexion (bloquant)
- [ ] Code PIN hashé en base (jamais en clair)
- [ ] Rate limiting actif (3 tentatives avant blocage 15 min)
- [ ] Sessions de 30 jours actives
- [ ] Admin peut réinitialiser password et supprimer code PIN
- [ ] Import Excel génère les users avec credentials par défaut
- [ ] Tests sur iOS et Android (clavier numérique, auto-focus)
- [ ] Logs des authentications fonctionnels

---

## 🎉 CONCLUSION

Ce PRD définit un **système d'authentification robuste et flexible** qui :
- ✅ Sécurise l'accès avec changement de password obligatoire
- ✅ Simplifie l'expérience mobile avec le code PIN
- ✅ Automatise la création des comptes utilisateurs
- ✅ Maximise la durée des sessions (moins de reconnexions)

**Architecture technique :**
- User Django étendu avec `phone_number` et `pin_code`
- 3 backends d'authentification custom
- Middleware pour forcer le changement de password
- Sessions longues (30 jours par défaut)

**Prochaine étape :** Validation de ce PRD, puis développement ou passage au PRD **Gestion des Commissions & Attribution Aléatoire** ! 🎲
