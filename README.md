# easy-flask-server
#### Running the server:
1. Setting up flask app in terminal:
    - In Windows: `set FLASK_APP=server.py`
    - In Linux: `export FLASK_APP=server.py`
2. To run the server: `flask run`
 
 Optional: 
 - to run flask app in debug mode `set FLASK_DEBUG=1` or `export FLASK_DEBUG=1` before running the server.
 - if `LOGFILE` is specified in `.env` the logger will write to that file.
 
 #### About
 Uploading and downloading is only possible when the user gives an API-key that is also in the `.env`-file of the server in the `ALLOWED_KEYS`-variable.
 
---
##### Requirements
- flask
- dotenv
