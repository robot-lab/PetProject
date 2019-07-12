import os

from backend import create_app

os.environ.setdefault('FLASK_ENV', 'development')


if __name__ == '__main__':
    env_name = os.getenv('FLASK_ENV')
    port = int(os.getenv('PORT', 8080))
    app = create_app(env_name)
    app.run(host='0.0.0.0', port=port)
