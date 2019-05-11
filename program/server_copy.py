from flask import Flask, request, render_template, url_for
import subprocess
from program.download import download_main
import random, threading, webbrowser

def main():
    app = Flask(__name__)

    port = 5000 + random.randint(0, 999)
    home_url = "http://127.0.0.1:{0}".format(port)
    threading.Timer(1.25, lambda: webbrowser.open(home_url) ).start()

    @app.route("/")
    def home():
        return render_template('home.html')

    @app.route("/cockpit")
    def cockpit():
        return render_template('cockpit.html')


    @app.route("/download1", methods=['POST'])
    def choose_dataset():
        _data_url = request.form["_data_url"] # Save dataset
        print("\nDownload process started for the following file: "+_data_url)
        _download_msg = "...downloading..."
        render_template('dataset.html', msg=_download_msg)
        _success_msg = download_main(_data_url)
        print(_success_msg)
        return dataset(_success_msg)

    @app.route("/download2")
    def dataset(_success_msg):
        _success_msg = _success_msg
        return render_template('dataset.html', msg=_success_msg)

    # @app.route("/dataframe1", methods=['POST'])
    # def dataframe1():
  

    # @app.route("/dataframe2")
    # def dataframe2(_success_msg):


    app.run(port=port, debug=False)
    
    return app
