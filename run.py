from application import app


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, port=5000)