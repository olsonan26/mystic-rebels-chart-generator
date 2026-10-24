JSON.stringify({
  title: document.title,
  viewportWidth: innerWidth,
  documentWidth: document.documentElement.scrollWidth,
  reducedMotion: matchMedia('(prefers-reduced-motion: reduce)').matches,
  orbOutsideWheel: !document.querySelector('#chart-wheel .plasma-orb'),
  animationCount: document.querySelector('.plasma-orb').getAnimations({subtree:true}).length,
  animations: document.querySelector('.plasma-orb').getAnimations({subtree:true}).map(a=>({
    name: a.animationName,
    state: a.playState,
    duration: a.effect.getTiming().duration,
    infinite: a.effect.getTiming().iterations===Infinity,
    keyframeProperties: [...new Set(a.effect.getKeyframes().flatMap(k=>Object.keys(k)).filter(k=>!['offset','computedOffset','easing','composite'].includes(k)))]
  })),
  pauseButtonLabel: document.querySelector('.plasma-motion-toggle').getAttribute('aria-label'),
  pauseButtonHidden: getComputedStyle(document.querySelector('.plasma-motion-toggle')).display==='none',
  chartMarkers: document.querySelectorAll('[data-object-id]').length,
  chartRows: document.querySelectorAll('[data-table-object]').length
})
