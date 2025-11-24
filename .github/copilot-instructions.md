<!-- Copilot instructions for contributors and AI coding agents -->
# Student-Dashboard — Copilot instructions

This project is a small static student dashboard (HTML/CSS/JS) with a tiny Python launcher. Use these notes to make targeted, low-risk edits and keep behavior consistent.

- **Big picture**: The app is a single-page static dashboard served from the repository root. Frontend assets live at the repository root (`index.html`, `style.css`, `images/`, `timeTable.js`, `app.js`). A Python TK launcher (`MMIS_PO.py`) opens the local `index.html` in a browser for convenience.

- **Key files**:
  - `index.html` — main HTML page; references `timeTable.js` then `app.js`.
  - `timeTable.js` — defines the timetable data arrays: `Sunday`, `Monday`, `Tuesday`, ... `Saturday`.
  - `app.js` — UI behavior: DOM wiring, theme toggling, timetable rendering, and navigation buttons (`nextDay`, `prevDay`).
  - `MMIS_PO.py` — optional Python login launcher that opens `index.html` with `webbrowser.open()`.
  - `style.css` and `images/` — styling and assets.

- **Important integration / ordering constraint**: `index.html` includes `<script src="timeTable.js"></script>` before `<script src="app.js"></script>`. `app.js` expects the day arrays (e.g. `Monday`) to exist as globals; do not change include order unless you update `app.js` to avoid reference errors.

- **Global variables & DOM expectations**:
  - `timeTable.js` exposes global arrays named `Sunday`, `Monday`, ... `Saturday`.
  - `app.js` expects DOM elements with IDs/classes: `#profile-btn`, `.theme-toggler`, `#nextDay`, `#prevDay`, `#timetable`, and a `table tbody` to populate rows.
  - Theme preference key: `localStorage` key `dark-theme` (string `'true'|'false'`).

- **Making common edits**:
  - To add/change timetable entries, edit `timeTable.js`. Each entry is an object with keys: `time`, `roomNumber`, `subject`, `type`.

```js
// example: add to Monday
Monday.push({ time: '03-04 PM', roomNumber: '12-101', subject: 'NEW101', type: 'Lab' })
```

  - To change profile/static text, update `index.html` (profile block under `aside > .profile`).
  - To change theme behavior, update `app.js` where `localStorage.getItem('dark-theme')` is read/written.

- **Run / debug workflows**:
  - Static dev: open `index.html` in a browser (double-click or `file://`), or run a simple HTTP server to avoid file-origin issues:

```powershell
# from repository root
python -m http.server 8000; Start-Process http://localhost:8000/index.html
```

  - Python launcher: run `python MMIS_PO.py` to launch the TK login window which opens `index.html` on successful login.

- **Patterns & conventions specific to this project**:
  - No build step or package manager — edits are made directly to static files.
  - Minimal JS: functionality is in `app.js` and plain arrays in `timeTable.js`; avoid introducing frameworks.
  - UI is predominately client-side state; there is no backend or API in the repo.

- **When editing JS**:
  - Keep `timeTable.js` purely data (arrays of objects). Keep `app.js` purely behavior that consumes those arrays.
  - Avoid renaming the day arrays; prefer adding new arrays or updating existing arrays in `timeTable.js`.
  - Keep global function `timeTableAll()` available (called from `index.html` inline `onclick` handlers).

- **Examples of safe changes**:
  - Fix a typo in a timetable entry or change a room number in `timeTable.js`.
  - Add an extra `div.message` to the announcements block in `index.html`.
  - Adjust theme toggling visuals in `style.css` while preserving the `dark-theme` class on `body`.

- **What to avoid / watch for**:
  - Do not reorder script tags unless you update any references that rely on globals.
  - Because there is no build/test automation, test changes by opening the site in a browser or running the HTTP server above.

If anything is unclear or you want me to expand examples or add CI / tests, tell me which area to improve.
