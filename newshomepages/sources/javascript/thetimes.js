document.querySelectorAll(
  '.message-container'
).forEach(el => el.remove())

document.querySelectorAll(
  '.type-modal,#ad-header,.Tooltip,#sticky-ad-header'
).forEach(el => el.style.display = 'none')
