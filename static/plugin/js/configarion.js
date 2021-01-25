var input = document.querySelector("#phoneInput"),
  errorMsg = document.querySelector("#error-msg"),
  validMsg = document.querySelector("#valid-msg");

// here, the index maps to the error code returned from getValidationError - see readme
var errorMap = ["Please Enter Valid Phone Number", "Invalid country code", "Phone Number Is Very Short", "Phone Number Is Very Logn", "Invalid Phone Number"];

// initialise plugin
var iti = window.intlTelInput(input, {
  //   utilsScript: "../../build/js/utils.js?1603274336113"

  separateDialCode: true,
  hiddenInput: "countryResult",

  utilsScript: "//cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.3/js/utils.js",
});

var reset = function () {
  input.classList.remove("error");
  errorMsg.innerHTML = "";
  errorMsg.classList.add("hide");
  validMsg.classList.add("hide");
};

input.addEventListener('keyup', function () {
  console.log('1');
  if (input.value.trim()) {
    if (iti.isValidNumber()) {
      input.classList.add("validNumber");
      validMsg.classList.remove("hide");
      errorMsg.classList.add("hide");
      $('#addCustomerForm').attr('onsubmit', 'return true;');
      var number = iti.getNumber();
      $('#phoneValue').val(number);
      var numberType = iti.getNumberType();
      console.log(numberType);
    } else {
      input.classList.remove("validNumber");
      input.classList.add("error");
      var errorCode = iti.getValidationError();
      errorMsg.innerHTML = errorMap[errorCode];
      errorMsg.classList.remove("hide");
      validMsg.classList.add("hide");
      $('#addCustomerForm').attr('onsubmit', 'return false;');
    }
  }
});



input.addEventListener("countrychange", function () {
  var countryData = iti.getSelectedCountryData();
  var countryCodeNew = countryData.dialCode;
  var newCode = "+" + countryCodeNew;
  // alert(newCode);
  $('#phoneInput').val(newCode);
});