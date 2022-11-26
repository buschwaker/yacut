from flask import abort, flash, redirect, request, render_template, url_for
from sqlalchemy.exc import SQLAlchemyError

from . import app
from .exceptions import ShortUrlGenerateError
from .forms import UrlForm
from .models import URL_map


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UrlForm()
    if request.method == 'GET' or not form.validate_on_submit():
        return render_template('index.html', form=form)
    original = form.original_link.data
    short = form.custom_id.data
    short = short if short != '' else None
    try:
        url = URL_map.create(original=original, short=short)
    except (SQLAlchemyError, ShortUrlGenerateError) as error:
        flash(str(error))
        return render_template('index.html', form=form)
    url_result = url_for('go_to_original', postfix=url.short, _external=True)
    return render_template('index.html', form=form, url_result=url_result)


@app.route('/<string:postfix>')
def go_to_original(postfix):
    url = URL_map.get_url_by_param(short=postfix)
    if not url:
        abort(404)
    return redirect(url.original)
