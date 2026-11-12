# Physical Music Radar

## Sony Music Identity Style Guide

Die Oberfläche wurde auf Basis des bereitgestellten Sony Music Identity Style Guides (V.1, Oktober 2023) neugestaltet. Verwendet werden Sony-Rot `#f90000`, Schwarz `#000000` und Weiß `#ffffff`, linksbündige, kompakte Überschriften und ein modulares Layout. Die dekorativen Kreise der Hero-Fläche sind **kein Sony Music Logo**. Das offizielle Sony Music Logo wurde bewusst nicht neu gezeichnet oder verfremdet. Für die Verwendung im Produkt muss eine freigegebene Original-Logodatei aus dem Corporate-Asset-Verzeichnis bereitgestellt und entsprechend den Vorgaben platziert werden.

Die im Style Guide vorgeschriebene Schrift ist **Basic Commercial LT STD** in Black und Roman. Aus Lizenzgründen sind keine Schriftdateien enthalten. Falls die Schrift lokal installiert bzw. intern eingebunden ist, wird sie bevorzugt verwendet. Sonst greift das CSS auf Systemschrift zurück. Für verbindliche Corporate-Freigabe bitte intern prüfen.


Eine responsive HTML/CSS/JavaScript-Website für physische Musikprodukte. Mit 12 Hersteller-Einträgen, Hersteller-Monitor, Branchen-News, Suche, Kategorien, Merkliste und CSV-Export.

## Schnellstart

`index.html` im Browser öffnen. Ohne Konfiguration erscheinen **nur sechs klar gekennzeichnete Beispielmeldungen**. Es findet keine Live-Recherche statt.

## GitHub + Vercel: Website veröffentlichen

1. Neues GitHub-Repository anlegen und alle Projektdateien hochladen (inklusive `.github/workflows/daily-news.yml`).
2. In Vercel auf **Add New → Project** gehen und das GitHub-Repository importieren. Framework **Other**, kein Build-Befehl, Root-Verzeichnis `./`.
3. Deploy klicken. Die angezeigte Vercel-URL lässt sich teilen. Ohne Supabase läuft weiterhin der Demo-Modus.

## Supabase: gemeinsamer Newsfeed

1. Ein Supabase-Projekt anlegen.
2. Den Inhalt von `supabase.sql` im SQL Editor ausführen.
3. In `config.js` die Projekt-URL und den **Publishable Key** (`sb_publishable_...`) hinterlegen. Dieser Key darf öffentlich sein. **Niemals Secret Keys in `config.js` eintragen!**
4. Änderungen ins GitHub-Repository übertragen. Vercel deployt die aktualisierte Seite.
5. Danach erscheint zunächst eine leere Live-Ansicht, bis Meldungen importiert wurden.

## Tägliche automatische Recherche per GitHub Actions

1. Im GitHub-Repository unter **Settings → Secrets and variables → Actions** zwei Repository-Secrets anlegen:
   - `SUPABASE_URL`: Projekt-URL aus Supabase
   - `SUPABASE_SECRET_KEY`: Supabase Secret Key (`sb_secret_...`) aus dem Supabase-Dashboard
2. In GitHub **Actions → Daily news import → Run workflow** ausführen, um den ersten Import manuell zu starten.
3. Danach läuft der Workflow täglich auf GitHub Actions, ungefähr 06:15 UTC (GitHub-Zeitpläne können verzögert starten oder bei inaktiven öffentlichen Repositories deaktiviert werden).
4. Der Import fragt Google-News-RSS nach Hersteller- und Branchenthemen der vergangenen sieben Tage ab. Er importiert Titel, Quelle, Datum und Link. Die Kurzbeschreibung ist zunächst ein redaktioneller Hinweis, keine KI-Zusammenfassung.

**Wichtig:** Das Import-Skript greift weder direkt auf LinkedIn noch auf Instagram zu. Die Social-Media-Links sind im Quellenverzeichnis hinterlegt, aber es gibt keinen automatischen Social-Media-Abruf. Google News kann Treffer auslassen oder zu falsch zugeordneten Artikeln führen. Vor Veröffentlichungen Titel, Datum, Quelle und Herstellerbezug prüfen.

## Datenschutz / Zugriff

Dieses MVP nutzt eine **öffentlich lesbare Supabase-Tabelle**. Wer die Website-Adresse hat, kann die importierten Nachrichten sehen, unabhängig von einem Sony-Login. Daher ausschließlich **öffentliche Nachrichten** importieren. Keine internen Vertragsdaten, vertraulichen Preislisten oder personenbezogenen Informationen hinterlegen. Für einen echten internen Sony-Music-Betrieb empfiehlt sich vor Produktivsetzung SSO/Login mit Row Level Security sowie eine Prüfung durch die interne IT/Datenschutzabteilung.

Die Merkliste ist **lokal pro Browser** gespeichert, nicht teamweit synchronisiert. Per CSV können Themen an Kolleg:innen weitergegeben werden.

## Entwicklungspfade

- Redaktionelle KI-Zusammenfassungen über einen geschützten Server-Endpunkt ergänzen.
- Separates Monitoring offizieller Hersteller-Newsrooms via RSS oder erlaubte APIs.
- Login, teamweite Merklisten, Review-Status, Archiv, Benachrichtigungen.
- Echte Supabase-Quellentabelle, um URLs und Suchbegriffe ohne Code-Änderung zu pflegen.

## Dateien

- `index.html`, `styles.css`, `app.js`: Oberfläche
- `config.js`: öffentliche Supabase-Konfiguration
- `supabase.sql`: Datenbankschema und Leserechte
- `scripts/collect.py`: täglicher RSS-Import
- `.github/workflows/daily-news.yml`: automatischer GitHub-Zeitplan
