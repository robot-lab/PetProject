import os

from backend import create_app
os.environ.setdefault('FLASK_ENV', 'development')


if __name__ == '__main__':
  env_name = os.getenv('FLASK_ENV')
  print(env_name)
  app = create_app(env_name)
  app.run(port=8080)