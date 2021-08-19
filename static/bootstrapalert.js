const makeId = length => {
  var result = ''
  var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  var charactersLength = characters.length
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength))
  }
  return result
}

if (typeof variable === 'undefined') {
  const gettext = (str) => str
}

const dangerIcon = `<b>
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-x-octagon-fill flex-shrink-0 me-2" viewBox="0 0 16 16">
    <path d="M11.46.146A.5.5 0 0 0 11.107 0H4.893a.5.5 0 0 0-.353.146L.146 4.54A.5.5 0 0 0 0 4.893v6.214a.5.5 0 0 0 .146.353l4.394 4.394a.5.5 0 0 0 .353.146h6.214a.5.5 0 0 0 .353-.146l4.394-4.394a.5.5 0 0 0 .146-.353V4.893a.5.5 0 0 0-.146-.353L11.46.146zm-6.106 4.5L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 1 1 .708-.708z"/>
  </svg>
</b>`

const infoIcon = `<b>
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-info-circle-fill flex-shrink-0 me-2" viewBox="0 0 16 16">
    <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
  </svg>
</b>`

const successIcon = `<b>
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-check-circle-fill flex-shrink-0 me-2" viewBox="0 0 16 16">
    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
  </svg>
</b>`

const warningIcon = `<b>
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2" viewBox="0 0 16 16">
    <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
  </svg>
</b>`


const bootstrap5Alert = ({ message, title, actionText, cb, color }) => {
  let modalId = makeId(12)
  icon = dangerIcon
  if(color === undefined) {
    color = 'danger';

  } else if(color === 'info') {
    icon = infoIcon
  } else if(color === 'success') {
    icon = successIcon
  } else if(color === 'warning') {
    icon = warningIcon
  }

  let hmodal = `<div class="modal" tabindex="-1" id=${modalId}>
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
        ${'<h5 class="modal-title text-'+color+'">'}
            ${title ? title : 'Alert'}
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="alert alert-${color} d-flex align-items-center" role="alert">
          ${icon} 
          <div>
            ${message}
          </div>
        </div>
        
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">${gettext('Close')}</button>
          ${cb ? `<button id='${modalId + 'ok'}' type="button" class=${'"btn btn-'+color+'"'} >${actionText}</button>`: ''}
        </div>
      </div>
    </div>
  </div>`

  let element = document.createElement('div')
  document.body.appendChild(element)
  element.innerHTML = hmodal

  let myModal = new bootstrap.Modal(document.getElementById(modalId), {
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
        evt.target.closest('form').submit();
      }
    })
    return false
  })
})

const confirmFormAction = ({sel, message, title, color}) => document.querySelectorAll(sel).forEach(el => {
  el.addEventListener('submit', (evt) => {
    evt.preventDefault();
    bootstrap5Alert({
      message,
      title,
      color,
      actionText: gettext('Yes'),
      cb: () => {
        evt.target.closest('form').submit();
      }
    })
    return false
  })
})