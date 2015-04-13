# soe-updater
Python script to programatically update an ArcGIS Server Server Object Extension (SOE).

Tested against Python 2.7 and 3.4, ArcGIS Server 10.2.2.

#### Dependencies:
requests (http://docs.python-requests.org/en/latest/)
```
pip install requests
```

#### Usage

1. Update constants at top of script
  ```python
  PROTOCOL = "http://"
  HOST = "localhost"
  USER = "siteadmin"
  PASSWORD = "yourpassword"

  # note that services are suffixed by type when passed to admin REST API
  SERVICES = [r"service_folder\service_name.MapServer"]

  # path to rebuilt SOE file
  SOE_FILE = r"C:\path_to_your_project\bin\Debug\yourSOE.soe"
  ```

2. Run from command line:

  ```
  C:\Projects\_General\_Code\soe-updater>python update_soe.py
  
  Retrieving token...
  Retrieved: oUK04q-J8ORWDUrSWGPfq8zAU29u3q5_YZ79ZvcFZx8kFneOMb5Z2Y2Yf19
  Uploading SOE...
  Uploaded: ibd792bae-a986-4861-8ac3-c16d42f4d610
  Updating SOE...
  Updated!
  Starting services...
  Starting service_folder/service.MapServer
  Started!
  ```
