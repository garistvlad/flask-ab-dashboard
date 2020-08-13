from flask import Blueprint
from flask import abort, redirect, url_for, render_template, flash, request
from flask_login import login_required

from .forms import ABExperimentForm, ABOptionForm, UserForm, App
from models import ABExperiment, ABOption, User
from main import db


bp = Blueprint(
    "admin",
    __name__
)


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    return redirect(url_for("ab.index"))


@bp.route("/<exp_name>", methods=['GET', 'POST'])
@login_required
def edit_experiment(exp_name):

    exp = ABExperiment.query.filter_by(name=exp_name).first()
    if exp is None:
        abort(404)
    
    apps = App.query.all()
    test_options = [i for i in exp.options if not i.is_control_group]
    control_options = [i for i in exp.options if i.is_control_group]

    form = ABExperimentForm(request.form)
    if form.validate_on_submit():
        # save user to DB:
        exp.app_id = form.app.data
        exp.name = form.exp_name.data
        exp.description = form.description.data
        exp.start_date = form.start_date.data
        if form.end_date.data:
            exp.end_date = form.end_date.data
        
        db.session.add(exp)
        # first, delete all options
        ABOption.query.filter_by(experiment_id=exp.id).delete()
        db.session.commit()

        # control options:
        for i in (form.option_control1.data, form.option_control2.data, form.option_control3.data):
            # if data in form filled:
            if i:
                option_i = ABOption(name=i, experiment_id=exp.id, is_control_group=True)
                db.session.add(option_i)
                db.session.commit()
        # test options
        for i in (form.option_test1.data, form.option_test2.data, form.option_test3.data):
            # if data in form filled:
            if i:
                option_i = ABOption(name=i, experiment_id=exp.id, is_control_group=False)
                db.session.add(option_i)
                db.session.commit()

        db.session.commit()
        flash(f"[{exp.name}]`s changes saved", category="success")
        return redirect(url_for("ab.detail", exp_name=exp.name))
    
    return render_template(
        "admin/edit_experiment.html",
        exp=exp,
        form=form,
        apps=apps,
        test_options=test_options,
        control_options=control_options
    )
