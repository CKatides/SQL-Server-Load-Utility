SQL Server Load Utility

Before you run the program, you will have to edit the Python file to add your own servername and driver(if different from Native Client 11.0) to the function "sqlalch()".

When you run this program, it will present the user with a tk window, where you enter your servername, the name of the database, and the name of the table that you would like to create with your csv file.

When you click Submit, you will then get  a fileopen dialog, where you can navigate to and choose your csv file.

-------------
Functionality
-------------
After double clicking on your file, it will import the data from the file(It will not edit or alter the original file).

It will create a database, based on the initial user entry, as well as a table based on the header row of the csv, creating the columns from it.

It will remove any spaces in the column names and replace them with underscores.

It will fill in any missing data items found in the csv with a zero.

It will then load all of the data into the table.