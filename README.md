# Smart Decisions by UnbasicJeans
## Description
We will visualize data on both monthly presidential approval ratings and consumer price indices in the United States to look for an enduring correlation between the two. Users will have access to detailed, overlapping timelines of presidential approval ratings and consumer price indices, as well as brief explanations of how the data can be interpreted. We hope that this will inform users about the effects that the economy has on presidential approval ratings. We think this is especially important for devos who are newly or soon-to-be eighteen years old so that they can be cognizant about the factors influencing their voting behavior. Our site would also have a discussion board, where users can post their opinions about the data and interact with other users. 

## Feature Spotlight
- Discussion section where you can make comments about the graphs
- Two graphs you can zoom in and out of
- Each individual data point on the graph is shown if you hover over it with your mouse
- Magnifying glass to zoom in on certain sections of the graph
- Hand button to move the graph
- You can download the graphs in SVG, PNG, and CSV

## Known Bugs/Issues
- No known bugs/issues in our website

## Roster & Roles
- Chloe Wong (PM) - Flask App
  - Linking pages and other backend stuff through Flask
- Brian Liu - Frontend
  - Implementing data visualization using Apex
  - Making website look nice with Tailwind and CSS
- Kishi Wijaya - Database
  - Implement login and user preferences
  -Handling processing of datasets and databases
- Raymond Lin - Flask App/Database
  - Connect database to frontend through Flask

## Install Guide
Our project can be installed locally by carrying out the following steps. Users may also skip installation and go straight to the website at the top of our Launch Codes.
1. Clone and move into this repository
```
$ git clone git@github.com:chloepwong/p04.git
```
```
$ cd p04
```
2. Create a virtual environment
```
$ python3 -m venv foo
```
3. Activate the virtual environment: Linux/MacOS
```
$ . foo/bin/activate
```
3. Activate the virtual environment: Windows
```
$ foo\Scripts\activate
```
4. Install required packages
```
$ pip install -r requirements.txt
```
## Launch Codes
Our project can be launched locally by carrying out the following steps. Users may also go straight to http://159.223.128.39/.
1. Move into this repository
```
$ cd p04
```
2. Activate the virtual environment: Linux/MacOS
```
$ . foo/bin/activate
```
2. Activate the virtual environment: Windows
```
$ foo\Scripts\activate
```
3. Move into the app directory
```
$ cd app
```
4. Run the Flask app
```
$ python3 __init__.py
```
5. Navigate to localhost: http://127.0.0.1:5000
