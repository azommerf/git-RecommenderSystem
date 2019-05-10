from flask import Flask, request, render_template
import subprocess
from download import download_main

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/cockpit")
def cockpit():
    return render_template('cockpit.html')

@app.route("/dataset2")
def dataset(_success_msg):
        _success_msg = _success_msg
        return render_template('dataset.html', msg=_success_msg)

@app.route("/dataset1", methods=['POST'])
def choose_dataset():
        _data_url = request.form["_data_url"] # Save dataset
        print("\nDownload process started for the following file: "+_data_url)
        _download_msg = "...downloading..."    
        render_template('dataset.html', msg=_download_msg)
        _success_msg = download_main(_data_url)
        print(_success_msg)
        return dataset(_success_msg)


if __name__ == "__main__":
    app.run(debug='True')