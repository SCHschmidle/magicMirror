# Magic Mirror

Ein einfaches Projekt für einen "Magic Mirror" mit Bild-Upload und -Anzeige. Das Frontend ist mit Vue.js gebaut, das Backend mit FastAPI.

## Features
- Hochladen von Bildern über das Dashboard.
- Anzeige aller Bilder in einer automatischen Slideshow (alle 10 Sekunden).
- Responsive Design für verschiedene Bildschirme.

## Technologien
- **Frontend**: Vue 3, Vite
- **Backend**: FastAPI, Python
- **Styling**: CSS (in Vue-Komponenten)

## Installation

### Backend
1. Gehe in den `backend` Ordner: `cd backend`
2. Installiere Abhängigkeiten: `pip install -r requirements.txt`
3. Starte den Server: `uvicorn main:app --reload` (läuft auf `http://127.0.0.1:8000`)

### Frontend
1. Gehe in den `frontend/magicmirror` Ordner: `cd frontend/magicmirror`
2. Installiere Abhängigkeiten: `npm install`
3. Starte den Dev-Server: `npm run dev` (läuft auf `http://localhost:5173`)

## Verwendung
1. Öffne das Frontend in einem Browser (z.B. `http://localhost:5173`).
2. Gehe zum Dashboard, um Bilder hochzuladen.
3. Gehe zur Display-View, um die Slideshow zu sehen.
4. Bilder werden in `frontend/public/images` gespeichert und von Vite serviert.

## API-Endpunkte (Backend)
- `GET /`: Dashboard-HTML (veraltet, da Vue verwendet wird).
- `POST /upload/single`: Einzelnes Bild hochladen (JSON-Antwort).
- `GET /display`: Liste aller Bilder (JSON für Vue).

## Entwicklung
- Backend: Ändere Code in `backend/routes/dashboard.py`.
- Frontend: Ändere Vue-Komponenten in `frontend/src/`.
- Für Produktion: Baue das Frontend mit `npm run build` und serviere es statisch.

## Lizenz
Dieses Projekt ist Open-Source. Verwende es frei, aber auf eigene Gefahr.