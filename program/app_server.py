import os
from flask import Flask, request, render_template, url_for, session
import subprocess
import program.app_modules as rs # rs stands for recommender system
import random, threading, webbrowser
import pandas as pd
import pickle
import webbrowser
from scipy.sparse import load_npz

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
        _success_msg = rs.data_download(_data_url)
        print(_success_msg)
        return render_template('dataset.html', msg=_success_msg)

    @app.route("/cockpit/dataframe", methods=['POST'])
    def create_dataframe():
        _data_url = request.form["_data_url"] # Save dataset
        print("\nCreating dataframe from the following file: "+_data_url.split('/')[-4])
        df, msg = rs.data_frame(_data_url)
        # session['df'] = df
        print(df.head())
        print("...saving dataframe as csv...\n...printing dataframe to HTML...")
        df.to_csv("program/data/df.csv", sep=',', index=False, encoding="utf-8")
        print("CSV file created.")
        return render_template('dataframe.html', msg=msg, data=df.head().to_html())

    @app.route("/cockpit/KNN", methods=['POST'])
    def fit_KNN():
        print("\n...Reading the dataframe as csv...")
        df = pd.read_csv("program/data/df.csv", sep=',', encoding="utf-8")
        print(df.head())
        msg = rs.data_KNN(df)

        return render_template('KNN.html', msg=msg)

    @app.route("/cockpit/reset", methods=['POST'])    
    def reset():
        msg = rs.data_reset(filetype="all")
        return render_template('reset.html', msg=msg)
        
    @app.route("/recommender")    
    def recommender():
        return render_template('recommender1.html')

    @app.route("/recommender/1", methods=['POST'])    
    def goAmazon():
        _amazon_url = request.form["_amazon_url"]
        webbrowser.open_new_tab(_amazon_url)
        return recommender()

    @app.route("/recommender/2", methods=['POST'])
    def recommend_prod():
        prod_id = request.form["_product_id"]
        metric = request.form["_metric"]
        print("Metric: {}".format(metric))

        # Load pickled variables needed
        print("\n...Loading pickled files...")
        with open("./program/data/prodUnique_indexed.pickle","rb") as pkl:
            prodUnique_indexed = pickle.load(pkl)
        
        with open("./program/data/prodUnique_reverseIndexed.pickle","rb") as pkl:
            prodUnique_reverseIndexed = pickle.load(pkl)

        print("\n...loading csv file...")
        df_csr = load_npz("./program/data/df_csr.npz")

        print("You chose the following product: {}".format(prod_id))
        print("\n...making recommendations...")
        recommendations, msg = rs.data_recommender(metric, prod_id, prodUnique_indexed, prodUnique_reverseIndexed, df_csr)
        
        return render_template('recommender2.html', recommendations=recommendations, msg=msg, metric=metric)

    app.run(port=port, debug=False)
    return app
