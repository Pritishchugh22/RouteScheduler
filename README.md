# Route Scheduler
We have built an appointment scheduling and routing solution that helps in reducing manual, time-taking processes. It takes total number of vehicles available as well as all the locations that need to be covered and provides the best routes that will take least time to cover all the location.
The time as well as distance between every two locations is calculated using google APIs which are then processed on the server as a REST API.
All the routes, that are calculated using time and distance between locations, are displayed with different colors on Map using google maps and leaflet library.
Our algorithm takes care of the real-time traffic that the rider will face while going for the appointment and will schedule the routes based on it as well as considering the distance between the locations. 
The user can add total number of vehicles available. Also, they can add as many locations as they want to be routed as we have made it dynamic in the frontend.

Important:
We have added a feature for adding locations that might come up while the rider is on for the appointments.  The route will dynamically get changed to add that new location to be visited along the way. 


1. Run cd sms - to move into the directory
2. Install virtualenv using command - pip install virtualenv
3. Now activate the virtual environment using command - virtualenv env
4. Now activate the virtual env using command - .\env\Scripts\activate . This will activate the virtual environment. For linux and Mac try - source env/bin/activate
5. python -m pip install flask
6. Install all requirements by - pip install -r requirements.txt
7. Now to activate the local host server, run python -m flask run
