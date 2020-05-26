# OnlineWeatherGrp12
This is the remote branch for Group 12 for the Online Weather PA1450 Project

# How to run
To run, simply install all required packages by running `pip install -r requirements.txt` and then run `__main__.py`, everything should start up properly.

## Start Page

The start page consists of information regarding which group has been developing this program. Simply click the button "Next" to move on to the graph page.

## Graphing Data

On page number two, you will find three important sections, the interval selection and the attribute selection, and the graph window itself. First select an interval start and end date and time, thereafter pick the attributes you wish to view on the graph. To select an attribute, simply click an attribute on the left of the screen. 

You can of course pick multiple attributes at once but please keep in mind that everything isn't evenly scaled and certain combinations won't produce good resulting graphs.

### Selecting an interval date and time

* To select an interval date, first pick a starting date by using the dropdown calendar. It should be intuitive in how you navigate the calendar.
* After picking a date, you  can pick an hour of the day using the hour dropdown right of the calendar dropdown.

## Updating the graph

The graph updates automatically whenever you pick a date, a time, or a new attribute. 

## Resizing the window

This program has the ability to resize the window if you wish to. To do it, simply click the dropdown menu "Resize" at the top left of the screen. A list of supported sizes will show. Click the size you wish to view and the screen will update immediately.

# Note regarding the MVP

In our MVP it mentions that it should be a website, but to avoid complications that could potentially arise when hosting a website, we decided to make use of tkinter to build an application instead. Tkinter solely handles the graphical user interface and graphics, and not the functionality. 

Please also note that there is no API to gather weather data yet and all data is downloaded and located in the folder `weatherdata`, hence only four months of data is available to graph, starting from January 14th at midnight until May 23rd at 8pm.