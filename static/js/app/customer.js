let addressForm = document.querySelectorAll('.addressFildContainer')
let add = document.querySelector('#addform')
let addButton = document.querySelector(".addAddressbutton")
let totalForms = document.querySelector("#id_address-TOTAL_FORMS")
let adform = document.querySelector('.addressFildContainer')
let removeclass = document.querySelector('.remove_field')

removeclass.onclick = removeform

let formNum = addressForm.length - 1
addButton.addEventListener('click', addForm)

function addForm(e) {
    e.preventDefault()
    let newForm = addressForm[0].cloneNode(true) //Clone the address form
    let style = newForm.querySelector('.remove_field').style = 'flex'
    let formRegex = RegExp(`address-(\\d){1}-`, 'g') //Regex to find all instances of the form number
    formNum++ //Increment the form number
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `address-${formNum}-`) //Update the new form to have the correct form number
    add.insertBefore(newForm, addButton) //Insert the new form at the end of the list of forms
    totalForms.setAttribute('value', `${formNum + 1}`) //Increment the number of total forms in the management form
}


function removeform(e) {
    var li = e.target.parentElement.parentElement.remove()
    formNum--
    totalForms.setAttribute('value', `${formNum + 1}`)
}




