# INF2009

## Web Server

Ensure Python is installed:

```
python --version
```

Go to Web Server Folder:

```
cd .\Webserver\
```

Install required dependencies:

```
pip install -r requirements.txt
```

Add `.env` file to Webserver/ folder and replace with your own credentials

- It's in `.gitignore` but just check it isn't in staged before you push

Go to `C:\xampp\mysql\bin\my.ini` or the equivalent in your machine, under `[mysqld]` add/edit this line:

```
max_allowed_packet=16M
```

Open XAMPP Control Panel and Start MySQL. Connect to MySQL.

Run the app:

```
python app.py
```

Should set up the db and everything if its the first time
