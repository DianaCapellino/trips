document.addEventListener('DOMContentLoaded', () => {

    // Gets into the edit title function when clicking the pencil
    const pencil_title = document.getElementById('pencil-title');
    if (pencil_title != null) {
        pencil_title.addEventListener("click", edit_title);
    }
    
    // Display details of the day when clicking the row
    const all_trip_rows = document.querySelectorAll('.trip-row');
    
    all_trip_rows.forEach((item) => {
        item.addEventListener("click", () => {
            display_tripitem(item.id);
        });
    });
});


// Function to edit the title
function edit_title() {

    // Gets the save button, pencil, title and text in title objects
    const save_btn = document.querySelector('#save-btn-title');
    const title = document.querySelector('#title');
    const title_input = document.querySelector('#titleinput');
    const pencil = document.querySelector('#pencil-title');

    // Activates the save button and hides the pencil and title
    pencil.className='d-none';
    title.className='d-none';
    save_btn.className='btn btn-primary mx-3 mb-2';
    
    // Activates the input field with the text of the title as default    
    title_input.className='form-control d-inline mx-3 mb-2';
    title_input.value = title.innerHTML;

    // Gets the trip id
    const trip_id = document.getElementById('trip-id').innerHTML;

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
        pencil.className='mx-3 mb-2 d-inline pencil';
    })
}


// Function to display details according to the item
function display_tripitem(tripitem_id, event) {

    // Gets the hide-eye element
    const hide_eye = document.getElementById(`hide-${tripitem_id}`);

    // Shows details and hide-eye and hide the open eye
    document.getElementById(`row-details-${tripitem_id}`).className='table-active';
    hide_eye.className='fa-sharp fa-solid fa-eye-slash d-inline';
    document.getElementById(tripitem_id).className='d-none';

    // Triggers the event to hide the details
    hide_eye.addEventListener("click", () => {
        hide_details(tripitem_id);
    });

    // Activates pencils to edit excursion and hotel details
    const excursion_details = document.getElementById(`pencil-excursion-${tripitem_id}`);
    const hotel_details = document.getElementById(`pencil-hotel-${tripitem_id}`);
    
    if (excursion_details != null) {
        excursion_details.addEventListener("click", () => {
            edit_item("excursion", tripitem_id);
        });
    };

    if (hotel_details != null) {
        hotel_details.addEventListener("click", () => {
            edit_item("hotel", tripitem_id);
        });
    };

}


// Hides the details of each row
function hide_details(tripitem_id) {
    document.getElementById(`row-details-${tripitem_id}`).className='d-none';
    document.getElementById(`hide-${tripitem_id}`).className='d-none';
    
    const save_btn_hotel = document.querySelector(`#save-btn-hotel-${tripitem_id}`);
    const save_btn_excursion = document.querySelector(`#save-btn-excursion-${tripitem_id}`);
    
    // Shows the open eye again
    document.getElementById(tripitem_id).className='fa-solid fa-eye trip-row';

    // Clearing the editing options for hotels if any
    if (save_btn_hotel != null) {
        if (save_btn_hotel.className != 'd-none') {
            save_btn_hotel.className = 'd-none';
            document.querySelector(`#new-hotel-${tripitem_id}`).className='d-none';
            document.querySelector(`#hotel-${tripitem_id}`).className='d-inline';
            document.querySelector(`#pencil-hotel-${tripitem_id}`).className='mx-3 mb-2 d-inline pencil';
            
        };
    };

    // Clearing the editing options for excursions if any
    if (save_btn_excursion !=null) {
        if (save_btn_excursion.className != 'd-none') {
            save_btn_excursion.className='d-none';
            document.querySelector(`#new-excursion-${tripitem_id}`).className='d-none';
            document.querySelector(`#excursion-${tripitem_id}`).className='d-inline';
            document.querySelector(`#pencil-excursion-${tripitem_id}`).className='mx-3 mb-2 d-inline pencil';
        }
    };
}


// Function to allow editing items
function edit_item(type, tripitem_id) {

    // Gets the save button, pencil, item name and select tag
    const save_btn = document.querySelector(`#save-btn-${type}-${tripitem_id}`);
    const pencil = document.querySelector(`#pencil-${type}-${tripitem_id}`);
    const item_name = document.querySelector(`#${type}-${tripitem_id}`);
    const select = document.querySelector(`#new-${type}-${tripitem_id}`);
    const item_description = document.querySelector(`#${type}-description-${tripitem_id}`);
    
    // Activates the save button and hides the pencil and item name
    pencil.className='d-none';
    item_name.className='d-none';
    save_btn.className='btn btn-primary mx-3 mb-2';
    
    // Gets the current item info
    fetch(`/trip/tripitem/${tripitem_id}`)
    .then(response => response.json())
    .then(item => {
        var current_item = "";
        if (type === "hotel") {
            current_item = item.hotel;
        } else {
            current_item = item.excursion;
        }
        const current_destination_id = item.destination;

        // Creates the list of options for item change
        select.className='form-control d-inline mx-3 mb-2';
        fetch(`/json/${type}/${current_destination_id}`)
        .then(response => response.json())
        .then(list => {

            // Creates an option for each element
            list.forEach(element => {
                const current_option = document.createElement('option');

                // Activates the select field with the current item as default
                if (current_item === element.id) {
                    current_option.defaultSelected = true;
                };

                current_option.value = `${element.id}`;
                current_option.text = `${element.name}`;
                select.appendChild(current_option);
            });

            // Function that will be activated when pressing save
            const getSelected = () => {
                const index = select.selectedIndex;
                const selectedOption = select.options[index];
                const detail_id = selectedOption.value;
                
                // Updates the item
                if (type === "excursion") {
                    fetch(`/trip/tripitem/${tripitem_id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            excursion: `${detail_id}`
                        })
                    });
                } else {
                    fetch(`/trip/tripitem/${tripitem_id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            hotel: `${detail_id}`
                        })
                    });
                };
                
                // Gets the information to update content
                fetch(`/json/${type}/${current_destination_id}`)
                .then(response => response.json())
                .then(list => {
                    list.forEach(element => {
                        if (element.id == detail_id) {

                            // Updates HTML new content
                            item_name.innerHTML = element.name;
                            item_description.innerHTML = element.description;
                            
                            // Hides input and save button and display edit button and content again
                            select.className='d-none';
                            save_btn.className='d-none';
                            item_name.className='d-inline';
                            pencil.className='mx-3 mb-2 d-inline pencil';
                        }                    
                    });
                });

            };
            save_btn.addEventListener("click", getSelected);
        });
        
        // Clean the options at select tag to avoid duplicating items
        for (let i = select.options.length; i >= 0; i--) {
            select.remove(i);
        };
    });
}