document.addEventListener('DOMContentLoaded', function() {

    // Gets into the edit title function when clicking the pencil
    const pencil = document.getElementById('pencil');
    pencil.addEventListener("click", edit_title);

    // Display details of the day when clicking the row
    const all_trip_rows = document.querySelectorAll('.trip-row');
    
    all_trip_rows.forEach((item) => {
        item.addEventListener("click", () => {
            display_details(item.id);
        });
    });

});


// Function to edit the title
function edit_title() {
    console.log("Button was clicked");

    // Gets the save button, pencil, title and text in title objects
    const save_btn = document.querySelector('#save-btn');
    const title = document.querySelector('#title');
    const title_input = document.querySelector('#titleinput');
    const pencil = document.querySelector('#pencil');

    // Activates the save button and hides the pencil and title
    pencil.className='d-none';
    title.className='d-none';
    save_btn.className='btn btn-primary mx-3 mb-2';
    
    // Activates the input field with the text of the title as default    
    title_input.className='form-control d-inline mx-3 mb-2';
    title_input.value = title.innerHTML;

    // Gets the trip id
    trip_id = document.getElementById('trip-id').innerHTML;

    // Modifies the title when clicking
    save_btn.addEventListener("click", () => {

        // Updates the name of the trip
        fetch(`/trip/json/${trip_id}`, {
            method: 'PUT',
            body: JSON.stringify({
              name: `${title_input.value}`
            })
        });

        // Update HTML new content
        title.innerHTML = title_input.value

        // Hides input and save button and display edit button and content again
        title_input.className='d-none';
        save_btn.className='d-none';
        title.className='d-inline';
        pencil.className='mx-3 mb-2 d-inline';
    })
}


// Function to display details according to the item
function display_details(tripitem_id) {

    const hide_eye = document.getElementById(`hide-${tripitem_id}`);

    document.getElementById(`row-details-${tripitem_id}`).className='table-active';
    hide_eye.className='fa-sharp fa-solid fa-eye-slash d-inline';
    document.getElementById(tripitem_id).className='d-none';

    hide_eye.addEventListener("click", () => {
        hide_details(tripitem_id);
    });
}

function hide_details(tripitem_id) {
    document.getElementById(`row-details-${tripitem_id}`).className='d-none';
    document.getElementById(`hide-${tripitem_id}`).className='d-none';
    document.getElementById(tripitem_id).className='fa-solid fa-eye trip-row';
}