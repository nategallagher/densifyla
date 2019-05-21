from app import app

@app.route('/')
def index():
    return "<h3>Hello World!</h3>"

