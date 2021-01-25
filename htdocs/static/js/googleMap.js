let latitude = $('#id_latitude').val();
let longitude = $('#id_longitude').val();


if (!latitude){
    latitude = 25.197017;
}
if (!longitude){
    longitude = 55.274438;
}

let myLatLng = new google.maps.LatLng(latitude, longitude);
let circle;

let map = new google.maps.Map(document.getElementById('myMap'), {
    zoom: 12,
    center: myLatLng
});

let marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    draggable: true
});


function drawCircle() {

    if (circle != undefined)
        circle.setMap(null);

    let multiplication_factor = 1000;
    let radius = $('#id_location_range').val();

    if (radius) {
        radius = radius * multiplication_factor
    } else {
        radius = 5 * multiplication_factor;
        $('#id_location_range').val(5)
    }

    let options = {
        strokeColor: '#004569',
        strokeOpacity: 0.5,
        strokeWeight: 0.5,
        fillColor: '#00679b',
        fillOpacity: 0.2,
        map: map,
        center: myLatLng,
        radius: radius
    };

    circle = new google.maps.Circle(options);
}

function setMarker() {
    if (marker != undefined)
        marker.setMap(null);

    marker = new google.maps.Marker({
        position: myLatLng,
        draggable: true,
        map: map
    });

    if (marker) {
        google.maps.event.addDomListener(marker, "dragend", function () {
            myLatLng = marker.getPosition();
            setLatLongValue();
            drawCircle();
        });
        drawCircle();
    }
}

function setLatLongValue() {
    $('#id_latitude').val(myLatLng.lat());
    $('#id_longitude').val(myLatLng.lng());
}

setLatLongValue();
setMarker();
