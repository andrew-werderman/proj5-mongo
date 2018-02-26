# Project 5: Brevet time calculator with Ajax and MongoDB

Simple list of controle times from project 4 stored in MongoDB database. Built on top of the previous project repository--proj4. Implemented by Andrew Werderman <awerderm@uoregon.edu>. 

To run this application: Download the repository, put a credentials.ini file in the directory including a SECRET_KEY = secretkey (can be generated in the pyhton shell by import os, os.urandom(24)) and PORT = 5000, and in the shell run docker-compose up in the DockerMongo directory (assuming the user has Docker installed and running). Now visit localhost:5000 in your web browser!


## Added Functionality

I have created two buttons: 'Submit' and 'Display'. Upon clicking 'Submit', the *valid* controls will be grabbed and entered into the user's database. Upon clicking 'Display', the entries from the database will be displayed in a new page. 

When the user clicks 'Submit', only the controls currently listed on the page will be in the database--all previous controls from earlier 'Submit' clicks will be replaced, if they no longer remain on the page. Revisiting the homepage will also clear the database. This means that once the user has visited the database page from clicking 'Display', returning to the homepage will clear out those controls. 

If there is nothing in the database, clicking 'Display' will bring the user to the database webpage and show an empty database. If there are no *valid* controls listed, clicking 'Submit' will only write a message at the top of the notes area. 


## Rules for Controls and Calculating Open/Close Times

The algorithm for calculating controle times is described at
https://rusa.org/octime_alg.html. Additional background information can be
found at https://rusa.org/pages/rulesForRiders.

As per the table at https://rusa.org/octime_alg.html, there are several different
distance intervals on which the minimum speed and maximum speed change. To clear up
some of the ambiguous parts about the algorithm, here is a discription of this implementation:

The intervals provided at https://rusa.org/octime_alg.html should be interpreted as the end boundary value being inclusive (which makes the starting boundary value non-inclusive), and used like
a piecewise function; i.e. the first 200km boundary governs the min/max speed for the 
first 200km of any control, the next 200km boundary governs the min/max speed for the 
next 200km of the same control, and so on. For example: for a control at 600km, the 
rider can go a maximum of 34km/hr for the first 200km (inclusive), 32km/hr until 
the 400km mark, and 30 km/hr for the final 200km. We use the speed limits, or 
minimums, in this way to calculate the opening and closing times for different
controls.

Because it is difficult to make courses exactly 200, 300, 400, etc. kilometers long
there is a certain cushion beyond those theoretical distances for the actual length
of the brevet. We have made the decision to make that cushion at most 15km (inclusive). 
To calculate the opening time of the final brevet, we use the theoretical distance. 
The closing time, after the official start, of the final brevet, by rule, is 13:30 
for 200 KM, 20:00 for 300 KM, 27:00 for 400 KM, 40:00 for 600 KM, and 75:00 for 1000 KM
(using a HH:MM format). This information was found at https://rusa.org/orgreg.html.

The last point of confusion comes from this final rule: the closing time for the
starting point control (at 0km) is one hour after the official start. As a result,
control points that are too close to the start may have an earlier closing time 
than the starting point. An example from https://rusa.org/octime_alg.html illustrates
that a control at 10km closes 40 minutes after the official start (earlier than the
starting point's one hour). 

Finally, all inputs are converted to kilometers and rounded to the nearest
kilometer, and times are rounded to the nearest minute. 


## Testing

One may verify expected test outputs on https://rusa.org/octime_acp.html. A Nose test suite is provided in the DockerMongo directory, see test_acp_times.py. Other tests inculed writing invalid values in the table in the webpage (i.e. a negative number, a very large number, a letter, etc.), submitting an empty table, displaying an empty db. 


