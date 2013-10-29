import flask

def create_app(name, id, key, debug=False):

    app = flask.Flask(__name__)
    app.config.update(dict(DEBUG=debug, SECRET_KEY=key))

    @app.route(name)
    def index():
        return flask.render_template("index.html")
    
    @app.route(name + '/accept')
    def accept():
        assign_response(id, 'accept')
        return flask.render_template("accept.html")

    @app.route(name + '/decline', methods=['GET', 'POST'])
    def decline():
        assign_response(id, 'decline')
        error, flash = None, None
        if flask.request.method == 'POST':
            date = flask.request.form['date']
            days = [str(i + 1).zfill(2) for i in range(31)]
            months = [str(i + 1).zfill(2) for i in range(12)]
            years = [str(i + 1).zfill(2) for i in range(100)]
            if (len(date) != 6) | (date[:2] not in days) | \
                (date[2:4] not in months) | (date[6:] not in years):
                error = 'Invalid format - DDMMYY'
            else:
                assign_response(id, 'decline', gone=date)
                flash = 'No presenting until %s' % date
        return flask.render_template("decline.html", error=error, flash=flash)

    @app.route(name + '/leave')
    def leave():
        assign_response(id, 'remove')
        return flask.render_template("leave.html")

    return app


if __name__ == '__main__':

    debug = True
    key = 'development key'

    name = '/katch'
    app = create_app(name, id, key, debug)
    app.run()
