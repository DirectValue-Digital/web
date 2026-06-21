# DirectValue Digital - Entwicklungs- & Deployment-Guide

Dieses Dokument beschreibt detailliert die Design-Richtlinien, die Struktur zur Erstellung neuer Web-Applikationen/Seiten sowie den Deployment-Prozess für das DirectValue-Digital-Portal. Zukünftige Entwicklungs-Agenten müssen diesem Leitfaden strikt folgen, um Konsistenz und Professionalität zu wahren.

---

## 🎨 1. Design-System & Styling-Richtlinien

Das Portal nutzt einen premium **Dark-Mode-Stil** mit Elementen aus dem **Glassmorphismus**, kombiniert mit sanften Farbverläufen und Mikro-Animationen.

### 1.1 Basiseinstellungen
- **Hintergrund**: `#050505` (tiefes Schwarz) für den Body, `#0a0a0a` für Kartenhintergründe.
- **Textfarben**:
  - Primär/Überschriften: `#ffffff`
  - Sekundär/Fließtext: `#e5e5e5`
  - Muted/Zusatztext: `#a3a3a3` oder `#737373`
- **Schriftarten (Google Fonts)**:
  - **Fließtext**: `Inter` (Standard-Sans-Schriftart)
  - **Display/Überschriften**: `Outfit` (für markante Hero-Titel)
- **Framework**: Tailwind CSS (per CDN geladen). Jede Seite deklariert ihre Konfiguration im `<head>`.

### 1.2 Farbpaletten & Akzente
Jedes Projekt erhält einen passenden Akzent-Farbton (z. B. Cyan für Flowen, Blau für Chef Log). Dieser Akzent wird verwendet für:
- Text-Gradients (`bg-gradient-to-r from-[Farbe-1] to-[Farbe-2]`)
- Glow-Effekte im Hintergrund (`radial-gradient` mit Blur)
- Fokussierte Buttons und Rahmen-Highlights

### 1.3 Key CSS-Klassen
Die folgenden Klassen definieren das visuelle Gefühl der Seite und sollten wiederverwendet werden:
```css
/* Transluzente Navigation */
.glass-nav {
    background: rgba(5, 5, 5, 0.8);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

/* Glassmorphism-Karten */
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.glass-card:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px);
}
```

---

## 📂 2. Struktur & Hinzufügen neuer Projekte

Jedes Projekt ist isoliert in einem eigenen Unterordner organisiert.

### 2.1 Verzeichnisstruktur
Ein neues Projekt wird wie folgt benannt und strukturiert:
```
06_DIRECTVALUE-DIGITAL/
├── assets/                          # Globale Assets (z.B. App-Icons, Logos)
│   └── icon_mein_projekt.png
├── XX_Mein_Projekt/                  # Projekt-Ordner (Nummerierung fortlaufend)
│   ├── index.html                   # Landingpage des Projekts
│   ├── privacy.html                 # Datenschutzerklärung der App
│   └── support.html                 # Supportseite der App (falls erforderlich)
└── index.html                       # Zentrale Landingpage (Root)
```
*Hinweis zur Nummerierung: Nutze das nächsthöhere freie Präfix (z. B. `12_Mein_Projekt`), um die Ordnung beizubehalten.*

### 2.2 Dateiinhalte eines neuen Projekts

#### 1. `index.html` (im Projektordner)
Muss dem Premium-Look entsprechen und folgende Struktur aufweisen:
- **Navbar**: Enthält das DirectValue-Digital-Logo, den Markennamen und einen deutlich sichtbaren Rücklink zum Hauptportal (`← Zurück` zu `../index.html`).
- **Hero-Bereich**:
  - Name der App als großer Display-Titel mit Gradient.
  - Das App-Icon (zentriert, stark abgerundete Ecken `rounded-3xl` oder `rounded-[2rem]`, dezenter Glow im Hintergrund).
- **Features-Bereich**: 3-Spalten- oder Grid-Layout mit `.glass-card`s.
- **Privacy/Datenschutz**: Kurze Erklärung zum Datenhandling (z.B. Offline-Fokus, lokale Datenhaltung).
- **Footer**: Urheberrechtshinweise und Links zur lokalen `privacy.html` sowie zum zentralen Impressum (`../legal/impressum.html`).

#### 2. `privacy.html` (Datenschutzerklärung)
Muss zwingend erstellt werden, falls die App im App Store veröffentlicht oder sensible Nutzerdaten verarbeitet werden.

---

## 🔗 3. Integration in das Hauptportal

Sobald das neue Projekt erstellt wurde, muss es auf der zentralen Landingpage (`index.html` im Root) verlinkt werden.

1. **Portfolio-Grid suchen**: Finde die Sektion `<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">`.
2. **Karten-HTML einfügen**: Füge ein neues Projekt-Kärtchen hinzu:
```html
<!-- Mein Projekt -->
<a href="XX_Mein_Projekt/index.html"
    class="group relative block bg-[#0a0a0a] rounded-2xl border border-neutral-800 p-8 transition-all duration-300 card-hover overflow-hidden">
    <div class="absolute top-4 right-4 bg-blue-500/10 text-blue-500 text-xs px-2 py-1 rounded-md font-medium border border-blue-500/20">
        New
    </div>
    <img src="assets/icon_mein_projekt.png" alt="Mein Projekt Icon" class="w-16 h-16 mb-6 rounded-2xl" style="clip-path: inset(1px);">
    <h3 class="text-xl font-bold text-white mb-2">Mein Projekt</h3>
    <p class="text-sm text-neutral-500 mb-4 line-clamp-2">
        Kurzbeschreibung der Anwendung in 1-2 Sätzen.
    </p>
</a>
```

---

## 🚀 4. Deployment-Prozess

Das Hosting erfolgt direkt über GitHub Pages aus dem `main`-Branch des Repositories `DirectValue-Digital/web`.

### 4.1 Git-Workflow & Synchronisation
Folge strikt diesem Ablauf bei der Veröffentlichung neuer Stände:

1. **Lokale Verifikation**:
   Öffne die geänderten Dateien lokal im Browser und teste:
   - Funktionieren alle Links (inkl. Rücklink `← Zurück`)?
   - Stimmt die Responsivität auf Mobilgeräten?
   - Werden alle Bilder/Icons korrekt geladen?

2. **Gedächtnis-Protokollierung (Level 2 & 3)**:
   Protokolliere das neue Projekt im lokalen Memory-System:
   ```bash
   python3 .antigravity/scripts/memory_manager.py log "Neues Projekt XX_Mein_Projekt hinzugefügt"
   python3 .antigravity/scripts/memory_manager.py fact "Projekt-Struktur: XX_Mein_Projekt als statisches HTML integriert"
   ```

3. **Änderungen committen & pushen**:
   Da dieses Repository ein eigenes `.git`-Verzeichnis besitzt, führe die Git-Befehle direkt im Root-Ordner aus:
   ```bash
   git add .
   git commit -m "feat: add project XX_Mein_Projekt to portfolio"
   git push origin main
   ```

4. **Veröffentlichung prüfen**:
   Nach ca. 1-2 Minuten baut GitHub Actions die Seite automatisch im Hintergrund.
   Prüfe das Deployment unter:
   - Hauptportal: `https://directvalue-digital.github.io/web/`
   - Direktlink: `https://directvalue-digital.github.io/web/XX_Mein_Projekt/index.html`
