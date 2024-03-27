var mymap = L.map('mapid').setView([51.505, -0.09], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);
var marker = L.marker([0, 0]).addTo(mymap);
marker.bindPopup(Property.address).openPopup();


// Function to update marker position based on address fetched from Flask route
function updateMarkerFromFlask(propertyId) {
    axios.get('/get_address', {
        params: {
            property_id: propertyId
        }
    })
    .then(function (response) {
        var data = response.data;
        if (data && data.address) {
            updateMarker(data.address);  // Call the original updateMarker function with the fetched address
        } else {
            console.error('Error fetching address:', data.error);
        }
    })
    .catch(function (error) {
        console.error('Error fetching address:', error);
    });
}

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



// Example usage
updateMarkerFromFlask(Property.address);  // Pass the property ID to fetch its address from MySQL


// Filter
document.addEventListener('DOMContentLoaded', function() {
    const filterButtons = document.querySelectorAll('[name="show_all"], [name="for_sell"], [name="for_rent"]');
    
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            console.log(filterButtons);
            // Remove the active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            console.log("hello");
            console.log(this);
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


document.getElementById('propertyStatus').addEventListener('change', function() {
    var selectedStatus = this.value;
    fetch('/load_properties?status=' + selectedStatus)
        .then(response => response.text())
        .then(data => {
            document.getElementById('propertyListings').innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
});



// Spinner
var spinner = function () {
    setTimeout(function () {
        if ($('#spinner').length > 0) {
            $('#spinner').removeClass('show');
        }
    }, 1);
};
spinner();

 // Back to top button
 $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
});
$('.back-to-top').click(function () {
    $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
    return false;
});

// function toggleFavorite(event, propertyId) {
//     event.preventDefault(); // Prevent the form submission

//     // AJAX request to add/remove property from favorites
//     fetch(`/add_favorite/${propertyId}`, { method: 'POST' })
//         .then(response => {
//             // Toggle the heart color
//             const heartIcon = event.target;
//             heartIcon.classList.toggle('text-danger'); // Add or remove 'text-danger' class
//         })
//         .catch(error => console.error('Error:', error));
// }


