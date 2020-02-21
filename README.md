# Web Crawler & Scraper

Premiere remise pour le projet de INF8007.

Ce script va rechercher et verifier le status de tous les liens presents sur la page du lien fournis.
Ensuite, ce dernier parcourera tous les lien valides present sur le meme domaine afin d'extraire
de nouveaux liens et verifier leurs status.

## Getting Started
Afin de rouler le script, il suffit de remplacer la valeur de la variable base_url (ligne 7) dans le fichier main.py.
Ensuite, vous pouvez rouler le script. Le rapport final (en json) se trouvera dans le fichier 'link_status_report.json' a la
racine du projet.

Le format du rapport est comme suit:
```
{
    "https://www.baseurl.com": [["https://www.baseurl.com/somepage.html", 200],["https://www.external.com/somepage.html", 404]],
    "https://www.baseurl.com/somepage.html": [["https://www.baseurl.com", 200],["https://www.external2.com", 404]]
}
```

### Installing & Prerequisites

Vous devez installer la librairie requests
```
pip install requests
```


## Authors

Olivier Brochu Dufour
Oceane Destras