# Web Crawler & Scraper

Deuxieme remise pour le projet de INF8007.

Ce script va rechercher et verifier le status de tous les liens presents sur la page du lien fournis.
Ensuite, ce dernier parcourera tous les lien valides present sur le meme domaine afin d'extraire
de nouveaux liens et verifier leurs status.

## Getting Started
Afin de rouler les scripts, référez-vous a la section "Usage".
Le script bash clone le repo git spécifier, lance le serveur au port local spécifié et roule main.py sur ce port local.
Une fois roulé, le rapport final (en json) se trouvera dans le fichier 'link_status_report.json' a la
racine du dossier d'execution.

Le format du rapport est comme suit:
```
{
    "https://www.baseurl.com": [["https://www.baseurl.com/somepage.html", 200],["https://www.external.com/somepage.html", 404]],
    "https://www.baseurl.com/somepage.html": [["https://www.baseurl.com", 200],["https://www.external2.com", 404]]
}
```

### Installing & Prerequisites

Vous devez utiliser python 3 et vous devez installer la librairie requests
```
pip install requests
```

### Usage
#### Main script usage
```
Usage examples:
python3 main.py url https://spacejam.com
python3 main.py url https://spacejam.com crawling false
python3 main.py file /path/to/file.html
python3 main.py stdin html|filelist|urllist:
   echo [\"https://spacejam.com\"] | python main.py stdin urllist
   echo [\"./tests/spacejam.html\"] | python main.py stdin filelist
   python main.py stdin html < ./tests/spacejam.html
----------------------------------------------
Parameter details:
help -> shows this message
url -> string url
file -> string path to a file
stdin -> accepted values are:
   html -> will tell the program to expect html in the stdin
   filelist -> will tell the program expect a JSON array of file paths in the stdin
   urllist -> will tell the program expect a JSON array of urls in the stdin
!!!! NOTE: url, file, and stdin are mutually exclusive. You must only use one of them.
crawling -> true (default) or false. (can be capitalized) To be used whenever the program reads URLs
```
#### Bash Script Usage
For mac and linux:
```
bash.sh [-u] git_url [-p] port. You should execute this script within the project directory.
```
For windows:
```
bash_win.sh [-u] git_url [-p] port. You should execute this script within the project directory.
```
Warning: bash script will call python using the 'python3' command. If your system uses an other command to call python 
3 you need to change it in the script.
## Authors

Olivier Brochu Dufour
Oceane Destras