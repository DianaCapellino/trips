# MY TRIP TO ARGENTINA WEB APPLICATION
#### Introduction:

This is a web application designed for people insterested in preparing a trip to Argentina. The idea is to give a first proposal itinerary based on the information given such as interests and destinations that the user have already visited. The user can later modify the details of the excursions and the hotels and share the trip with another user and make comments.

I have a degree in tourism and have worked in the last 10 years in incoming tourism to Argentina so it is a field I know and feel confortable with which was the main reason I decided to work on this web application.

#### Distinctiveness and Complexity:
The web application has information about Argentina main destinations but also the functionality to create a trip based on the interests, attractions desired and already visited destination/s by the user. With the knowledge I have about tourism in Argentina I have carefully created each object destination with the information.

The main complexity in the application is the creation of the new trip that needs to have in mind the quantity of days the user wants to travel, the destinations they have already visited and the interests and attractions desire. Other features implemented includes the option to edit the excursion and the hotel indicated each day made with Javascript on the front-end (client side) and Django on the back-end (server side).

The web application uses Bootstrap for styles purposes but also to implement the responsive design. It has also implemented an animation with CSS at the home page.

#### Contents:
The app works with Django so as expected the files urls.py contents the links to the sites and the functions in views.py with the functionality for each page. In admin.py some models where installed to help to load the first database of destinations, hotels and excursions. In db.sqlite3 was created the database through Django migrations from the models created.

I detail below the most important files where the funcionality was added:

Inside 'argentina' folder:

- models.py:
    It contains the models built for the application. The models Destination, Hotel and Excursion contain information to build the trips. The model TripData takes all the information provided by the user and it is used to build the trip. The model Trip is where all the main information about the trip is contained. TripItem is a model that is used to contain the information for each item of the trip (each day is a TripItem). The Comment model is used for adding comment at each trip and SharedUser to share an specific trip with another user/users.

- views.py: 
    It contains the core functionallity of the application to the registration, login, logout, creation of the trip, json responses for API.

In the static folder is saved all the images with the icons, the styles.css where all the style is implemented general and with Bootstrap and Javascript files provided by Bootstrap.
In the 'js' foler inside static is found the Javascript code implemented for the web application:

- edittrip.js:
    This file contains all the functionality on the client side to edit the trip from the main trip page ('trip.html').

The web application has the following pages saved in the templates folder:

- layout.html: 
    It contains the layout for the nav menu and footer.

- index.html: 
    This page contains an animation built with CSS with images of Argentina.

- destinations.html:
    Brings all the destinations in cards and when clicking the cards you can see pictures and details for each destination.

- excursions.html:
    Brings all the excursions in cards and when clicking the cards you can see pictures and details for each destination.

- hotels.html:
    Brings all the hotels in cards and when clicking the cards you can see pictures and details for each destination.

- register.html: 
    The register page is access when clicking "Register" in the menu. It is hidden when user has already logged in where a dropdown menu will appear.
    It is compulsory to give a username and a password, repeat it, and giving an e-mail. The username cannot be repeated. The validation is made server side and sends a message that appears as an alert message on the top of the registration page.

- login.html: 
    This page can be acceded by clicking "Log in" in the menu. If the user has already logged in, the option is not shown and in that place a dropdown menu appears with the username. The user should provide the username and password. The validation works exactily as mentioned for register.html.

- mytrips.html:
    This is a page that only is possible to access when the user has logged in, accessing by the dropdown menu with the name of the username. It contains all the trips created by the user and at the end the trips shared to the user.

- newtrip.html:
    As in mytrips.html, this page is also accesible through the dropdown menu if the user has logged in.

- trip.htmal:
    It is possible to access this page when clicking the trip selected in mytrips.html. This is the main page of the trip where it is possible to edit items when clicking the eye icon and then the pencil. It is also possible to edit the title when clicking the pencil next to the title and delete the trip when clicking the trash icon. Here it is also where the comments are shown and in the aside menu the users and share the trip. The aside section is moved down where it is seen in small screens.

#### How to run the application:
From the main directory, execute in the terminal:
- python3 manage.py runserver