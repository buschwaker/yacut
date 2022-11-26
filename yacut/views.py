from flask import abort, redirect, render_template

from . import app, db
from .forms import UrlForm
from .models import URL_map


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UrlForm()
    url_result = False
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data
        short = short if short != '' else None
        url = URL_map(
            original=original,
            short=short
        )
        db.session.add(url)
        db.session.commit()
        url_result = url.short
    return render_template('index.html', form=form, url_result=url_result)


@app.route('/<string:postfix>')
def go_to_original(postfix):
    url = URL_map.query.filter_by(short=postfix).first()
    if not url:
        abort(404)
    return redirect(url.original)
