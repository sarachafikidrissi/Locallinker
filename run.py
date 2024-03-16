""" This is a model that runs our application"""

from application import app
import os # Import the os module for environment variables


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)