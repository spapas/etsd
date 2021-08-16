// Careful. This returns a Promise. Proper usage is:

// loadPrivateKey(...).then(
//    privateKey => console.log(privateKey) // RESOVE
//    ,
//    reason => console.log(reason) // REJECT
//).catch(
//    err => console.log(err)
//)

const gtools = {}

gtools.loadPrivateKey = (async(privateKeyArmored, passphrase) => {
    let privateKey = await openpgp.decryptKey({
      privateKey: await openpgp.readPrivateKey({ armoredKey: privateKeyArmored }),
      passphrase
    });
    return privateKey
})

gtools.loadPrivateKeyLocal = async () => gtools.loadPrivateKey(
    localStorage['privateKeyArmored'],localStorage['privateKeyPassphrase'] 
)

gtools.enableTooltips = () => {
    let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))      
    let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
}

gtools.loadPublicKey = (async(key_data) => {
    let publicKey = await openpgp.readKey({
        armoredKey: key_data
    });
    return publicKey
    
})

gtools.generateKeyPair = (async (name, email, passphrase) => {
    const date = new Date().toISOString()
    console.log(name, email)
    const { privateKey, publicKey, revocationCertificate } = await openpgp.generateKey({
        type: 'ecc', 
        curve: 'curve25519', 
        userIDs: [{ name, email, comment: "ETSD Generated Key, " + date }], 
        passphrase, 
        format: 'armored' 
    });

    return {
        privateKey,
        publicKey
    }
})

gtools.downloadBlob = (blob, filename) => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'download';
    const clickHandler = () => {
        setTimeout(() => {
        URL.revokeObjectURL(url);
        this.removeEventListener('click', clickHandler);
        }, 150);
    };
    a.addEventListener('click', clickHandler, false);
    a.click();
    return a;
}

gtools.downloadKey = (keyString, filename) => gtools.downloadBlob(new Blob([keyString], {type :'application/pgp-keys'}), filename)

gtools.jqDisable = (sel) => $(sel).prop({'disabled': true})
gtools.jqEnable = (sel) => $(sel).prop({'disabled': false})

gtools.displayTimer = logoutUrl => {
    let timeleft = 15*60;
    let downloadTimer = setInterval(() => {
      //console.log(timeleft)
      timeleft--;
      let s = String(timeleft % 60).padStart(2, '0');
      let m = String(Math.floor(timeleft / 60)).padStart(2, '0');
      document.getElementById("countdowntimer").textContent = `${m}:${s}`;
      if(timeleft <= 0) {
          clearInterval(downloadTimer);
          //console.log("TIME OVER")
          window.location.href = logoutUrl
      }
    }, 1000);
}

gtools.signAndVerify = async (publicKey, privateKey) => {

    const unsignedMessage = await openpgp.createCleartextMessage({ text: 'Hello, World!' });
    const cleartextMessage = await openpgp.sign({
        message: unsignedMessage,
        signingKeys: privateKey
    });
    
    const signedMessage = await openpgp.readCleartextMessage({
        cleartextMessage
    });
    const verificationResult = await openpgp.verify({
        message: signedMessage,
        verificationKeys: publicKey
    });
    const { verified, keyID } = verificationResult.signatures[0];
    return verified
    try {
        await verified; // throws on invalid signature
    } catch (e) {
        throw new Error('Signature could not be verified: ' + e.message);
    }
}

gtools.encrypt = async (publicKey, binMessage) => {
    // The binMessage is an ArrayBuffer so it needs to be converte toan Uint8Array
    const encrypted = await openpgp.encrypt({
        message: await openpgp.createMessage({ binary: new Uint8Array(binMessage) }), 
        encryptionKeys: publicKey
    })
    return encrypted
}

gtools.decrypt = async(privateKey, encrypted) => {
    const message = await openpgp.readMessage({
        armoredMessage: encrypted 
    });
    // Use the binary format to return an Uint8Array
    const { data: decrypted } = await openpgp.decrypt({
        message,
        format: 'binary',
        decryptionKeys: privateKey
    });
    return decrypted
}