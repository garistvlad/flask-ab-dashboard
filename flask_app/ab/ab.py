from flask import Blueprint
from flask import abort, render_template, request
from flask_login import login_required
from models import ABExperiment, App


bp = Blueprint(
    "ab",
    __name__
)


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    """ List of AB experiments """
    # parse get params:
    page = request.args.get("page", default=1, type=int)
    q = request.args.get("q", default="")
    exp_pagination = ABExperiment.query \
        .join(App, ABExperiment.app_id == App.id) \
        .filter(
            (ABExperiment.name.like(f"%{q}%")) | (App.name.like(f"%{q}%"))
        ) \
        .order_by(ABExperiment.start_date.desc(), ABExperiment.name) \
        .limit(100).from_self() \
        .paginate(page=page, per_page=10)
        
    return render_template("ab/ab_list.html", exp_pagination=exp_pagination, q=q)


@bp.route("/<exp_name>")
@login_required
def detail(exp_name):
    """ Detail main page for selected experiment """
    exp = ABExperiment.query.filter_by(name=exp_name).first()
    if exp is None:
        abort(404)
    
    return render_template("ab/ab_item.html", exp=exp)
