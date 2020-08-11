from flask import url_for
from flask_login import UserMixin
import json
from werkzeug.security import generate_password_hash, check_password_hash

from main import db
from main import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # is_admin = db.Column(db.Boolean)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)


class App(db.Model):
    __tablename__ = "app"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    experiments = db.relationship('ABExperiment', backref='app')

    def __repr__(self):
        return f'<App: {self.name}>'


class ABExperiment(db.Model):
    __tablename__ = "experiment"
    # unique constraint on multiple fields:
    __table_args__ = (db.UniqueConstraint('app_id', 'name', name="unique_constraint_app_exp"), )

    id = db.Column(db.Integer, primary_key=True)
    app_id = db.Column(db.Integer, db.ForeignKey("app.id"))
    name = db.Column(db.String(120), index=True)
    description = db.Column(db.Text)
    metrics = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    options = db.relationship('ABOption', backref='experiment') # cascade="all, delete-orphan"

    @property
    def metrics_json(self):
        return json.loads(self.metrics) if self.metrics is not None else dict()

    @property
    def clean_name(self):
        clean_name = " ".join(
            [i.capitalize() for i in self.name.split("_") if i not in ("exp", "ios", "android")]
        )
        return clean_name

    @property
    def sorted_options(self):
        options = sorted(self.options, key=lambda x: (-x.is_control_group, x.name))
        return [i.name for i in options]

    def is_period_data_exists(self, period):
        """ Chech, wether data exists for requested period (cnt_users > 0 for all options) """
        return all([i > 0 for i in self.metrics_json.get(f"cnt_users_{period}").values()])

    def get_user_donut_svg_url(self):
        return f'img/ab/{self.name}/user_donut.svg'
    
    def get_user_dynamics_svg_url(self):
        return f'img/ab/{self.name}/user_dynamics.svg'

    def get_pdf_and_confint_svg_url(self, col_name="conversion", period="all"):
        return f'img/ab/{self.name}/pdf_{col_name}_{period}.svg'

    def get_valueset_total(self, col_name='cnt_users'):
        """ Format for further barplot_total, being rendered with chart.js """
        if not self.metrics_json:
            return
        valueset = {i: [] for i in self.sorted_options}
        for period in ["1d", "7d", "30d", "all"]:
            tmp = self.metrics_json[f"{col_name}_{period}"]
            for option in valueset.keys():
                valueset[option].append(tmp[option])
        return valueset

    def __repr__(self):
        return f'<Exp: {self.name}>'


class ABOption(db.Model):
    __tablename__ = "option"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    is_control_group = db.Column(db.Boolean) # base, ...
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'))

    def __repr__(self):
        return f'<Option: {self.name}>'
