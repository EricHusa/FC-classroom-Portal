from portal.app import create_app


if __name__ == '__main__':
    app = create_app('PORTAL')
    app.run()
