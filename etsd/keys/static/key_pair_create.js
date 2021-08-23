
const validatePassphrase = (passphrase) => {
  // Check if passphrase contains a lower case character, an uppercase character a number and a symbol
  const lowerCase = /[a-z]/g;
  const upperCase = /[A-Z]/g;
  const number = /[0-9]/g;
  const symbol = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/g;
  const passphraseLength = passphrase.length;
  
  if (passphrase.match(lowerCase) && passphrase.match(upperCase) && passphrase.match(number) && passphrase.match(symbol)) {
    return true;
  }
  return false 
}

$(function() { 
  $('#passphraseLength').html(passphraseLength)
  $('#generateButton').click(function() { 
    
    const passphrase = $('#passphrase').val()
    const passphraseConfirm = $('#passphraseConfirm').val()
    if(!passphrase) {
      bootstrap5Alert({'message': gettext("Please enter a passphrase"), 'title': gettext("ERROR")})
      return 
    }
    if (passphrase.length < passphraseLength) {
      bootstrap5Alert({'message': gettext('Minimum passphrase length: ' ) + passphraseLength, 'title': gettext("ERROR")})
      return 
    }
    if (!validatePassphrase(passphrase)) {
      bootstrap5Alert({'message': gettext('Please make sure that the passphrase contains at least a lower case character, an upercase character a number and a symbol!'), 'title': gettext("ERROR")})
      return 
    }

    if(passphrase!=passphraseConfirm) {
      bootstrap5Alert({'message': gettext("The confirm passphrase is not the same with the passphrase"), 'title': gettext("ERROR")})
      return 
    }
    
    
    gtools.generateKeyPair(authority, authority_email, passphrase).then(
      ({ privateKey, publicKey }) => {
      $('#id_key').val(publicKey)
      $('#downloadButton').unbind( "click" );
      $('#downloadButton').click( event => {
        event.preventDefault();
        gtools.downloadKey(privateKey, "private.asc")
        gtools.jqEnable('#submitButton')
        gtools.jqDisable('#generateButton')
      })
      gtools.jqEnable('#downloadButton')
      
      gtools.loadPublicKey(publicKey).then(
        publicKey => {
          //window.publicKey = publicKey
          //console.log("OK", publicKey)
          const user_id = publicKey.getUserIDs().join(',')
          const fingerprint = publicKey.getFingerprint()
          $('#id_user_id').val(user_id)
          $('#id_fingerprint').val(fingerprint)

        }
      ).catch(err => {
        console.log(err)
      })
      
    }).catch(err => {
        console.log(err)
    })
  })

  confirmFormAction({
    'sel': '#keyform',
    'title': gettext('Warning'),
    'message': gettext(`Are you sure you want to continue?<br />
    Please make sure that:
    <ul>
      <li>You remember the private key encryption passphrase</li>
      <li>You have saved the private key in a safe place</li>
    </ul>
    <b>If you lose access to your private key or its encryption password
    you won't be able to use it anymore and you'll need to create a new one!</b>`),
  })
})