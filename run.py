from application import app
import os


if __name__ == '__main__':
    # with app.app_context():
    #     app.run(host="0.0.0.0", port=5000)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)