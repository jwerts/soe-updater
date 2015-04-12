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
  python update_soe.py
  ```
