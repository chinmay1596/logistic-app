function ajaxLoaderStart(text) {
    if (jQuery('body').find('#resultLoading').attr('id') != 'resultLoading') {
        jQuery('body').append('<div id="resultLoading" style="display:none"><div><img src="/assets/images/ajax-loader.gif"><div>' + text + '</div></div><div class="bg"></div></div>');
    }

    jQuery('#resultLoading').css({
        'width': '100%',
        'height': '100%',
        'position': 'fixed',
        'z-index': '1500',
        'top': '0',
        'left': '0',
        'right': '0',
        'bottom': '0',
        'margin': 'auto'
    });

    jQuery('#resultLoading .bg').css({
        'background': '#000000',
        'opacity': '0.7',
        'width': '100%',
        'height': '100%',
        'position': 'absolute',
        'top': '0'
    });

    jQuery('#resultLoading>div:first').css({
        'width': '250px',
        'height': '75px',
        'text-align': 'center',
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'right': '0',
        'bottom': '0',
        'margin': 'auto',
        'font-size': '16px',
        'z-index': '10',
        'color': '#ffffff'

    });

    jQuery('#resultLoading .bg').height('100%');
    jQuery('#resultLoading').fadeIn(300);
    jQuery('body').css('cursor', 'wait');
}

function ajaxLoaderStop() {
    jQuery('#resultLoading .bg').height('100%');
    jQuery('#resultLoading').fadeOut(300);
    jQuery('body').css('cursor', 'default');
}



$(document).ready(function() {
    $('ul.main-menu li a').each(function() {
        if ($($(this))[0].href == String(window.location.pathname)) {
            $(this).parent().addClass('active');


        }
    });

    $('ul.main-menu li ul li a').each(function() {
        if ($($(this))[0].pathname == String(window.location.pathname)) {
            // $(this).parent().addClass('active');


            $(this).parent().addClass('subactive');

            $('.subactive').parent().parent().addClass('active');
            $(this).parent().removeClass('active');
            $(this).parent().parent().show();
        }
    });

    /* ---------- Submenu  ---------- */

    $('.dropmenu').click(function(e) {
        e.preventDefault();
        $(this).parent().find('ul').slideToggle();
    });

    $('.nav-trigger').click(function() {
        $('.side-nav').addClass('visible');
    });
});

/*--------- end here --------------*/

/*--------- end here --------------*/





//for message toast automatic hide after some time
$(document).ready(function () {
    $('#message-tost-id-small').delay(4000).fadeOut();
    // $('#alert-text-id').delay(4000).fadeOut();
    // setTimeout(function(){ $('#alert-text-id').fadeOut() }, 5000);
});

window.setTimeout(function() {
    $(".alert").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 4000);


//for flora liecence text hide
$(document).ready(function () {
    $(".fr-wrapper + div").css("display", "none");
});

function addPatient() {
    $('#payment_modal').modal('hide');
    debugger;
    var baseURL = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port: '');
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var name = $('#name').val();
    if (name){
        $.ajax({
            type: "POST",
            url: baseURL + '/add/patient/',
            data: {
                'name':$('#name').val(),
                'age':$('#age').val(),
                'temp':$('#temp').val(),
                'bp':$('#bp').val(),
                'weight':$('#weight').val(),
                'adv':$('#adv').val(),
                'cap':$('#caps').val(),
                'tab':$('#tabs').val(),
                // 'gender':$('#gender').val(),
            },
            dataType: "json",
            headers:{
                "X-CSRFToken": csrftoken
            },
            beforeSend: function () {
                var text = "please wait"
                ajaxLoaderStart(text);
            },

            success: function (data) {
                debugger;
                ajaxLoaderStop();
                paymentAdd(data)
            },
            error: function (jqXHR, ex) {
                ajaxLoaderStop();
                console.log((JSON.stringify(jqXHR)));
                return false;
            }

        })
    }
    else {
        $('#payment_modal').modal('hide');
        alert("Please enter the required fields.")
        return ;
    }


}

// function addCustomer() {
//     debugger;
//     var baseURL = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
//     var requestData = {};
//     $.ajax({
//         url: baseURL+'/customer/addEdit/',
//         method: 'GET',
//         contentType: "application/json",
//         beforeSend: function () {
//             var text = 'fetching data. please wait...';
//             ajaxLoaderStart(text);
//         },
//         success: function (data) {
//             ajaxLoaderStop();
//             // alert(data);
//             $("#addBranchByGymIdResponse").html("");
//             $("#addBranchByGymIdResponse").append(data);
//             $('#gymBranchModel').modal('show');
//
//         },
//         error: function (jqXHR, ex) {
//             ajaxLoaderStop();
//             // alert(JSON.stringify(jqXHR));
//         }
//     });
//
//
// }