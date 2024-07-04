from flask_sqlalchemy import SQLAlchemy
# ERROR [flask_migrate] Error:
# The current Flask app is not registered with this 'SQLAlchemy' instance.
# Did you forget to call 'init_app',
# or did you create multiple 'SQLAlchemy' instances?

db = SQLAlchemy()