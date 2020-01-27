#### API for basic CRUD operations with TODO list
    
##### Steps to up and run application.

1. Before start application, MongoDB should be installed locally or created instance of DB in Cloud.

2. Create virtual environment `virtualenv --python=python3 <path_to_env>/env`.

3. Activate virtualenv `source <path_to_env>/env/bin/activate`.

4. Install dependencies: `pip install -r requirements.txt`.

5. Run app `uvicorn main:app --reload `.

6. Format code `black .`

7. Go To `http://127.0.0.1:8000/docs#/` API documentation.  

