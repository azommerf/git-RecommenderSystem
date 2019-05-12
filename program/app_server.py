from flask import Flask, request, render_template, url_for
import subprocess
from program.app_modules import data_download, data_frame
import random, threading, webbrowser
import pandas as pd

def main():
    app = Flask(__name__)

    # Automatically open in web browser
    port = 5000 + random.randint(0, 999)
    home_url = "http://127.0.0.1:{0}".format(port)
    threading.Timer(1.25, lambda: webbrowser.open(home_url) ).start()

    @app.route("/")
    def home():
        return render_template('home.html')

    @app.route("/cockpit")
    def cockpit():
        return render_template('cockpit.html')


    @app.route("/cockpit/download", methods=['POST'])
    def choose_dataset():
        _data_url = request.form["_data_url"] # Save dataset
        print("\nDownload process started for the following file: "+_data_url)
        _success_msg = data_download(_data_url)
        print(_success_msg)
        # return dataset(_success_msg)
        return render_template('dataset.html', msg=_success_msg)

    @app.route("/cockpit/dataframe", methods=['POST'])
    def create_dataframe():
        _data_url = request.form["_data_url"] # Save dataset
        print("\nDownload process started for the following file: "+_data_url[0:-3])
        df, msg = data_frame(_data_url)
        df.head()
        return render_template('dataframe.html', msg=msg)




    app.run(port=port, debug=False)
    
    return app
