"""Validate local references and public copy without third-party dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from build_site import PROJECTS, ROOT, GAMEPLAY

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.text, self.ids = [], [], []
        self.headings = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.headings += tag == 'h1'
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for key in ('src', 'href', 'poster', 'data-game-src'):
            if attrs.get(key):
                self.refs.append(attrs[key])
    def handle_data(self, data):
        self.text.append(data)

if __name__ == '__main__':
    pages = {}
    for name in ['index.html'] + [p['slug']+'.html' for p in PROJECTS]:
        page = Page()
        page.feed((ROOT/name).read_text(encoding='utf-8'))
        pages[name] = page
    for name,page in pages.items():
        if name != 'index.html':
            source = (ROOT/name).read_text(encoding='utf-8')
            slug = name.removesuffix('.html')
            assert slug in GAMEPLAY and len(GAMEPLAY[slug][1]) == 3
            assert source.index('id="gameplay"') < source.index('id="section-1"'), (name, 'missing gameplay introduction')
        if name == 'memorizer.html':
            assert 'assets/portfolio/memorizer-purple-star.png' in page.refs
            assert 'assets/portfolio/page-15-12.webp' not in page.refs
        if name == '1000-action.html':
            assert 'https://itch.io/embed-upload/16338738?color=0a0a0a' in page.refs
            assert 'html-classic.itch.zone' not in source, 'Use the official embed, not a hotlinked game file'
        assert page.headings == 1, (name, 'heading')
        assert len(page.ids) == len(set(page.ids)), (name, 'duplicate ID')
        for term in ('笔试', '测试题', 'Cellphone', 'Address:', '封面图接口'):
            assert term not in ''.join(page.text), (name, term)
        for ref in page.refs:
            url = urlsplit(ref)
            if url.scheme:
                continue
            target = unquote(url.path) or name
            assert not target.startswith('资料/'), (name, ref)
            assert (ROOT/target).is_file(), (name, ref)
            if url.fragment and target in pages:
                assert url.fragment in pages[target].ids, (name, ref)
        print(name, 'OK')
    print('All seven public pages passed.')
