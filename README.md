### **Program to find a healthier food item, based on the Open Food Facts API.**

#### **Description**


This project has been developed for an Openclassrooms project.
Its purpose is for the user to choose a food item and find a better alternative, dieteticly speaking.


#### Prerequisites

**Python3**  

Linux : 
1) With command line =>_apt install python3_
2) Download compressed file here : https://www.python.org/downloads/source/ 

Windows : Donwload here => https://www.python.org/downloads/windows/

MacOS : Download here => https://www.python.org/downloads/mac-osx/

**MySQL**

Linux : 

1) With command line => _apt install mysql-server_
2) Download the MySQL installer on : https://dev.mysql.com/downloads/mysql/

Windows and macOS :

Download the MySQL installer on : https://dev.mysql.com/downloads/mysql/

**Create the database**

Use the file _script_database.sql_ : it will create the database, its tables, 
encoding and user for you.

**Python libraries**

Go to the project folded and type in your terminal : _pip install -r requirements.txt_


#### How to use

Start _program.py_ on a terminal. A window opens and the program connects with your database, which will be
filled with the API request automatically if it is empty.
You can see the categories and products available.
Select a category number and the program display to you the product associated to this
category.
Then select the id of the product you would like to trade.
If the program find a product from the same category but with a higher nutriscore,
it will display it to you.
You can then choose to save a substitute by entering its id.
You can see your saved products, if you have some,  with a information link and a 
store where you can buy, on the right section of the window.




