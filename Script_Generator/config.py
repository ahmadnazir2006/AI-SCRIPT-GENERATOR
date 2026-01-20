import os
class config:
            SECRET_KEY=os.environ.get('SECRET_KEY')
            uri = os.getenv("DATABASE_URL")
            if uri and uri.startswith("postgres://"):
                uri = uri.replace("postgres://", "postgresql://", 1)
            SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///site.db'

            MAIL_SERVER= 'smtp.gmail.com'
            MAIL_PORT = 587
            MAIL_USE_TLS = True
            MAIL_USE_SSL = False
            MAIL_USERNAME = os.environ.get('EMAIL_USER')
            MAIL_PASSWORD= os.environ.get('EMAIL_PASS')
