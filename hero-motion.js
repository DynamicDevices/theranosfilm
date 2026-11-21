/* Decorative motion only: all research and headings remain ordinary HTML. */
'use strict';
function createHeroMotion(video, poster, button, preference, doc, connection, observe) {
  let paused = false, visible = true, failed = false, optedIn = false, loaded = false;
  let revision = 0;
  const enabled = () => optedIn || (!preference.matches && !connection?.saveData);
  const canRun = () => enabled() && !paused && visible && !doc.hidden && !failed;
  const label = () => { button.textContent = canRun() ? 'Pause background video' : 'Play background video'; };
  function still() { video.hidden = true; poster.hidden = false; }
  function sync() {
    const current = ++revision;
    label();
    if (!canRun()) { video.pause(); if (!enabled() || failed) still(); return; }
    if (!loaded) { video.src = video.dataset.src; loaded = true; }
    try {
      const attempt = video.play();
      if (attempt?.catch) attempt.catch(() => {
        if (current !== revision) return;
        paused = true; still(); label();
      });
    } catch { paused = true; still(); label(); }
  }
  button.hidden = false;
  button.addEventListener('click', () => {
    if (failed) return;
    if (!enabled()) { optedIn = true; paused = false; }
    else paused = !paused;
    sync();
  });
  video.addEventListener('playing', () => {
    if (canRun()) { video.hidden = false; poster.hidden = true; }
    else video.pause();
  });
  video.addEventListener('error', () => {
    failed = true; still(); button.hidden = true; video.pause();
  });
  preference.addEventListener('change', () => { optedIn = false; sync(); });
  doc.addEventListener('visibilitychange', sync);
  const observer = observe(entries => {
    visible = entries.some(entry => entry.isIntersecting);
    sync();
  });
  observer?.observe(video.parentElement);
  sync();
  return {sync};
}
if (typeof module !== 'undefined' && module.exports) module.exports = {createHeroMotion};
if (typeof document !== 'undefined') {
  const video = document.querySelector('#hero-video');
  if (video && window.matchMedia) createHeroMotion(video,
    document.querySelector('#hero-poster'), document.querySelector('#hero-video-toggle'),
    window.matchMedia('(prefers-reduced-motion: reduce)'), document, navigator.connection,
    callback => typeof IntersectionObserver === 'undefined' ? null : new IntersectionObserver(callback));
}
