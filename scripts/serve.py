"""Local preview exposing only public website assets, never private source material."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlsplit
import os

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = {'index.html', 'memorizer.html', 'beneath-the-ice.html', 'lost-realm.html',
          'divine-deception.html', '1000-action.html', 'peng-win.html', 'portfolio.css', 'portfolio.js'}

class PublicHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        path = unquote(urlsplit(self.path).path).lstrip('/') or 'index.html'
        resolved = (ROOT / path).resolve()
        if not resolved.is_relative_to(ROOT) or not (path in PUBLIC or path.startswith('assets/portfolio/')) or not resolved.is_file():
            self.send_error(404)
            return None
        return super().send_head()

if __name__ == '__main__':
    os.chdir(ROOT)
    print('Preview: http://127.0.0.1:4173', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 4173), PublicHandler).serve_forever()
