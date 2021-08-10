const makeId = length => {
  var result = ''
  var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  var charactersLength = characters.length
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength))
  }
  return result
}

const bootstrap5Alert = ({ message, title, actionText, cb }) => {
  let modalId = makeId(12)

  let hmodal = `<div class="modal" tabindex="-1" id=${modalId}>
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title text-danger">
          <b>
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-x-octagon" viewBox="0 0 16 16">
              <path d="M4.54.146A.5.5 0 0 1 4.893 0h6.214a.5.5 0 0 1 .353.146l4.394 4.394a.5.5 0 0 1 .146.353v6.214a.5.5 0 0 1-.146.353l-4.394 4.394a.5.5 0 0 1-.353.146H4.893a.5.5 0 0 1-.353-.146L.146 11.46A.5.5 0 0 1 0 11.107V4.893a.5.5 0 0 1 .146-.353L4.54.146zM5.1 1 1 5.1v5.8L5.1 15h5.8l4.1-4.1V5.1L10.9 1H5.1z"/>
              <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
            </svg>  
          </b>
            ${title ? title : 'Alert'}
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">

        
        <p>${message}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          ${cb ? `<button id=${modalId + 'ok'} type="button" class="btn btn-danger"  >${actionText}</button>`: ''}
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
      message: 'Are you sure you want to delete this?',
      title: 'Delete',
      actionText: 'Delete',
      cb: () => {
        console.log("Submit form");
        evt.target.closest('form').submit();
      }
    })
  })
})

const confirmFormAction = ({sel, message, title}) => document.querySelectorAll(sel).forEach(el => {
  console.log("Z", el)
  el.addEventListener('submit', (evt) => {
    evt.preventDefault();
    bootstrap5Alert({
      message,
      title,
      actionText: 'Yes',
      cb: () => {
        console.log("Submit form");
        evt.target.closest('form').submit();
      }
    })
  })
})
