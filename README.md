# Route Scheduler
- Created and implemented a Regression algorithm to mimic a simulation device for Hard disks by learning based on the provided data set.
- Improved the model accuracy from 73% to 86% by implementing various pre-processing techniques as well as changing the regression model being used.
- Implemented optimizer algorithms to find optimized parameter values from the data set to get higher output performance.


<h2 align="left">About</h2>
We have built an appointment scheduling and routing solution that helps in reducing manual, time-taking processes. It takes total number of vehicles available as well as all the locations that need to be covered and provides the best routes that will take least time to cover all the location.<br>
The time as well as distance between every two locations is calculated using google APIs which are then processed on the server as a REST API.<br>
All the routes, that are calculated using time and distance between locations, are displayed with different colors on Map using google maps and leaflet library.<br>
Our algorithm takes care of the real-time traffic that the rider will face while going for the appointment and will schedule the routes based on it as well as considering the distance between the locations. <br>
The user can add total number of vehicles available. Also, they can add as many locations as they want to be routed as we have made it dynamic in the frontend.

<h4 align="left"> Important:</h4>
We have added a feature for adding locations that might come up while the rider is on for the appointments.  The route will dynamically get changed to add that new location to be visited along the way. 

<h3 align="left">Demo</h3>
Visit: https://routescheduler.herokuapp.com/

## Available Scripts

1. First fork this repo and then Clone it
2. Run `cd sms` - to move into the directory 
3. Install virtualenv using command - `pip install virtualenv`
3. Now activate the virtual environment using command - `py -m venv env`
4. Now activate the virtual env using command - `.\env\Scripts\activate` . This will activate the virtual environment. For linux and Mac try - `source env/bin/activate`
5. Install flask - `python -m pip install flask`.
6. Install all requirements by - `pip install -r requirements.txt`.
7. Now to migrate the models run - `python manage.py migrate`.
8. Now to activate the localhost server run - `python -m flask run`<br />
<pre>
	Runs the app in the development mode.<br />
	Open (http://localhost:8000) to view it in the browser.
</pre>
