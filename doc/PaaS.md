# Platform as a service


### Objectifs 
Dans le cadre de l'application ANdo checker un PAAS (Platform as a service) est nécessaire ce document auras pour but de comparer les PAASs gratuits disponibles afin de nous aiguiller dans notre choix 
## Table des  matières
0. [Objectifs](#Objectifs)
1. [ PAAS disponible](#PAAS-disponible)
2. [Remarques](#Remarques)
3. [ Conclusion ](#Conclusion)

## PAAS disponible 
Ci-dessous un énumération des PAAS disponible avec leur spécification :

Nom|Ram| Persistant Storage|Resource hibernation|Expiration
:---|:---|:---|:---|:---|
Heroku| 512 MB|500 MB |The app sleeps after 30 minutes of inactivity|1000 free hours/month
OpenShift| 2 GB|2 GB | Your project resources sleep after 30 minutes of inactivity, and must sleep 18 hours in a 72 hour period|Your subscription automatically expires after 60 days; resubscribe as often as you like
Google App Engine| NC|5 GB |NC |NC
Gigalixir|  NC | NC |  Never sleeps|NC
Pythonanywhere| NC | NC  |  NC|NC 

## Remarques
Ci-dessous les informations pertinentes relevé pour certain PAAS susceptibles de nous aidé dans notre choix 


Nom|Remarque
:---|:---|
Heroku|Dans la grande majorité la communauté présente Heroku comme LA meilleur solution à court terme pour des petits projets, mais dès que le projet prend de l'ampleur et que les ressources deviennent insuffisantes les offre payante sont couteuse par rapport au service obtenue.
Openshift| Me semble pertinent malgré le manque de tutoriel et le fait de devoir tous les 60 jours se réinscrire et rebuild le projet.
Google App Engine|Trop peu d'information disponible.
Gigalixir|Pas créé spécifiquement pour des projets codé en python dans leur vidéo de présentation ils expliquent de Gigalixir peu prendre en charge pas mal de langage mais 0 information de trouvé sur leur site a ce sujet.
pythonanywhere|Pratiquement 0 information sur les ressources mise a disposition . La seule information disponible et que le nom du site devra être sous cette forme : yourapp.pythonanywhere.com

# Conclusion 
Pour conclure a mon avis aucune des solutions disponible ne corresponds a nos besoins soit par manque d'information soit pas adapté a notre solution , Je dirais donc qu'une implémentation en locale avec une solution des déploiement et intégration continue et le plus adapté pour notre projet avec des outils comme Jenkins , Travis CI, Circle CI .

