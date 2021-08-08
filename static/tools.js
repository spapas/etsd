// Careful. This returns a Promise. Proper usage is:

// loadPrivateKey(...).then(
//    privateKey => console.log(privateKey) // RESOVE
//    reason => console.log(reason) // REJECT
//).catch(
//    err => console.log(err)
//)
const loadPrivateKey = (async(privateKeyArmored, passphrase) => {
    let privateKey = await openpgp.decryptKey({
      privateKey: await openpgp.readPrivateKey({ armoredKey: privateKeyArmored }),
      passphrase
    });
    return privateKey
})

const loadPrivateKeyLocal = async () => loadPrivateKey(
    localStorage['privateKeyArmored'],localStorage['privateKeyPassphrase'] 
)

const enableTooltips = () => {
    let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))      
    let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
}