from flask import Flask, render_template, abort
from datetime import datetime


app = Flask(__name__, static_url_path='')

    
@app.route('/<page>')
def render(page):
    valid_templates = ['index', 'classes', 'instructors', 'chen', 'yang', 'resources', 'czl2016']
    template = page.lower()
    if template in valid_templates:
        current_year = datetime.now().year
        return render_template(template + '.html', current_year=current_year)
    abort(404)


@app.route('/')
def root():
    return render('index')


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)

