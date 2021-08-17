const makeId = length => {
  var result = ''
  var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  var charactersLength = characters.length
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength))
  }
  return result
}


const bootstrap5Alert = ({ message, title, actionText, cb, color }) => {
  let modalId = makeId(12)
  let icon = `<b>
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-square" viewBox="0 0 16 16">
    <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>
    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
  </svg>
  </b>`
  if(color === undefined) {
    color = 'danger';
  }
  if(color === 'success') {
    icon = `<b>
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-square" viewBox="0 0 16 16">
      <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>
      <path d="M10.97 4.97a.75.75 0 0 1 1.071 1.05l-3.992 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.235.235 0 0 1 .02-.022z"/>
    </svg>
    </b>`
  }
  if(color === 'warning') {
    icon = `<b>
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-square" viewBox="0 0 16 16">
      <path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>
      <path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/>
    </svg>
    </b>`
  }

  let hmodal = `<div class="modal" tabindex="-1" id=${modalId}>
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
        ${'<h5 class="modal-title text-'+color+'">'}
            ${icon}
            ${title ? title : 'Alert'}
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
        
        <p>${message}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          ${cb ? `<button id='${modalId + 'ok'}' type="button" class=${'"btn btn-'+color+'"'} >${actionText}</button>`: ''}
        </div>
      </div>
    </div>
  </div>`

  let element = document.createElement('div')
  document.body.appendChild(element)
  element.innerHTML = hmodal

  var myModal = new bootstrap.Modal(document.getElementById(modalId), {
    backdrop: 'static',
  })
  myModal.show()
  if(cb) {
    document.getElementById(modalId + 'ok').addEventListener('click', cb)
  }
}


const confirmDelete = (cls) => document.querySelectorAll(cls).forEach(el => {
  el.addEventListener('submit', (evt) => {
    evt.preventDefault();
    bootstrap5Alert({
      message: gettext('Are you sure you want to delete this?'),
      title: gettext('Delete'),
      actionText: gettext('Delete'),
      cb: () => {
        console.log("Submit form");
        evt.target.closest('form').submit();
      }
    })
    return false
  })
})

const confirmFormAction = ({sel, message, title}) => document.querySelectorAll(sel).forEach(el => {
  el.addEventListener('submit', (evt) => {
    evt.preventDefault();
    bootstrap5Alert({
      message,
      title,
      actionText: gettext('Yes'),
      cb: () => {
        console.log("Submit form");
        evt.target.closest('form').submit();
      }
    })
    return false
  })
})