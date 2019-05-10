import sys # For input/output to terminal
import os # For saving filepath
import requests # For requesting and downloading data set from URL
import gzip # For unzipping the data set
import shutil # For unzipping
import pandas as pd # For handling dataframe
import numpy as np # For sparse grid


def download_main(url):

    #################################################################################
    #  Prepare the data set from Amazon
    # Choose category here: https://s3.amazonaws.com/amazon-reviews-pds/tsv/index.txt


    # INSERT URL HERE

    filename = url.split('/')[-1]
    workingdir = os.path.abspath('')
    datadir = "data" # Directory where data is stored
    filepath_tsvgz = os.path.join(workingdir, datadir, filename)
    filepath_tsv = filepath_tsvgz[0:-3]


    while True:
        
        # If download function should be callable with question, uncomment the following and comment out the lext line after the following.
        #download_request = input("\nDo you want to prepare the following Amazon data set (can take a while if not downloaded): {}? [y]/[n] ".format(filename))
        download_request = "y"
        
        print(filepath_tsvgz)


        if download_request == "y":

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

                # Unzip file  
                print("\n\nunzipping the file...")
                # zipped = gzip.GzipFile(filepath_tsvgz, 'rb')
                # zipped_content = zipped.read()
                # zipped.close()
                # unzipped = open(filepath_tsv, 'wb')
                # unzipped.write(zipped_content)
                # unzipped.close()

                with gzip.open(filepath_tsvgz, 'r') as f_in, open(filepath_tsv, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

                print("\nFile decompressed successfully.")

                # Delete zipped file
                os.remove(filepath_tsvgz) # delete compressed data
                print("Compressed file deleted successfully.")
                print("File saved in the following location:\n{}".format(filepath_tsv))

            exists_tsv = os.path.isfile(filepath_tsv)
            # Execute download
            if not exists_tsv:
                download_gz(url, filepath_tsvgz, filename)
                break
            else: 
                print("\nFile already exists. Continue with creating data frame. ")
                break

        else:
            print("\nChecking if data is downloaded.")

            # Check if decompressed data file already exists
            exists = os.path.isfile(filepath_tsv)
            if exists:
                print("\nFile already exists. Continue with creating data frame.")
                break
            else:
                print("\nData file not found. Download the file to continue program.")

    if os.path.isfile(filepath_tsv):
        msg = "Data downloaded successfully (check data directory)"
        return msg
    else:
        msg = "Something went wrong. Please try again or send a message to on of our hosts: andre.zommerfelds@unil.ch"
        return msg
                