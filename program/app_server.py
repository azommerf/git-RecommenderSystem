import os
from flask import Flask, request, render_template, url_for, session
import subprocess
from program.app_modules import data_download, data_frame, data_KNN, data_reset
import random, threading, webbrowser
import pandas as pd
import pickle

def main():
    app = Flask(__name__)

    # Automatically open in web browser
    port = 5000 + random.randint(0, 999)
    home_url = "http://127.0.0.1:{0}".format(port)
    threading.Timer(1.25, lambda: webbrowser.open(home_url) ).start()

    def return_function(parameter):
        return parameter

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
        return render_template('dataset.html', msg=_success_msg)

    @app.route("/cockpit/dataframe", methods=['POST'])
    def create_dataframe():
        _data_url = request.form["_data_url"] # Save dataset
        print("\nCreating dataframe from the following file: "+_data_url.split('/')[-4])
        df, msg = data_frame(_data_url)
        # session['df'] = df
        print(df.head())
        print("Saving dataframe as csv. Printing dataframe to HTML.")
        df.to_csv("program/data/df.csv")
        print("CSV file created.")
        return render_template('dataframe.html', msg=msg, data=df.head().to_html())

    @app.route("/cockpit/KNN", methods=['POST'])
    def fit_KNN():
        print("\nReading the dataframe as csv.")
        df = pd.read_csv("program/data/df.csv")
        print(df.head())
        custNo, prodUnique_indexed, prodUnique_reverseIndexed, df_csr, msg = data_KNN(df)

        # Pickle variables for later use
        pickle_out = open("./program/data/custNo.pickle", "wb")
        pickle.dump(custNo, pickle_out)
        pickle_out.close()

        pickle_out = open("./program/data/prodUnique_indexed.pickle", "wb")
        pickle.dump(prodUnique_indexed, pickle_out)
        pickle_out.close()

        pickle_out = open("./program/data/prodUnique_reverseIndexed.pickle", "wb")
        pickle.dump(prodUnique_reverseIndexed, pickle_out)
        pickle_out.close()

        df.to_csv("program/data/df_csr.csv")

        return render_template('KNN.html', msg=msg)

    @app.route("/cockpit/reset", methods=['POST'])    
    def reset():
        msg = data_reset(filetype="all")
        return render_template('reset.html', msg=msg)
        

    app.run(port=port, debug=False)
    
    return app
