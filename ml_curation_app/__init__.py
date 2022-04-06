import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from sqlalchemy.orm import relationship,scoped_session,sessionmaker

from .config import config_by_name

db = SQLAlchemy() # 변수를 다른 파일에서 불러올 수 있도록 create_app 위에 선언함
migrate = Migrate()
bootstrap = Bootstrap()

def create_app(config=None):
    app = Flask(__name__,static_url_path='', 
    static_folder='web/static',
    template_folder='web/templates')
    """
    app.config.from_pyfile('config.py')
    참고
    - https://velog.io/@sangmin7648/MariaDB%EB%A5%BC-Flask-API%EC%97%90-%EC%97%B0%EA%B2%B0%ED%95%98%EA%B8%B0
    app.config.from_object(config_by_name[config_name])
    """
    
    app.config.from_object(config_by_name['dev'])

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap = Bootstrap(app)

    from ml_curation_app.views.main_views import main_route_bp
    """
    circular import 문제를 해결하기 위해  create_app 내부에서 route 함수를 불러온다
    """
    app.register_blueprint(main_route_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debuig=True)
