
# Instructions for Running the Code

To run the code from this repository, follow these steps:

## 1. Downloading the Repository
Clone this repository to your local computer using the following command:
```bash
git clone https://github.com/SzczypekJ/Medical-Clinic.git
```

## 2. Navigating to the Project Directory
Navigate to the directory that contains the downloaded repository:
```bash
cd Medical-Clinic
```

## 3. Installing Required Packages
The required packages are:
- Python
- Flask
- SQLite3

To install Python and Flask, use the `pip install` command:
```bash
pip install flask
```

To install SQLite3, follow the instructions from [this website](https://www.tutorialspoint.com/sqlite/sqlite_installation.htm).

## 4. Changing the Path to the Database File
In this project, SQLite3 database is used. To connect with it, you need to change the path in the `app.py` file on line 9 to the folder where you cloned the project. For example:
```python
app_info = {'db_file': 'C:/Users/szczy/Desktop/STUDIA/dodat/Esatto/data/patients.db'}
```
Change the path accordingly to where your `patients.db` file is located.

## 5. Running the Application
To run the application, execute the following command:
```bash
python app.py
```
This command will run the application. You can also run the application by executing:
```bash
flask run
```

## 6. Opening the Application in the Browser
Once the application is running, open your web browser and navigate to:
```
http://127.0.0.1:5000
```
You can copy and paste this URL into your web browser or click on it while holding `Ctrl` (Windows/Linux) or `Cmd` (Mac) and clicking the link.
