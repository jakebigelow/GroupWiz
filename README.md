```
----------------------------------------------------
   ___                             __    __  _      
  / _ \ _ __   ___   _   _  _ __  / / /\ \ \(_) ____
 / /_\/| '__| / _ \ | | | || '_ \ \ \/  \/ /| ||_  /
/ /_\\ | |   | (_) || |_| || |_) | \  /\  / | | / / 
\____/ |_|    \___/  \__,_|| .__/   \/  \/  |_|/___|
                           |_|                      
----------------------------------------------------
```


GroupWiz is a tool that is designed to interact with GoPhish's API. It is designed to allow the user to view existing groups, search for contacts in those groups, delete groups, and to upload new sending groups without ever having to open up browser.

---
To use the tool install you will need to run the following command in the directory that cloned the repo into: 
```
pip3 install requirements.txt
```
You will also need to pull the API key for you GoPhish instance. Once you have the the API key save it in a .env file located in the same directory as GroupWiz.py
This will ensure that you have the correct libraries installed on your machine to use GroupWiz.

To use the tool use the following command:
```
python3 /path/to/GroupWiz.py -h
```

This will show the help menu for the tool. Allowing you to see the various arguments that it will accept. 

To view the groups that already exist on your GoPhish instances you can run the following command:
```
python3 /path/to/GroupWiz.py -l -u <your_domain.com>
```

To view the details about a specific group run the following command:
```
python3 /path/to/GroupWiz.py -l -n <Group_Name> -u <your_domain.com>
```

If you would like to search to see if a specific contact has been added to any of the groups that exist on the GoPhish instance you can do so by search for them by either the Frist Name and Last Name or by their email address. To run a search run the following command:
```
python3 /path/to/GroupWiz.py -l -fn <First_Name> -ln <Last_Name> -u <your_domain.com>
```
or 
```
python3 /path/to/GroupWiz.py -l -e <Email_Address> -u <your_domain.com>
```

---
If you are looking to create a new sending group this can be done with a csv file that contains headers for the following categories.  The headers that the GroupWiz looks for are a first name, last name, email address, and position.  As of version one the only header that is required is the email header.

To create a new group run the following command: 
```
python3 /path/to/GroupWiz.py -f /path/to/contact/csv -u <your_domain.com>
```

This command will create a Sending Group that contains all of the entries in the file. 

If you would like to create a Sending Group that is a random size as well has random entries pulled use the following command: 
```
python3 /path/to/GroupWiz.py -f /path/to/contact/csv -rand -u <your_domain.com>
```

If you have more targets then needed and would like to select a random selection of targets from the file you can use the following command:
```
python3 /path/to/GroupWiz.py -f /path/to/contact/csv -rand -c -u <your_domain.com>
```

There are more features coming in the near future. If you would like something specific please reach out to and let me know and I will see what can be done. 

