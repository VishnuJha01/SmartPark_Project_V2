from flask import Flask
from application.model import db, User
from application.routes import routes
from application.security import jwt
from flask_cors import CORS
from application.celery_init import celery_init_app
from celery.schedules import crontab
from application.tasks import *
from application.cache import cache

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
app.config.update({
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": "localhost",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_DEFAULT_TIMEOUT": 5
})


db.init_app(app)
jwt.init_app(app)
CORS(app)
celery = celery_init_app(app)
cache.init_app(app)

celery.autodiscover_tasks()


@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute = '*/2'),
        monthly_parking_report.s(),
    )

# ---------------------- ADMIN CREATION ----------------------
def create_admin():
    if not User.query.filter_by(email='Vishnu@parking.com').first():
        admin = User(
            email='Vishnu@parking.com',
            password='123',
            fullname='Vishnu Kumar Jha',
            address='Admin HeadQuarter',
            pin_code='846002',
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

# ---------------------- RUN ----------------------

with app.app_context():
    db.create_all()
    create_admin()

routes(app)

if __name__ == '__main__':
    app.run(debug=True)