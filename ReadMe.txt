An API For Social-Media Database Project In Databases Courses ECE AUTH
Ιmplemented Flask Framework in Python language and MySQL as database

Instructions To Run:
0)Have python.For the project used python 3.9.1
1) Run Sql Script (SocialMedia.sql) to create the database and then run users.sql to create users
2) Import flask,MySQldb or (mysql-client),flask_mysqldb libraries with  pip install "package" in Command Prompt
3) From Command Prompt go to directory where main.py is
3) Write: 
For Windows:
> set FLASK_APP=main.py
> flask run

For Linux:
> export FLASK_APP=main.py
> flask run


Then the Url Is:
Running on http://127.0.0.1:5000/


Structure of files:
	--pythonlogin	
		--main.py	
		--templates		
			--chat.html	
			--chathead.html
			--friendrequests.html
			--MainPage.html
			--Profile.html
			--register.html
			--Search.html
			--start_screen.html
			--VisitProfile.html	
		--static
			--logo.png
			--login_image.png

