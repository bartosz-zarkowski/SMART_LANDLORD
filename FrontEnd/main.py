from flask import Flask, render_template
import auth
import mainApp

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="aajuyfgkargargyerghaiolhgfkiareuhgliauerhgoiauhgoliudztrgholsiutrhgsiuhtgiud",
    )

app.register_blueprint(auth.bp)
app.register_blueprint(mainApp.bp)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('home.html')


# make url_for('index') == url_for('blog.index')
# in another app, you might define a separate main index here with
# app.route, while giving the blog blueprint an url_prefix, but for
# the tutorial the blog will be the main index
app.add_url_rule("/", endpoint="landing")


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
