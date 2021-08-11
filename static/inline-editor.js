function inlineEditor(inlineSetName) {
    let tmpl = document.querySelector('#empty-form-' + inlineSetName);
    let counter = document.querySelector('[name=' + inlineSetName + '-TOTAL_FORMS]')

    document.querySelector('#add-form-' + inlineSetName).addEventListener('click', ev => {
        let newForm = tmpl.content.cloneNode(true);

        newForm.querySelectorAll('[id*=__prefix__]').forEach(el => {
            el.id = el.id.replace('__prefix__', counter.value);
            if (el.name) el.name = el.name.replace('__prefix__', counter.value);
        });

        newForm.querySelectorAll('[for*=__prefix__]').forEach(el => {
            el.htmlFor = el.htmlFor.replace('__prefix__', counter.value);
        })

        counter.value = 1 + Number(counter.value);
        document.querySelector('form #card_' + inlineSetName + ' div.row:last-of-type').insertAdjacentElement('afterend', newForm.children[0])
    })
}