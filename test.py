import pickle
from program.app_modules import data_KNN, data_frame, data_reset
import pandas as pd

import os

# data_dir = "./program/data/"
# data_dir_ = os.listdir(data_dir)
# for file in data_dir_:
#     if file.endswith(".pickle"):
#         os.remove(os.path.join(data_dir,file))



# def data_reset(filetype):
#     data_dir = "./program/data/"
#     data_dir_ = os.listdir(data_dir)
#     if filetype == "all":
#         for file in data_dir_:
#             if file.endswith(".pickle"):
#                 os.remove(os.path.join(data_dir,file))
#             elif file.endswith(".csv"):
#                 os.remove(os.path.join(data_dir,file))
#             elif file.endswith(".tsv"):
#                 os.remove(os.path.join(data_dir,file))
#     elif filetype == "pickle":
#         for file in data_dir_:
#             if file.endswith(".pickle"):
#                 os.remove(os.path.join(data_dir,file))
#     elif filetype == "csv":
#         for file in data_dir_:
#             if file.endswith(".csv"):
#                 os.remove(os.path.join(data_dir,file))
#     elif filetype == "tsv":
#         for file in data_dir_:
#             if file.endswith(".tsv"):
#                 os.remove(os.path.join(data_dir,file))
#     else: print("\nAll necessery files deleted.")

data_reset("all")