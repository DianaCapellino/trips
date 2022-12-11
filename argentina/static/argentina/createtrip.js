document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').onsubmit = create;
});

function create() {
    
    document.querySelector('#trip-form').style.display = 'none';
    document.querySelector('#trip').style.display = 'block';
    
    fetch('/trip', {

    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        window.location.href = "../mytrips.html";
    });
}