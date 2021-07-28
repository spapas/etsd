const makeId = length => {
  var result = ''
  var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
  var charactersLength = characters.length
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength))
  }
  return result
}

const bootstrap5Alert = ({ message, title, cb }) => {
  let modalId = makeId(12)

  let hmodal = `<div class="modal" tabindex="-1" id=${modalId}>
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">${title ? title : 'Modal dialog'}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>${message}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          ${cb ? `<button id=${modalId + 'ok'} type="button" class="btn btn-danger"  >Delete!</button>`: ''}
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
      cb: () => {
        console.log("Submit form");
        evt.target.closest('form').submit();
      }
    })
  })
})
    
