# Classroom Portal for Academic Food Computers

## Project Description

The portal is a Vue web app that is primarily single page. Each tab and page on the web app is called a "view" (and are stored in the views folder). Views are made up of one or more components (which are stored in the components folder).

The backend is written in Flask and is responsible for having API endpoints available for the web app to call in order to access data from and store data to the database.  
  
<hr>

## Dev Setup

### Backend:
1). Set up env  

    cd server
    python3 -m venv env
    source env/bin/activate

2). Install requirements  
  
    make python-packages

    # or

    pip install -r requirements.txt

3). Have a [local Postgres database set up](https://github.com/EricHusa/FC-classroom-Portal/wiki/Local-db-Initialization-and-Workflow)

4). Run Flask server in a terminal:  

    python app.py

**For Windows or Hopper (Python2.7), please check the documentation**
>https://flask.palletsprojects.com/en/1.1.x/installation/#create-an-environment

   **It will be live at** [http://localhost:5000/api/](http://localhost:5000) (_note: this points to nothing, but is the base url for api calls_)

  

### Frontend
2. Run the Vue web app in a separate terminal:

    ```sh
    $ cd web
    $ npm install
    $ npm run serve
    ```

    **It will be live at** [http://localhost:8080](http://localhost:8080)
