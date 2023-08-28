from flask import Flask, render_template, redirect, send_file, url_for, request
import subprocess
import os
import threading
import time
from flask_sslify import SSLify
from flask_sse import sse

app = Flask(__name__)
sslify = SSLify(app)
app.config["REDIS_URL"] = "redis://localhost"  # Set the Redis URL, you can customize this if needed
app.register_blueprint(sse, url_prefix='/stream')

current_directory = os.path.dirname(os.path.abspath(__file__))
server_path = os.path.join(current_directory, 'files', 'server.crt')
key_path = os.path.join(current_directory, 'files', 'server.key')
port = 4433

# home page (Page 1)
@app.route('/')
def home():
    return render_template('home.html', port=port)

# test certificate page (Page 2)
@app.route('/test_certificate')
def test_certificate():
    # Remove the call to openssl s_server
    return render_template('index.html')

# certificate validation page (Page 3)
@app.route('/validate_certificate')
def validate_certificate():
    return render_template('index.html')

@app.route('/open_new_tab')
def open_new_tab():
    # Retrieve the port number from the cookie
    # port = request.cookies.get('port')
    # Open the new tab with the correct URL
    return redirect(f"/browser_script.html?port={5000}")

@app.route('/browser_script.html')
def get_browser_script():
    # Return the "browser_script.html" file
    return send_file("/home/pinata/PRE/pylstar-tls/WebAppV3/files/browser_script.html")

# Define the /start_inference endpoint to handle the POST request
@app.route('/start_inference', methods=['POST'])
def start_inference():
    try:
        # Extract the port from the JSON data in the request body

        cmd = "python3 $PWD/../src/infer_client.py -L 127.0.0.1:5000 -C good:$PWD/files/server.crt:$PWD/files/server.key:DEFAULT -S tls13 -E BDist:1 -o $PWD/files --timeout 0.1"
        print(cmd)
        subprocess.Popen(cmd, shell=True)
        # Return a success response if the inference process is started successfully
        return {"message": "Inference process started successfully."}, 200
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {"error": "Failed to start inference process."}, 500


if __name__ == '__main__':
    app.run(port=port, debug=True, ssl_context=(server_path, key_path))
