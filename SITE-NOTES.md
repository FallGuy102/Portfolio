# Portfolio maintenance

The site is static HTML. Open `index.html` directly, or run `python scripts/serve.py`
for a localhost preview at http://127.0.0.1:4173. The preview only serves public pages
and selected media, not the original source documents.

## Editing

- Public case-study content and shared page templates: `scripts/build_site.py`.
- Shared design tokens and responsive styles: `portfolio.css`.
- Image viewer and optional scroll animation: `portfolio.js`.
- Rebuild all seven pages: `python scripts/build_site.py`.
- Check links, anchors and public content: `python scripts/check_site.py`.
- Generated HTML works without Python or a build step on the hosting server.
- `styles.css`, `main.js` and `project.html` belong to the old prototype and are not
  used by the new pages. Do not use the old prototype as the deployment entry point.

## Media and privacy

- `assets/portfolio/page-*.webp`: extracted from the supplied portfolio PDF.
- `ice-01.webp` to `ice-06.webp`: original-resolution lossless exports from the level
  design document (up to 5216 pixels wide). The image viewer supports native-size zoom.
- `ice-cover.webp`: 2560x1440 frame from the original video, encoded at high quality.
- `action-*.png`: https://zzoonng.itch.io/1000action
- `peng-*.png`: https://scariett77.itch.io/peng-win
- Primary demo: https://www.youtube.com/watch?v=bwX1CtxmgSg embedded with the
  privacy-enhanced player, fullscreen support and strict-origin-when-cross-origin.
- `beneath-the-ice.mp4`: complete 09:40 demo, 720p H.264/AAC, about 56 MB, retained
  as a collapsed fallback when YouTube is unavailable. Use HTTP localhost preview
  instead of file:// when checking the YouTube embed.
- Original PDF, DOCX and game builds in `资料/` are private local inputs and ignored
  by Git. Only the public email is included; no original resume download is exposed.
- `.gitignore` is not a hosting access-control mechanism. Deploy only the seven
  current HTML pages, `portfolio.css`, `portfolio.js` and `assets/portfolio/`.
- GameJam roles and awards follow the supplied resume. Peng-Win's date follows the
  December 2025 dates and public Xmas Game Jam 2025 project listing.
- The video was visually spot-checked, not transcribed end to end. Review its
  complete audio and burned-in subtitles before public release.
