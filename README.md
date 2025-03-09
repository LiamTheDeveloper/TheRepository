# Note: This script has a pushToSQL variable that is set to 1 in order to push data to SQL

The WeatherCSV.py Python script processes rainfall data from a CSV file and optionally pushes the data to an SQL database. 
The script was written with Python 3.12 and it requires the pandas and pyodbc libraries for data processing and SQL operations respectively.

Prerequisites
Before running this script, ensure the following requirements are met:

1. Python Version
This script is written for Python 3.12. If you're running a different version, such as Python 2.x, you may need to update certain functions (like print statements) to match Python 3 syntax.
2. Install Required Libraries
The script depends on the following Python libraries:
pandas: For handling and processing data in the CSV file.
pyodbc: For connecting to and interacting with the SQL database.

3. CSV File (Rainfall Data)
Ensure you have downloaded the Rainfall CSV file and saved it in a location where Python can access it.
The script assumes the CSV file is accessible from the current working directory (CWD) or the script's installation directory.

4. SQL Database (Optional)
Ensure that pushToSQL parameter variable is not set to 1 if you do not want to push to SQL, otherwise, update the SQL variables to the appropriate names. 
The script includes an option to push data to an SQL database. However, this feature is optional -> see the pushToSQL parameter variable in the Variables section of the script.

If you'd like to push data to SQL:

Set up the appropriate SQL environment.
Ensure the SQL server is accessible.
Update the database connection settings in the script as necessary.
If you don't want to push data to SQL (e.g., if you don't have access to a SQL environment), the script has a parameter to disable the SQL push, 
this avoids any errors if the SQL environment is unavailable on your machine.
