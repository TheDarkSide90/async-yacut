import re
import random
from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import LinkForm, FilesForm
from .models import URLMap
from .yandex_disk import upload_file, get_download_link
from .constants import CHARS, REGEX
from settings import GENERATE_RANGE, GENERATE_SHORT_MAX_LENGTH


def get_unique_short_id():
    for _ in range(GENERATE_RANGE):
        short_id = ''.join(
            random.choice(CHARS)
            for _ in range(GENERATE_SHORT_MAX_LENGTH)
        )
        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id
    raise RuntimeError("Не удалось сгенерировать уникальный код")


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if custom_id:
            if not re.fullmatch(REGEX, custom_id):
                flash(
                    'Недопустимый формат короткой ссылки.',
                    'info'
                )
                return render_template(
                    'cut.html',
                    form=form
                )
            short = custom_id
        else:
            short = get_unique_short_id()
        if short == 'files':
            flash('Предложенный вариант короткой ссылки уже существует.',
                  'info')
            return render_template('cut.html', form=form)
        if URLMap.query.filter_by(short=short).first() is not None:
            flash('Предложенный вариант короткой ссылки уже существует.',
                  'info')
            return render_template('cut.html', form=form)
        url = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url)
        db.session.commit()

        short_url = url_for(
            'redirect_view',
            short=short,
            _external=True
        )

        flash('Ваша новая ссылка готова:', 'info')
        flash(short_url, 'link')
        return render_template('cut.html', form=form, short_url=url.short)
    return render_template('cut.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def upload():
    form = FilesForm()

    if form.validate_on_submit():
        for file in form.files.data:
            filename = file.filename
            disk_path = await upload_file(
                file,
                filename
            )
            await get_download_link(disk_path)
            short = get_unique_short_id()
            url = URLMap(
                original=disk_path,
                short=short,
                filename=filename
            )
            short_url = url_for(
                'redirect_view',
                short=short,
                _external=True
            )
            db.session.add(url)
            flash((file.filename, short_url), 'info')
        db.session.commit()
    return render_template(
        'upload.html',
        form=form
    )


@app.route('/<string:short>')
async def redirect_view(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    if url.filename:
        download_url = await get_download_link(url.original)
        return redirect(download_url)
    return redirect(url.original)
