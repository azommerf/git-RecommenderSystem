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

    # Home page
    @app.route("/")
    def home():
        return render_template('home.html')

    # Cockpit page
    @app.route("/cockpit")
    def cockpit():
        return render_template('cockpit.html')

    # Download page showing success/failure message of download
    @app.route("/cockpit/download", methods=['POST'])
    def choose_dataset():
        _data_url = request.form["_data_url"] # Save dataset
        print("\nDownload process started for the following file: "+_data_url)
        _success_msg = rs.data_download(_data_url)
        print(_success_msg)
        return render_template('dataset.html', msg=_success_msg)

    # DataFrame page showing if Pandas DataFrame creating was successful or not
    @app.route("/cockpit/dataframe", methods=['POST'])
    def create_dataframe():
        _data_url = request.form["_data_url"] # Save dataset
        print("\nCreating dataframe from the following file: "+_data_url.split('/')[-4])
        
        # Making df global because it is used in hole application
        # Sometimes not recommended, but here it brings much more
        # clarity since we are using only one dataframe for the
        # whole application
        global df
        df, msg, err = rs.data_frame(_data_url)

        if not err:
            print(df.head())
            print("...saving dataframe as csv...\n...printing dataframe to HTML...")
            # df.to_csv("program/data/df.csv", sep=',', index=False, encoding="utf-8")
            # print("CSV file created.")
            button_msg = "Continue with step 3"

            return render_template('dataframe.html', msg=msg, data=df.head().to_html(), button_msg=button_msg)
        else:
            button_msg = "Go back to cockpit"
            return render_template('dataframe.html', msg=msg, data=df, button_msg=button_msg)

    # KNN page showing if creating sparse matrix from DataFrame successfull or not
    @app.route("/cockpit/KNN", methods=['POST'])
    def fit_KNN():
        print("\n...Reading the dataframe as csv...")
        # df = pd.read_csv("program/data/df.csv", sep=',', encoding="utf-8")
        print(df.head())
        
        # Same intuition as in df: since we are only using one
        # data set at a time in this application, we will
        # make the sparse matrix and the product indices
        # global for more clarity in the code.
        global df_csr
        global prodUnique_indexed
        global prodUnique_reverseIndexed

        print("...creating sparse matrix...")
        df_csr, msg, prodUnique_indexed, prodUnique_reverseIndexed = rs.data_KNN(df)

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
        algorithm = request.form["_algorithm"]

        # Load pickled variables needed
        # print("\n...Loading pickled files...")
        # with open("./program/data/prodUnique_indexed.pickle","rb") as pkl:
        #     prodUnique_indexed = pickle.load(pkl)
        
        # with open("./program/data/prodUnique_reverseIndexed.pickle","rb") as pkl:
        #     prodUnique_reverseIndexed = pickle.load(pkl)

        try:
            prodUnique_indexed[prod_id]
            error_prod = False
        except:  
            error_prod = True 
        
        if not error_prod:
            # print("...loading dataframe...")
            # df = pd.read_csv("program/data/df.csv", sep=',', encoding="utf-8")
            # print("...loading sparse matrix...")
            # df_csr = load_npz("./program/data/df_csr.npz")

            print("You chose the following product: {}".format(prod_id))
            print("...making recommendations...")
            recommendations, total_stars, total_reviews, products, msg = rs.data_recommender(algorithm, metric, prod_id, prodUnique_indexed, prodUnique_reverseIndexed, df_csr, df)
            print("Recommendations: {}".format(recommendations))
            print("Product IDs: {}".format(products))
            print("Total number of stars: {}".format(total_stars))

            return render_template('recommender2.html',\
                                    recommendations=recommendations,\
                                    msg=msg, prod_id=prod_id,\
                                    metric=metric,\
                                    algorithm=algorithm,\
                                    total_stars=total_stars,\
                                    total_reviews=total_reviews,\
                                    products=products)
        else:
            msg = "\nUnfortunately this product ID was not found in the data base. Please search for another product ID."
            return render_template('recommender3.html', msg=msg)

    app.run(port=port, debug=False)
    return app
