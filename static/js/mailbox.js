// TO MAKE THE MAP APPEAR YOU MUST
// ADD YOUR ACCESS TOKEN FROM
// https://account.mapbox.com
// reference url: https://www.codeproject.com/Articles/587199/Draw-Cirlce-Around-Marker-in-Google-Map
mapboxgl.accessToken = 'pk.eyJ1IjoiY3RhbGx1aXRlbCIsImEiOiJja2V4NHl6b2EwbWMwMnVuNDFpNjVtZmd4In0.Yqjn_RjJ-aVszxNq-RDFRg';
var latitude = parseFloat($('#id_latitude').val())
var longitude = parseFloat($('#id_longitude').val())

if (!latitude) {
    latitude = 25.110530
}
if (!longitude) {
    longitude = 55.234573
}

var map = new mapboxgl.Map({
    container: 'myMap',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [longitude, latitude],
    zoom: 11
});
var remove_layer = false;

var marker = new mapboxgl.Marker(
    {
        draggable: true
    }
).setLngLat([longitude, latitude]).addTo(map);

function onDragEnd() {
    var lngLat = marker.getLngLat();
    $('#id_longitude').val(lngLat.lng);
    $('#id_latitude').val(lngLat.lat);
    drawCircle();
}

marker.on('dragend', onDragEnd);
map.on('load', onDragEnd);

function drawCircle() {
    var createGeoJSONCircle = function (center, radiusInKm, points) {
        if (!points) points = 64;

        var coords = {
            latitude: center[1],
            longitude: center[0]
        };

        var km = radiusInKm;

        var ret = [];
        var distanceX = km / (111.320 * Math.cos(coords.latitude * Math.PI / 180));
        var distanceY = km / 110.574;

        var theta, x, y;
        for (var i = 0; i < points; i++) {
            theta = (i / points) * (2 * Math.PI);
            x = distanceX * Math.cos(theta);
            y = distanceY * Math.sin(theta);

            ret.push([coords.longitude + x, coords.latitude + y]);
        }
        ret.push(ret[0]);

        return {
            "type": "geojson",
            "data": {
                "type": "FeatureCollection",
                "features": [{
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [ret]
                    }
                }]
            }
        };
    };

    if (remove_layer) {
        map.removeLayer("polygon");
        map.removeSource("polygon");
    }
    console.log($('#id_longitude').val(), $('#id_latitude').val())
    map.addSource(
        "polygon",
        createGeoJSONCircle(
            [parseFloat($('#id_longitude').val()), parseFloat($('#id_latitude').val())],
            parseInt($('#id_location_range').val())
        )
    );
    map.addLayer({
        "id": "polygon",
        "type": "fill",
        "source": "polygon",
        "layout": {},
        "paint": {
            "fill-color": "green",
            "fill-opacity": 0.3
        }
    });
    remove_layer = true;
}

$(document).on('click', '.check-radius', function (e) {
    drawCircle();
})