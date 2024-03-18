var mymap = L.map('mapid').setView([51.505, -0.09], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);
var marker = L.marker([0, 0]).addTo(mymap);
marker.bindPopup("tunisia").openPopup();

// Function to update marker position based on address
function updateMarker(address) {
    axios.get('https://nominatim.openstreetmap.org/search', {
        params: {
            q: address,
            format: 'json',
        }
    })
    .then(function (response) {
        var data = response.data;
        if (data && data.length > 0) {
            var lat = parseFloat(data[0].lat);
            var lon = parseFloat(data[0].lon);
            marker.setLatLng([lat, lon]);
            mymap.setView([lat, lon]);
        }
    })
    .catch(function (error) {
        console.error('Error fetching data:', error);
    });
}

// Example: Update marker position for Tunis, Tunisia
updateMarker('canada');
