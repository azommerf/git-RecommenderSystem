import sys # For input/output to terminal
import os # For saving filepath
import requests # For requesting and downloading data set from URL
import gzip # For unzipping the data set
import shutil # For unzipping
import pandas as pd # For handling dataframe
import numpy as np # For sparse grid
from scipy.sparse import csr_matrix, save_npz, load_npz # Sparse matrix
from sklearn.neighbors import NearestNeighbors
import pickle
import webbrowser



def data_download(url):

    #################################################################################
    #  Prepare the data set from Amazon
    # Choose category here: https://s3.amazonaws.com/amazon-reviews-pds/tsv/index.txt

    filename = url.split('/')[-1]
    workingdir = os.path.abspath('')
    datadir = "program/data" # Directory where data is stored
    filepath_tsvgz = os.path.join(workingdir, datadir, filename)
    filepath_tsv = filepath_tsvgz[0:-3]

    def download_gz(url, filepath_tsvgz, filename):
        filepath_tsv = filepath_tsvgz[0:-3]
        # Check if data file already exists
        exists_tsvgz = os.path.isfile(filepath_tsvgz)
        if exists_tsvgz: print("\nFile already downloaded.")
        else:
            print("\nFile does not exist. Continue with download process.")
            print("\n{:^50}".format("...downloading the data..."))

            # Retrieve data from URL
            r = requests.get(url, stream=True)
            total_length = r.headers.get('content-length')

            with open(filepath_tsvgz, 'wb') as f:
                # Show download progress bar
                if total_length is None:
                    f.write(r.content)
                else:
                    downloaded = 0
                    total_length = int(total_length)
                    for data in r.iter_content(chunk_size=max(int(total_length/1000), 1024*1024)):
                        downloaded += len(data)
                        f.write(data)
                        done = int(50*downloaded/total_length)
                        sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                        sys.stdout.flush()

            print("\nDownloaded "+filename+" successfully.")

        # # Unzip file  
        # print("\n\nunzipping the file...")
        # with gzip.open(filepath_tsvgz, 'r') as f_in, open(filepath_tsv, 'wb') as f_out:
        #     shutil.copyfileobj(f_in, f_out)
        # print("\nFile decompressed successfully.")
        # # Delete zipped file
        # os.remove(filepath_tsvgz) # delete compressed data
        # print("Compressed file deleted successfully.")
        # print("File saved in the following location:\n{}".format(filepath_tsv))

    exists_tsvgz = os.path.isfile(filepath_tsvgz) # Check if data already exists
    # Execute download
    if not exists_tsvgz:
        download_gz(url, filepath_tsvgz, filename)
        msg = "Data downloaded successfully."
        return msg
    else: 
        msg = "File already exists. Continue with creating data frame."
        print(msg)
        return msg

def data_frame(url):

    #################################################################################
    # Create dataframe

    try:
        filename = url.split('/')[-1]
        workingdir = os.path.abspath('')
        datadir = "program/data" # Directory where data is stored
        filepath_tsvgz = os.path.join(workingdir, datadir, filename)
        filepath_tsv = filepath_tsvgz[0:-3]

        # Create pandas dataframe
        print()
        print("\n...creating dataframe...")
        # df = pd.read_csv(filepath_tsv, delimiter='\t', encoding="utf-8", error_bad_lines=False)

        usecols = ['customer_id','product_id','star_rating',]
        # dtype = {'star_rating':np.int32}
        df = pd.read_csv(filepath_tsvgz,\
                        delimiter='\t',\
                        encoding="utf-8",\
                        error_bad_lines=False,\
                        compression='gzip',\
                        # dtype=dtype,\
                        usecols=usecols)
        # Clean dataframe
        df = df[df['star_rating'].isin([0,1,2,3,4,5])]
        df.astype({'star_rating':int})

        msg = "Dataframe created successfully. Take a look at the first 5 entries: "
        err = False
        return df, msg, err

    except:
        msg = "Encountered an error while creating dataframe. Please try to go through step 1 again."
        df = ""
        err = True
        return df, msg, err


def data_KNN(df):
    #################################################################################
    # Nearest neighbors method
    # (1) Create sparse matrix with unique customer and unique item index and the corresponding star rating
    #    needed data: start_rating, product_id, customer_id
    # (2) Compute nearest neighbors

    try:

        # Calculate total number of products and customers (for range calculation)
        prodNo = len(set(df["product_id"])) # Number of products
        custNo = len(set(df["customer_id"])) # Number of customers
        print("Number of unique products: {}".format(prodNo))
        print("Number of unique customers: {}".format(custNo))

        # Get unique product and customer IDs and index them
        prodUnique_indexed = dict(zip(np.unique(df["product_id"]), list(range(prodNo))))
        custUnique_indexed = dict(zip(np.unique(df["customer_id"]), list(range(custNo))))
        prodUnique_reverseIndexed = dict(zip(list(range(prodNo)), np.unique(df["product_id"])))
        custUnique_reverseIndexed = dict(zip(list(range(custNo)), np.unique(df["customer_id"])))

        # Finally go through each row of dataframe and assign index 
        custIndex = [custUnique_indexed[i] for i in df["customer_id"]]
        prodIndex = [prodUnique_indexed[i] for i in df["product_id"]]

        # Create indexed matrix
        df_custIndex = pd.DataFrame(custIndex, columns=["custIndex"])
        df_prodIndex = pd.DataFrame(prodIndex, columns=["prodIndex"])
        df_indexed = pd.DataFrame(df["star_rating"], columns=["star_rating"])
        df_indexed.insert(0, "prodIndex", df_prodIndex)
        df_indexed.insert(0, "custIndex", df_custIndex)


        # Create the sparse matrix based on a matrix with dimensions:
        # (no. of unique products x no. of unique customres).
        # Description from official scipy documentation:
        # csr_matrix((data, (row_ind, col_ind)), [shape=(M, N)])
        # where data, row_ind and col_ind satisfy the relationship a[row_ind[k], col_ind[k]] = data[k].

        print("...creating sparse matrix...")
        df_csr = csr_matrix((df_indexed["star_rating"], (prodIndex, custIndex)), shape=(prodNo, custNo))

        # print("...storing number of customers...")
        # with open("./program/data/custNo.pickle", "wb") as pkl:
        #     pickle.dump(custNo, pkl, protocol=pickle.HIGHEST_PROTOCOL)
        # print("...storing indices...")
        # with open("./program/data/prodUnique_indexed.pickle", "wb") as pkl:
        #     pickle.dump(prodUnique_indexed, pkl, protocol=pickle.HIGHEST_PROTOCOL)
        # with open("./program/data/prodUnique_reverseIndexed.pickle", "wb") as pkl:
        #     pickle.dump(prodUnique_reverseIndexed, pkl, protocol=pickle.HIGHEST_PROTOCOL)
        # print("...storing sparse matrix...")
        # save_npz("./program/data/df_csr.npz", df_csr)

        msg = "\nPrepared the data for KNN model successfully."

        return df_csr, msg, prodUnique_indexed, prodUnique_reverseIndexed

    except: 

        msg = "\nError during KNN model fitting encountered."
        return msg


def data_reset(filetype):
    data_dir = "./program/data/"
    data_dir_ = os.listdir(data_dir)
    msg = "We cleaned the garbage for you."
    if filetype == "all":
        for file in data_dir_:
            if file.endswith(".pickle"):
                os.remove(os.path.join(data_dir,file))
            elif file.endswith(".csv"):
                os.remove(os.path.join(data_dir,file))
            elif file.endswith(".tsv"):
                os.remove(os.path.join(data_dir,file))
            elif file.endswith(".npz"):
                os.remove(os.path.join(data_dir,file))
        return msg
    elif filetype == "pickle":
        for file in data_dir_:
            if file.endswith(".pickle"):
                os.remove(os.path.join(data_dir,file))
        return msg
    elif filetype == "csv":
        for file in data_dir_:
            if file.endswith(".csv"):
                os.remove(os.path.join(data_dir,file))
        return msg
    elif filetype == "tsv":
        for file in data_dir_:
            if file.endswith(".tsv"):
                os.remove(os.path.join(data_dir,file))
        return msg
    elif filetype == "npz":
        for file in data_dir_:
            if file.endswith(".npz"):
                os.remove(os.path.join(data_dir,file))
        return msg
    else: return msg

def data_recommender(algorithm, metric, prod_id, prodUnique_indexed, prodUnique_reverseIndexed, df_csr, df):
    try:
        # Now we look at an example product "prod"

        prod_index = prodUnique_indexed[prod_id]
        print("\nUnique index for {}: {}".format(prod_id,prod_index))

        # From the sparse matrix we extract all rows that are related to prod1.
        # E.g. we look at all rows where a customer at least (!) reviewed B003VWJ2K8 
        prod_csr = df_csr[prod_index]

        amazon_url = "https://www.amazon.com/dp/"

        no_recommendations = 16
        NN_model = NearestNeighbors(metric=metric, algorithm=algorithm)
        NN_model.fit(df_csr)
        KNN = NN_model.kneighbors(prod_csr, no_recommendations) # Set number of suggestions

        recommendations = np.array([]) # For array with all recommended URLs
        products = np.array([]) # For array with all recommended product IDs
        total_stars = np.array([]) # For total number of stars per product
        total_reviews = np.array([]) # For total number of reviews per product
        for i in KNN[1][0]:
            prod_id = prodUnique_reverseIndexed[i]
            prod_url = amazon_url+prod_id
            print(prod_url)
            # webbrowser.open_new_tab(prod_url) # If you want to automatically open new tabs
            total_stars = np.append(total_stars, df.loc[df['product_id'] == prod_id, 'star_rating'].sum())
            total_reviews = np.append(total_reviews, len(df.loc[df['product_id'] == prod_id, 'star_rating']))
            products = np.append(products, prod_id)
            recommendations = np.append(recommendations, prod_url)

        msg = "These are the top {} recommendations:".format(no_recommendations-1, prod_id, metric)
        print("\n"+msg)
        return recommendations, total_stars, total_reviews, products, msg
    except:
        recommendations = np.array(["" "" "" "" "" ""])
        total_stars = np.array(["" "" "" "" "" ""])
        total_reviews = np.array(["" "" "" "" "" ""])
        products = np.array(["" "" "" "" "" ""])
        msg = "\nUnfortunately we encountered an error using the chosen parameters. Please try another set-up."
        print(msg)
        return recommendations, total_stars, total_reviews, products, msg