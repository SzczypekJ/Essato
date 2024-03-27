# Instructions for running the code  
  
To run code from this repository, follow these steps:  
**1. Downloading the repository**  
Clone this repository to your local computer using the **'git clone'** command:  
**git clone https://github.com/SzczypekJ/Essato.git**  
  
**2. Go to the project directory**  
Navigate to the directory that contains the downloaded repository:  
**cd folder_name**  
Where **'folder_name'** is the name of the directory that was created when the repository was downloaded.  
  
**3. Install required packages**  
The required packages are:  
- Python
- Flask
- SQLite3
  
To install Python and Flask use **pip install** command.  
To install SQLite3 follow the instructions from this website:  
https://www.tutorialspoint.com/sqlite/sqlite_installation.htm  
  
**4. Change the path to database file**  
In this project I used SQLite 3 database. To connect with it you have to change the path in app.py file on line 9  
to the folder where you clone the project. For example:  
app_info = {'db_file': **'C:/Users/szczy/Desktop/STUDIA/dodat/Esatto/data/patients.db'** - The path to change}
  
**5. Running the application**  
To run the application, run the following command:  
**python app.py**  
This command will run the application. Application can be also run from the project by **running the code**.  
You can also write in terminal the commad:  
**flask run**  
  
**6. Opening the application in the browser**  
When you run the applicaion please copy the **http://127.0.0.1:5000** to your webbrowser or click on it using **CTR+LPM**
