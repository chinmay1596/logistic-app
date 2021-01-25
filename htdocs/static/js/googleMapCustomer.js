function submitForm() {
        debugger;
        var frm = document.getElementsByName('contact-form')[0];
        var customerFirstName = $("#first_name").val();
        var customerLastName = $("#last_name").val();
        var phone = $('#phone').val();
        var lats = $("#latitude").val();
        var longs = $("#longitude").val();

        if (customerFirstName &&customerLastName && phone && latitude && longitude){
            var validateEmail = email_validation();
            if (validateEmail== true){
                frm.submit(); // Submit the form
                $("#betDisable").attr("disabled", true);
                return false; // Prevent page refresh
            }
            else {
                $("#betDisable").attr("disabled", true);
                setTimeout(function(){document.getElementById("betDisable").disabled = false;},5000);
                throw new Error();
            }

        }
        alert('All fields is required.');
        $("#betDisable").attr("disabled", true);
        setTimeout(function(){document.getElementById("betDisable").disabled = false;},5000);
    }

function validateLocation() {
    if (($('#auto_complete_resopnse_from_google').val() == '') && ($('#latitude').val() == '') && ($('#longitude').val() == '')) {
        alert('please select address field from dropdown')
        return false
    }
    return true
}
function addressFormater() {
    debugger;
//    var locality = document.getElementsByClassName("locality")[0].innerHTML;
//    var region = document.getElementsByClassName("region")[0].innerHTML;
//    var postal_code = document.getElementsByClassName("postal-code")[0].innerHTML;
    var country_name = document.getElementsByClassName("country-name")[0].innerHTML;
//    $('#locality').val(locality);
//    $('#region').val(region);
////    $('#postal_code').val(postal_code);
    $('#country_name').val(country_name);

}
function initialize() {
    debugger;
    var a = $('#lat').val()
    var b = $('#long').val()
    var mapOptions, map, marker, searchBox, city,
        infoWindow = '',
        addressEl = document.querySelector( '#map-search' ),
        latEl = document.querySelector( '.latitude' ),
        longEl = document.querySelector( '.longitude' ),
        element = document.getElementById( 'map-canvas' );
    city = document.querySelector( '.reg-input-city' );
    codeLatLng(a,b)

    mapOptions = {
        // How far the maps zooms in.
        zoom: 8,
        // Current Lat and Long position of the pin/

        center: new google.maps.LatLng( $('#lat').val(), $('#long').val() ),
         center : {
         	lat: 25.197017,
         	lng: 55.274438
         },
        disableDefaultUI: true, // Disables the controls like zoom control on the map if set to true
        scrollWheel: true, // If set to false disables the scrolling on the map.
        draggable: true, // If set to false , you cannot move the map around.
        // mapTypeId: google.maps.MapTypeId.HYBRID, // If set to HYBRID its between sat and ROADMAP, Can be set to SATELLITE as well.
        // maxZoom: 11, // Wont allow you to zoom more than this
        // minZoom: 9  // Wont allow you to go more up.

    };

    /**
     * Creates the map using google function google.maps.Map() by passing the id of canvas and
     * mapOptions object that we just created above as its parameters.
     *
     */
    // Create an object map with the constructor function Map()
    map = new google.maps.Map( element, mapOptions ); // Till this like of code it loads up the map.

    /**
     * Creates the marker on the map
     *
     */
    marker = new google.maps.Marker({
        position: mapOptions.center,
        map: map,
        // icon: 'http://pngimages.net/sites/default/files/google-maps-png-image-70164.png',
        draggable: true
    });

    /**
     * Creates a search box
     */
    searchBox = new google.maps.places.SearchBox( addressEl );

    /**
     * When the place is changed on search box, it takes the marker to the searched location.
     */
    google.maps.event.addListener( searchBox, 'places_changed', function () {
        debugger;
        var places = searchBox.getPlaces(),
            bounds = new google.maps.LatLngBounds(),
            i, place, lat, long, resultArray,
            adr_format = places[0].adr_address;
        $('#adrFormat').html(adr_format);
        addresss = places[0].formatted_address;
        addressFormater();
        $('#mapLocation').val(addresss);

        for( i = 0; place = places[i]; i++ ) {
            bounds.extend( place.geometry.location );
            marker.setPosition( place.geometry.location );  // Set marker position new.
        }

        map.fitBounds( bounds );  // Fit to the bound
        map.setZoom( 15 ); // This function sets the zoom to 15, meaning zooms to level 15.
        // console.log( map.getZoom() );

        lat = marker.getPosition().lat();
        long = marker.getPosition().lng();
        $('#lat').val(lat)
        $('#long').val(long)
        latEl = val(lat);
        longEl = val(long);

        resultArray =  places[0].address_components;

        // Get the city and set the city input value to the one selected
        for( var i = 0; i < resultArray.length; i++ ) {
            if ( resultArray[ i ].types[0] && 'administrative_area_level_2' === resultArray[ i ].types[0] ) {
                citi = resultArray[ i ].long_name;
                // city.value = citi;
            }
        }

        // Closes the previous info window if it already exists
        if ( infoWindow ) {
            infoWindow.close();
        }
        /**
         * Creates the info Window at the top of the marker
         */
        infoWindow = new google.maps.InfoWindow({
            content: addresss
        });

        infoWindow.open( map, marker );
    } );


    /**
     * Finds the new position of the marker when the marker is dragged.
     */
    google.maps.event.addListener( marker, "dragend", function ( event ) {
        debugger;
        var lat, long, address, resultArray, citi;

        console.log( 'i am dragged' );
        lat = marker.getPosition().lat();
        long = marker.getPosition().lng();
        $('#lat').val(lat)
        $('#long').val(long)

        var geocoder = new google.maps.Geocoder();
        geocoder.geocode( { latLng: marker.getPosition() }, function ( result, status ) {
            if ( 'OK' === status ) {  // This line can also be written like if ( status == google.maps.GeocoderStatus.OK ) {
                address = result[0].formatted_address;
                resultArray =  result[0].address_components;

                // Get the city and set the city input value to the one selected
                for( var i = 0; i < resultArray.length; i++ ) {
                    if ( resultArray[ i ].types[0] && 'administrative_area_level_2' === resultArray[ i ].types[0] ) {
                        citi = resultArray[ i ].long_name;
                        console.log( citi );
                        // city.value = citi;
                    }
                }
                addressEl.value = address;
                // latEl = val(lat);
                // longEl = val(long);

            } else {
                console.log( 'Geocode was not successful for the following reason: ' + status );
            }

            // Closes the previous info window if it already exists
            if ( infoWindow ) {
                infoWindow.close();
            }

            /**
             * Creates the info Window at the top of the marker
             */
            infoWindow = new google.maps.InfoWindow({
                content: address
            });

            infoWindow.open( map, marker );
        } );
    });
}
function codeLatLng(lat, lng) {
    debugger;
    var geocoder= new google.maps.Geocoder();

    var latlng = new google.maps.LatLng(lat, lng);
    geocoder.geocode({'latLng': latlng}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            console.log(results)
            if (results[1]) {
                //formatted address
                address = results[0].formatted_address
                $('#map-search').val(address);
                // alert(address)
                //find country name
                for (var i=0; i<results[0].address_components.length; i++) {
                    for (var b=0;b<results[0].address_components[i].types.length;b++) {

                        //there are different types that might hold a city admin_area_lvl_1 usually does in come cases looking for sublocality type will be more appropriate
                        if (results[0].address_components[i].types[b] == "administrative_area_level_1") {
                            //this is the object you are looking for
                            city= results[0].address_components[i];
                            break;
                        }
                    }
                }
                //city data
                // alert(city.short_name + " " + city.long_name)
            }
        }
    });
}
// function for gymBranch_email_validation
function email_validation() {
    debugger;
    var text_email = (document.getElementById("email").value).replace(/\s+/g, '');;
    if (text_email ){
        var seperated_emai = text_email.split(',');
        var re = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        for (var i=0;i<seperated_emai.length;i++){
            var validate_email = re.test(String(seperated_emai[i]).toLowerCase());
            if (validate_email==false){
                var invalidEmail = seperated_emai[i];
                alert('Please fill the correct email' ,invalidEmail);
                $("#betDisable").attr("disabled", true);
                return false;
                break;
            }
            else {$("#betDisable").attr("disabled", false);
            }
        }return true;
    }
    else {return true;}
}

