/*
   On submiting the form, send the POST ajax
   request to server and after successfull submission
   display the object.
*/

$(".ajax-form").submit(function (e) {
    // preventing from page reload and default actions
    e.preventDefault();
    // serialize the data for sending the form data.
    let serializedData = $(this).serialize();
    let _url = $(this).attr('action');
    $.ajax({
        type: 'POST',
        url: _url,
        data: serializedData,
        success: function (response) {
            $(this).trigger('reset');
            $('#ajax-form-modal').modal('hide');
            successFormSubmit(response);
        },
        error: function (response) {
            // alert the error if any error
            console.log(response);
        }
    })
})