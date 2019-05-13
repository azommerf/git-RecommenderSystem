import os
import pickle
from program.app_modules import data_KNN, data_frame
import pandas as pd

pickle_in = open("msg.pickle","rb")
msg = pickle.load(pickle_in)
print(msg)


df = pd.to_hdf("./df.hdf",'mydata')
# df = pd.read_pickle("./df_pickled.pickle.gzde", compression='gzip')
print(df.head())

os.remove("./*.pickel")
os.remove("./*.hdf")