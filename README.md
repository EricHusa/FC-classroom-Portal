# Classroom Portal for Academic Food Computers

### Dev setup

1. Run Flask server in a terminal:

    ```sh
    $ cd server
    $ python3 -m venv env
    $ source env/bin/activate
    (env)$ pip install -r dependencies.txt
    (env)$ python app.py
    ```

   **It will be live at** [http://localhost:5000](http://localhost:5000)

2. Run the Vue web app in a separate terminal:

    ```sh
    $ cd web
    $ npm install
    $ npm run serve
    ```

    **It will be live at** [http://localhost:8080](http://localhost:8080)
