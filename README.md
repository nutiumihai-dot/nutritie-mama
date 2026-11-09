# Nutriția mea

Jurnal de mese pe telefon (PWA): calorii, proteine, fibre, vitamine și minerale, comparate cu VNR. Estimările și sfaturile le scrie Claude într-un depozit privat de date; aici e doar codul, fără date personale.

- Fără build și fără dependențe: `index.html` e toată aplicația, plus `sw.js`, `manifest.webmanifest` și iconițele (`python tools/make_icons.py .`).
- La fiecare versiune nouă: `CACHE` din `sw.js` (`nm-vNN`) și `APP_VERSION` din `index.html` cresc împreună.
