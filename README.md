# Classroom Portal for Academic Food Computers

## Dev setup

### Backend:
1. Run Flask server in a terminal:

**For Python3 on MacOS**:

    ```sh
    $ cd server
    $ python3 -m venv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt
    (env)$ python server.py
    ```
    
**For Windows or Hopper (Python2.7), please check the documeentation**
>https://flask.palletsprojects.com/en/1.1.x/installation/#create-an-environment

   **It will be live at** [http://localhost:5000](http://localhost:5000) (_note: this points to nothing at the moment_)

    Test it by making a call to the test endpoint
    > http://localhost:5000/api/test/itWorks/
                    
                                                                                                                                                                                                                                                                                                                                 
### Frontend
2. Run the Vue web app in a separate terminal:

    ```sh
    $ cd web
    $ npm install
    $ npm run serve
    ```

    **It will be live at** [http://localhost:8080](http://localhost:8080)
    
    _Currently there is no database, so use the student and teacher buttons to login_
