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

// Filter
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('[name="show_all"], [name="for_sell"], [name="for_rent"]');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove the active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));

            // Add the active class to the clicked button
            this.classList.add('active');

            const status = this.getAttribute('name');  // Get the status from button's name attribute
            filterProperties(status);  // Call the function to filter properties
        });
    });
});


// function filterProperties(status) {
//     const propertyItems = document.querySelectorAll('.property-item');  

//     propertyItems.forEach(item => {
//         const itemStatus = item.querySelector('.bg-primary').textContent.trim();  // Get property status

//         if (status === 'show_all' || itemStatus.toLowerCase() === status.replace('_', ' ')) {
//             item.style.display = 'block';
//         } else {
//             item.style.display = 'none';
//         }
//     });
// }


