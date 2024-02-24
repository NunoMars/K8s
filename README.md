# Infrastructure et Guide d'Installation

## Architecture

### Composants de l'Infrastructure :

1. **Cluster Kubernetes** :
   - Un cluster Kubernetes est utilisé pour orchestrer les conteneurs et gérer les ressources de manière efficace.

2. **ArgoCD** :
   - ArgoCD est employé pour mettre en œuvre le déploiement en mode GitOps. Il surveille un dépôt Git spécifique et applique automatiquement les changements détectés sur les clusters Kubernetes. Cela garantit une gestion des configurations centralisée et reproductible.

3. **Git Repository** :
   - Le dépôt Git est structuré en deux branches principales : `dev` et `master`.
     - **dev**: Cette branche est utilisée pour le développement et les tests. Les changements sont d'abord déployés sur cet environnement.
     - **master**: Cette branche représente l'environnement de production où les versions stables sont déployées après validation.

4. **GitHub Actions** :
   - GitHub Actions est utilisé pour automatiser le processus de création d'images Docker et leur publication sur DockerHub. Des workflows sont configurés pour déclencher ces actions lors de chaque push sur les branches `dev` et `master`.

5. **DockerHub** :
   - DockerHub est utilisé comme registre d'images pour stocker les images Docker des applications.

6. **ConfigMap** :
   - Un ConfigMap est utilisé pour stocker deux variables :
     - URL du backend : Cette variable détermine l'URL du service backend à utiliser.
     - Environnement : Cette variable indique l'environnement actuel, que ce soit "prod" ou "dev".

7. **Persistent Volume Claim (PVC)** :
   - Le PVC est utilisé pour stocker les fichiers de base de données nécessaires au fonctionnement de l'application. Il assure la persistance des données même en cas de redéploiement ou de mise à l'échelle des pods.

8. **Déploiement Kubernetes** :
   - Le déploiement Kubernetes orchestre l'ensemble des composants de l'application. Il s'assure que les pods sont correctement instanciés et configure les services nécessaires pour les exposer.

9. **Service Backend** :
   - Ce service est exposé en tant que ClusterIP sur le port 5000. Il gère le pod de backend qui contient une API Django Flask. Les requêtes provenant du frontend sont dirigées vers ce service pour traitement.

10. **Service Frontend** :
   - Ce service est exposé en tant que LoadBalancer. Le ConfigMap est monté sur ce service pour permettre l'accès à l'environnement et à l'adresse du service Backend. Il s'agit de l'interface utilisateur de l'application et reçoit les requêtes des utilisateurs.

### Configuration des Namespaces :

Pour une isolation et une gestion efficace des environnements, les namespaces suivants sont utilisés :

- **nuno-dev** : Utilisé pour le développement et les tests. Les déploiements de la branche `dev` sont effectués dans ce namespace.
- **nuno-prod** : Représente l'environnement de production où les versions stables sont déployées après validation. Les déploiements de la branche `master` sont effectués dans ce namespace.

### Workflow GitHub Actions :

- Des workflows GitHub Actions sont configurés pour déclencher automatiquement la création et la publication des images Docker sur DockerHub à chaque push sur les branches `dev` et `master`.
- Les workflows récupèrent les sources depuis le dépôt Git, construisent les images Docker correspondantes et les publient sur DockerHub.

## Installation

Suivez les étapes ci-dessous pour installer l'infrastructure sur votre environnement Kubernetes :

1. **Configuration du Cluster Kubernetes** :
   - Assurez-vous d'avoir un cluster Kubernetes prêt à l'emploi.
   - Installez les outils Kubernetes nécessaires, notamment kubectl et helm.

2. **Installation d'ArgoCD** :
   - Suivez les instructions officielles d'ArgoCD pour l'installer sur votre cluster Kubernetes.

3. **Configuration du Dépôt Git** :
   - Créez un dépôt Git avec deux branches : `dev` et `master`.
   - Ajoutez les fichiers de configuration nécessaires pour le déploiement dans ce dépôt.

4. **Configuration des Workflows GitHub Actions** :
   - Ajoutez les workflows GitHub Actions dans le dépôt Git pour automatiser la création et la publication des images Docker sur DockerHub.

5. **Déploiement Initial** :
   - Utilisez ArgoCD pour déployer l'application initiale à partir de la branche `dev`.
   - Vérifiez que tous les pods sont en cours d'exécution correctement dans le namespace `nuno-dev`.

6. **Configuration pour la Production** :
   - Basculez vers la branche `master` pour déployer en production.
   - Utilisez ArgoCD pour déployer l'application dans le namespace `nuno-prod`.
   - Configurez les HPA pour scaler automatiquement les pods en fonction du trafic dans le namespace `nuno-prod`.

7. **Tests et Surveillance** :
   - Effectuez des tests pour vérifier le bon fonctionnement de l'application dans les deux environnements.
   - Surveillez les performances de l'application et ajustez les ressources au besoin.
   - il y a un livenessprobe sur le port 80 pour le front et sur le 5000 pour le back qui s'execute touttes les 5 secondes
