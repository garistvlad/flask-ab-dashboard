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
        
    return render_template("ab/ab_list.html", exp_pagination=exp_pagination, q=q, active_link="home")


@bp.route("/<exp_name>")
@bp.route("/<exp_name>/index")
@login_required
def detail(exp_name):
    """ Detail main page for selected experiment """
    exp = ABExperiment.query.filter_by(name=exp_name).first()
    if exp is None:
        abort(404)
    
    return render_template("ab/ab_item.html", exp=exp, active_link="info")


@bp.route("/<exp_name>/funnel")
@login_required
def detail_funnel(exp_name):
    """ Detail main page for selected experiment """
    exp = ABExperiment.query.filter_by(name=exp_name).first()
    if exp is None:
        abort(404)
    
    return render_template("ab/ab_item_funnel.html", exp=exp, active_link="funnel")


@bp.route("/<exp_name>/users")
@login_required
def detail_users(exp_name):
    """ Detail main page for selected experiment """
    exp = ABExperiment.query.filter_by(name=exp_name).first()
    if exp is None:
        abort(404)
    
    return render_template("ab/ab_item_users.html", exp=exp, active_link="users")


@bp.route("/<exp_name>/stats/<period>", methods=['GET', 'POST'])
@login_required
def detail_stats(exp_name, period='all'):
    """ Detail main page for selected experiment """
    exp = ABExperiment.query.filter_by(name=exp_name).first()
    if exp is None:
        abort(404)
    return render_template("ab/ab_item_stats.html", exp=exp, active_link="stats", period=period)
