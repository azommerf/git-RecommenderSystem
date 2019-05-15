import program.app_modules as rs
import os
import pandas as pd
import numpy as np


url = "https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Books_v1_00.tsv.gz"
# url = "https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Musical_Instruments_v1_00.tsv.gz"

filename = url.split('/')[-1]
workingdir = os.path.abspath('')
datadir = "program/data" # Directory where data is stored
filepath_tsvgz = os.path.join(workingdir, datadir, filename)
filepath_tsv = filepath_tsvgz[0:-3]

print("creating dataframe")

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
df.astype({'star_rating':np.int8})

print("created successfully")
print(df.head())

# Calculate total number of products and customers (for range calculation)
print("success 1")
prodNo = len(set(df["product_id"])) # Number of products
custNo = len(set(df["customer_id"])) # Number of customers
print("Number of unique products: {}".format(prodNo))
print("Number of unique customers: {}".format(custNo))

# Get unique product and customer IDs and index them
print("success 2")
prodUnique_indexed = dict(zip(np.unique(df["product_id"]), list(range(prodNo))))
custUnique_indexed = dict(zip(np.unique(df["customer_id"]), list(range(custNo))))
prodUnique_reverseIndexed = dict(zip(list(range(prodNo)), np.unique(df["product_id"])))
custUnique_reverseIndexed = dict(zip(list(range(custNo)), np.unique(df["customer_id"])))

# Finally go through each row of dataframe and assign index 
print("success 3")
custIndex = [custUnique_indexed[i] for i in df["customer_id"]]
prodIndex = [prodUnique_indexed[i] for i in df["product_id"]]

# Create indexed matrix
print("success 4")
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

print("...storing number of customers...")
with open("./program/data/custNo.pickle", "wb") as pkl:
    pickle.dump(custNo, pkl, protocol=pickle.HIGHEST_PROTOCOL)
print("...storing indices...")
with open("./program/data/prodUnique_indexed.pickle", "wb") as pkl:
    pickle.dump(prodUnique_indexed, pkl, protocol=pickle.HIGHEST_PROTOCOL)
with open("./program/data/prodUnique_reverseIndexed.pickle", "wb") as pkl:
    pickle.dump(prodUnique_reverseIndexed, pkl, protocol=pickle.HIGHEST_PROTOCOL)
print("...storing sparse matrix...")
save_npz("./program/data/df_csr.npz", df_csr)

msg = "\nFitted the KNN model successfully."