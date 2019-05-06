import sys # For input/output to terminal
import os # For saving filepath

import requests # For requesting and downloading data set from URL
import gzip # For unzipping the data set
import pandas as pd # For handling dataframe



def main():
    
    #################################################################################
    #  Prepare the data set from Amazon
    # Choose category here: https://s3.amazonaws.com/amazon-reviews-pds/tsv/index.txt
        
    download_request = input("\nDo you want to download the Amazon data set (can take a while)? [y]/[n] ")

    # INSERT URL HERE
    # url = "https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Musical_Instruments_v1_00.tsv.gz"
    url = "http://ctdbase.org/reports/CTD_genes_pathways.tsv.gz" # This is just an example data base which is smaller to handle

    filename = url.split('/')[-1]
    workingdir = os.path.dirname(os.path.realpath(__file__))
    datadir = "data"
    filepath = os.path.join(workingdir, datadir, filename)
    
    
    if download_request == "y":
        
        def download_gz(url, filepath, filename):
            print("\n{:^50}".format("...downloading the data..."))

            # Retrieve data from URL
            r = requests.get(url, stream=True)
            total_length = r.headers.get('content-length')
            
            with open(filepath, 'wb') as f:
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
            zipped = gzip.GzipFile(filepath, 'rb')
            zipped_content = zipped.read()
            zipped.close()
            unzipped = open(filepath[0:-3], 'wb')
            unzipped.write(zipped_content)
            unzipped.close()
            print("\n File decompressed successfully.")

            # Delete zipped file
            os.remove(filepath)
            filepath = filepath[0:-3]
            print("\nCompressed file deleted successfully.")

            return filepath

        # Execute download
        filepath = download_gz(url, filepath, filename)

    else:
        print("\nData not downloaded.")
        filepath = filepath[0:-3]
    

    ###########################################
    # Create dataframe

    print(filepath)
    # df = pd.read_csv(filepath, sep='\t')
    df = pd.read_table(filepath, delim_whitespace=True, error_bad_lines=False, header=0)

    df


















    print("\nProgram exited successfully")



