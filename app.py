from . import app    # For application discovery by the 'flask' command.

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/test")
def test():
    return "Hello, test!"

# Also, if you want to run the development server on a different IP address or port,
# use the host and port command-line arguments, as with --host=0.0.0.0 --port=80.

"""
How to:
Implement an API endpoint that returns a static file.
      In the static folder, create a JSON data file named data.json
      For this purpose, the Flask object contains a built-in method, send_static_file,
      which generates a response with a static file contained within the app's static folder.

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

"""