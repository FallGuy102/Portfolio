const viewer = document.querySelector('#image-viewer');
let opener;
if (viewer && typeof viewer.showModal === 'function') {
  const image = viewer.querySelector('img');
  const zoom = viewer.querySelector('.viewer-zoom');
  zoom.addEventListener('click', () => {
    const expanded = image.classList.toggle('native-size');
    zoom.setAttribute('aria-pressed', String(expanded));
    zoom.textContent = expanded ? '适应窗口' : '原尺寸查看';
  });
  document.querySelectorAll('[data-lightbox]').forEach(link => {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = link;
      image.src = link.href;
      image.alt = link.querySelector('img').alt;
      image.classList.remove('native-size');
      zoom.setAttribute('aria-pressed', 'false');
      zoom.textContent = '原尺寸查看';
      viewer.querySelector('p').textContent = image.alt;
      viewer.showModal();
      document.body.classList.add('viewing-image');
    });
  });
  viewer.querySelector('.viewer-close').addEventListener('click', () => viewer.close());
  viewer.addEventListener('click', event => {
    if (event.target === viewer) viewer.close();
  });
  viewer.addEventListener('close', () => {
    document.body.classList.remove('viewing-image');
    opener?.focus();
  });
}

const gameStage = document.querySelector('[data-game-src]');
if (gameStage) {
  const launch = gameStage.querySelector('.game-launch');
  const fullscreen = document.querySelector('.game-fullscreen');
  const stop = document.querySelector('.game-stop');
  const status = document.querySelector('.game-status');
  launch.addEventListener('click', () => {
    const frame = document.createElement('iframe');
    frame.title = '1000, Action! 网页版游戏';
    frame.allow = 'autoplay; fullscreen; gamepad';
    frame.allowFullscreen = true;
    frame.addEventListener('load', () => {
      status.textContent = '试玩窗口已打开，游戏资源可能仍在加载。出现画面后点击游戏区域操作；若无法运行，请前往 itch.io。';
    });
    frame.src = gameStage.dataset.gameSrc;
    launch.hidden = true;
    gameStage.append(frame);
    fullscreen.disabled = !gameStage.requestFullscreen;
    stop.hidden = false;
    status.textContent = '游戏正在从 itch.io 加载。若长时间无画面，请使用上方 itch.io 链接。';
  });
  fullscreen.addEventListener('click', async () => {
    try {
      await gameStage.requestFullscreen();
    } catch {
      status.textContent = '浏览器未允许全屏，可继续在页面中游玩或打开 itch.io。';
    }
  });
  stop.addEventListener('click', async () => {
    if (document.fullscreenElement === gameStage) await document.exitFullscreen();
    gameStage.querySelector('iframe')?.remove();
    launch.hidden = false;
    fullscreen.disabled = true;
    stop.hidden = true;
    status.textContent = '游戏已关闭；再次加载将重新开始。';
    launch.focus();
  });
}

// Content stays readable when JavaScript or observer support is unavailable.
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
if ('IntersectionObserver' in window && !reducedMotion.matches) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.animate([{ opacity: 0.45, transform: 'translateY(16px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 500, easing: 'cubic-bezier(.25,0,0,1)' });
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.work-row, .case-section').forEach(item => observer.observe(item));
}
