const messageData = JSON.parse(document.getElementById('message-data').textContent);
const cipherData = JSON.parse(document.getElementById('authority-cipher-data').textContent);

if(privateKeyFingerprint) {
  gtools.loadPrivateKeyLocal().then(
    privateKey=>{
      console.log("Private key loaded!")
      window.privateKey=privateKey
    }
  )
}


const decryptAndDownload = (cipher_id, data_ext) => {
  console.log("OK DOWNLOAD ", cipher_id, data_ext)
  $(`#downloaButton_${cipher_id}`).prop('disabled', true);
  const url = `${cipherDataFileUrl}${cipher_id}/`
  // Download the cipher
  $.ajax({
    url, 
    success: data => {
      // And decrypt it using the loaded private key
      gtools.decrypt(privateKey, data).then(
        decrypted => {
          // After it's been decrypted just download it with the downloadBlob
          gtools.downloadBlob(new Blob([decrypted]), cipher_id+'.'+data_ext)
          $(`#downloaButton_${cipher_id}`).prop('disabled', false);
        }
        ,
        reason => console.log(reason) // No error handling for now
      ).catch(
        err => console.log(err) // No error handling for now
      )
    },
    cache: false
  })
  return false
}

const deleteCipherData = (cipher_id) => {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
  const cb = () => {
    const url = `${cipherDataDeleteUrl}${cipher_id}/`
    $.ajax({
      url, 
      method: 'POST',
      headers: {'X-CSRFToken': csrftoken},
      success: data => {
        location.reload();
      },
      error: function (xhr, ajaxOptions, thrownError) {
        if(xhr.status == 403) {
          bootstrap5Alert({
            'message': gettext("You cannot delete this file. Please make sure that you have read all the message files first."), 
            'title': gettext("ERROR")
          })
        }
      },
      cache: false
    })
  }
  bootstrap5Alert({
    'message': gettext("Are you sure you want to delete this file?"), 
    'title': gettext("Confirm"), 
    'actionText': gettext("Delete"), 
    'cb': cb
  })
  return false 
}

$(function() {
  if(messageData.length > 0) {
    const cipherDataContent = messageData.map(md => {
      let cd = cipherData.find(cd => cd.data_id == md.data_id)
      
      let html = `<tr>
        <td title='Data id: ${md.data_id}'>${md.number}</td>
        <td>${md.ext}</td>
        <td>${cd?cd.authority_name:"-"}</td>
        <td>${
          cd?
          (cd.fingerprint==privateKeyFingerprint
          ?`<button id='downloaButton_${cd.id}' class='btn btn-warning btn-sm' onclick='return decryptAndDownload(${cd.id}, "${cd.ext}")'>
              ${gettext('Decrypt and download')}
            </button>`
          :`<span class='text-danger'>
              ${gettext('Not possible to decrypt. Please make sure you have loaded the proper private key')}
            </span>`
          ):`<span class='text-danger'>${gettext('Cipher data not available')}</span>`
        }</td>
        <td>
          ${cd?`<a onclick='return deleteCipherData(${cd.id})' class='btn btn-danger' href='#'>${gettext('Delete')}</a>`:'-'}
        </td>
      </tr>`
      return html
    }).join('')

    const cipherDataContentAll = messageData.filter(md => {
      let cd = cipherData.find(cd => cd.data_id == md.data_id)
      return cd.fingerprint==privateKeyFingerprint
    }).map(md => {
      let cd = cipherData.find(cd => cd.data_id == md.data_id)
      return `${cd.id}:${cd.ext}`
    }).join(',')

    //console.log(cipherDataContentAll)
    let cipherDataContentFooter =''
    if(cipherDataContentAll.length > 0 ) {
      cipherDataContentFooter += `<tr>
        <td colspan='3'>
        <td>
          <button id='downloaAllButton' class='btn btn-warning btn-sm' onclick='return decryptAndDownloadAll("${cipherDataContentAll}")'>
            ${gettext('Decrypt and download all')}
          </button>
        </td>
        <td></td>
      </tr>`
    }
    
    $('#cipher-data-container').html(cipherDataContent + cipherDataContentFooter)
  }

  confirmFormAction({
    sel: '#sendForm', 
    message: gettext('Are you sure you want to send the message?'), 
    title: gettext('Send message'),
    color: 'success'
  })
  confirmDelete('#deleteForm')

})

const decryptAndDownloadPromise = (cipher_id, data_ext) => {
  return new Promise((resolve, reject) => {
    //console.log("OK DOWNLOAD ", cipher_id, data_ext)
    const url = `${cipherDataFileUrl}${cipher_id}/`
    // Download the cipher
    $.ajax({
      url, 
      success: data => {
        // And decrypt it using the loaded private key
        gtools.decrypt(privateKey, data).then(
          decrypted => {
            // After it's been decrypted just download it with the downloadBlob
            //gtools.downloadBlob(new Blob([decrypted]), cipher_id+'.'+data_ext)
            resolve({
              blob: new Blob([decrypted]),
              name: cipher_id+'.'+data_ext
            })
          }
          ,
          reason => {
            console.log(reason) // No error handling for now
            reject(reason)
          }
        ).catch(
          err => {
            console.log(err) // No error handling for now
            reject(reason)
          }
        )
      },
      cache: false
    })
    return false
  })
}

const decryptAndDownloadAll = (data) => {
  $('#downloaAllButton').prop('disabled', true);
  const data_ok = data.split(',').map(z => { let [a,b] = z.split(':') ; return {id: a, ext: b }} )

  let promises = data_ok.map(z => decryptAndDownloadPromise(z.id, z.ext))
  Promise.all(promises).then(values => {
    
    const zip = JSZip()
    values.forEach(z => {
      zip.file(z.name, z.blob)
    })
    
    zip.generateAsync({type:"blob"}).then(function (blob) { 
      $('#downloaAllButton').prop('disabled', false);
      gtools.downloadBlob(blob, 'data.zip')
    }, function (err) {
      $('#downloaAllButton').prop('disabled', false);
      console.log("ERRORS", err)
    });
  });
  
  return false
  
}