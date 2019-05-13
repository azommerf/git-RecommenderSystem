import pickle
from program.app_modules import data_KNN, data_frame, data_reset, data_recommender
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix, save_npz, load_npz # Sparse matrix
from sklearn.neighbors import NearestNeighbors
import os



recommendations = np.array([])

for i in range(10):
    recommendations = np.append(recommendations, i)

print(recommendations)