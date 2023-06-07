from flask import Flask
from sqlalchemy import *
from dotenv import load_dotenv
from flask_cors import CORS
import os
from sqlalchemy.orm import sessionmaker
from Model.models import Base

app = Flask(__name__)
cors = CORS(app)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)



if __name__ == '__main__':
    #imported here becouse the circular error
    from Routes.questions import questions_bp
    app.register_blueprint(questions_bp)

    from Routes.Group import group_bp
    app.register_blueprint(group_bp)

    from Routes.Answers import answer_bp
    app.register_blueprint(answer_bp)

    from Routes.Game import game_bp
    app.register_blueprint(game_bp)

    from Routes.Authentication.Authentication import auth_bp
    app.register_blueprint(auth_bp)

    app.run(debug=True, host='127.0.0.1', threaded=True)