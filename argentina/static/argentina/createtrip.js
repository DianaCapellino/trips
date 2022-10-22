document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').onsubmit = create;
});

function create(event) {
    
    document.querySelector('#trip-form').style.display = 'none';
    document.querySelector('#trip').style.display = 'block';
    
    const attractions = [];
    const all_attractions = document.querySelectorAll('.attraction');
    all_attractions.forEach(attraction => {
        attractions.push(attraction.value);
    });

    console.log(all_attractions);

    const interests = [];
    const all_interests = document.querySelectorAll('.interest');
    all_interests.forEach(interest => {
        interests.push(interest.value);
    });

    const destinations = [];
    const all_destinations = document.querySelectorAll('.destination');
    all_destinations.forEach(destination => {
        destinations.push(destination.value);
    });


    fetch('/trip', {
        method: 'POST',
        body: JSON.stringify({
            num_pax: document.querySelector('#passengers').value,
            min_age: document.querySelector('#min_age').value,
            max_age: document.querySelector('max_age').value,
            days: document.querySelector('#days').value,
            season: document.querySelector('#season').value,
            attractions: attractions,
            interests: interests,
            destinations: destinations,
            quality: document.querySelector('#quality').value
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        window.location.href = "../mytrips.html";
    });
    event.preventDefault();
}