document.querySelectorAll(
    '.fancybox-overlay.fancybox-overlay-fixed' // <-- Pull your page’s identifiers here. If there's more than one thing to target you can comma seperate them.
  ).forEach(el => el.style.display = 'none')
