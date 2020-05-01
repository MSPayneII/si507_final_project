# si507_final_project

#################################
##### Name: Michael Payne
##### Uniqname:mpaynei
##### Final Project
#################################


To run the program, you will need the following on your computer:
BeautifulSoup
flask
requests
json
sqlite3

DIRECTIONS ON HOW TO RUN FILE
1. Download the folder called: si507_final_project
2. Open python 3
3. Locate main.py
4. When you locate the file, in your command prompt run: main.py
5. Open http://127.0.0.1:5000/ in your web Browser
6. Complete the flask form and click "Get Sites" to view results

WHAT SHOULD HAPPEN IF THE PROGRAM RUNS CORRECTLY
Once the program runs, the user will complete the flask form in their web browser and submit it to receive their search results for Underground Railroad Site information.

PROJECT DESCRIPTION
I am choosing to do my project on Historic Underground Railroad Sites in the United States.
I scraped and crawled data from: "https://www.nps.gov/nr/travel/underground/states.htm" using BeautifulSoup. The user will be able to look up various information about sites like (name, description, state, and it's location) via flask. There are five different ways to present the data. The user can sort the data by State(1) or Site(2). Then they have the option to sort in ascending order(3) or descending order(4). Finally, they have the option to filter the results by State(5) rather than receive a list of sites for all states.


BACKGROUND
There are 23 states with a combined 83 Underground Railroad Sites. The following data was retrieved for each site:
- Name - The official name of the Underground Railroad Site
- Description - provides historical background for the site
- Location - describes where the site is located
- Image_url - provides a visual image of the location (i.e., a house, place where the building once stood, etc) in jpg format

Data will be shown to the user with Flask forms.


I’ve created a database with two tables: States_Sites and Site_Info. The ID field in both tables serves as a primary key and links the two tables together.

Table 1
Name:  States_Sites
Fields:
- "Id" INTEGER PRIMARY KEY AUTOINCREMENT”
- "State" TEXT NOT NULL
- "Site_Name" TEXT NOT NULL
- "Site_URL" TEXT NOT NULL

 Table 2
 Name:  Site_Info
 Important note: Site_name for this table will be pulled from Table 1. Because of this in Table 2 “Site_name” values are listed as “see states_sites table for name”.
 Fields:
- "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
-  "Site_name" TEXT NOT NULL,
-  "Location" TEXT NOT NULL,
-   "Description" TEXT NOT NULL,
-   "Image_URL" TEXT NOT NULL


I am using Flask as a means for user interaction and information presentation.
Please note: In my flask html table, I’ve included the original site url which, when clicked,  will redirect the user to the actual page where they can view any data that is missing. Due to the inconsistent formatting of the webpages, I was unable to pull all of the necessary information for each site. For data that was unable to be pulled, the user will see a prompt that says the data is unavailable. For example, if a location was not able to be successfully pulled, the prompt would read “Location Data Available”.


Once the program runs, The user will be able to view a browser titled:
"Welcome to the Underground Railroad Site Browser". Through Flask, the user will be prompted to fill out a flask form. They have the option to sort data for Underground Railroad Sites by State or Site. They also have the option to sort the data “Top to bottom” or “Bottom to Top”. “Top to bottom” means the site information will be displayed in ascending order (e.g. A-Z) while “Bottom to Top” will display the data in descending order (e.g. Z-A). If the user chooses, they can filter site results by state or view information from all States. If they select a state, they will only see site results for sites in that state. Once search criteria are made, the user submits the form via the “Get Sites” button and are shown the results.
