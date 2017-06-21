from flask import Flask, render_template
app = Flask(__name__)
wsgi_app = app.wsgi_app


@app.route('/')
def main():
    return render_template("index.html")

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(HOST, PORT, debug=True)
