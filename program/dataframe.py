import pandas as pd # For handling dataframe
import numpy as np # For sparse grid

from scipy.sparse import csr_matrix # Sparse matrix
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors

def dataframe_main(url):

    filename = url.split('/')[-1]
    workingdir = os.path.abspath('')
    datadir = "program/data" # Directory where data is stored
    filepath_tsvgz = os.path.join(workingdir, datadir, filename)
    filepath_tsv = filepath_tsvgz[0:-3]

    # Create pandas dataframe
    print()
    print("\n...creating dataframe...")
    df = pd.read_csv(filepath_tsv, delimiter='\t', encoding="utf-8", error_bad_lines=False)

    # Write dataframe to excel
    # df = df.applymap(lambda x: x.encode('unicode_escape').
    #              decode('utf-8') if isinstance(x, str) else x)
    # df.to_excel("data.xlsx")

    msg = "Data frame created successfully!"
    return