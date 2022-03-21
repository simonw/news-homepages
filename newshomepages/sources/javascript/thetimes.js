const style = document.createElement('style')
style.innerHTML = `
#sp_message_container_523772 {
  display:none!important
}

#ad-news {
  display:none!important
}

react-edition-personalised-article-rail {
  display: none!important
}`

document.head.appendChild(style)

document.querySelectorAll(
  '.type-modal,#ad-header,.Tooltip,#sticky-ad-header'
).forEach(el => el.style.display = 'none')
