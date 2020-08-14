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


@bp.route("/manage_users", methods=['GET', 'POST'])
@login_required
def manage_users():
    # TODO
    return redirect(url_for("ab.index", active_link="manage_users"))


@bp.route("/delete_experiment/<exp_name>", methods=['GET', 'POST'])
@login_required
def delete_experiment(exp_name):
    exp = ABExperiment.query.filter_by(name = exp_name).first()
    if exp is None:
        flash(f"Experiment `{exp_name}` not found", category="danger")
        return redirect(url_for("ab.index"))
    
    db.session.delete(exp)
    db.session.commit()
    flash(f"Experiment `{exp_name}` has been deleted", category="success")

    return redirect(url_for("ab.index"))


@bp.route("/create_experiment", methods=['GET', 'POST'])
@login_required
def create_experiment():
    form = ABExperimentForm(request.form)
    apps = App.query.all()

    if form.validate_on_submit():
        exp = ABExperiment.query.filter_by(name = form.exp_name.data).first()
        if exp is not None:
            flash(f"Experiment `{exp.name}` already exist. Choose another name or edit the existing exp.", category="danger")
            return render_template("admin/create_experiment.html", form=form, apps=apps, active_link="create_experiment")

        exp = ABExperiment(
            app_id = form.app.data,
            name = form.exp_name.data,
            description = form.description.data,
            start_date = form.start_date.data
        )
        if form.end_date.data:
            exp.end_date = form.end_date.data
        
        db.session.add(exp)
        db.session.commit()

        # select experiment from DB, just after being saved:
        exp = ABExperiment.query.filter_by(name = exp.name, app_id = exp.app_id).first()
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
        
        flash(f"Experiment `{exp.name}` has been created. Check this out...", category="success")
        return redirect(url_for("admin.edit_experiment", exp_name = exp.name))
    
    return render_template("admin/create_experiment.html", form=form, apps=apps, active_link="create_experiment")



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
        return redirect(url_for("ab.index"))
    
    return render_template(
        "admin/edit_experiment.html",
        exp=exp,
        form=form,
        apps=apps,
        test_options=test_options,
        control_options=control_options
    )
