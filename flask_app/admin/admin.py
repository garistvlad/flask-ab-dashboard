from flask import Blueprint
from flask import redirect, url_for
from flask_login import login_required


bp = Blueprint(
    "admin",
    __name__
)


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    return redirect(url_for("ab.index"))
