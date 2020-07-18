#!/usr/bin/env python
# coding: utf-8

# In[95]:


######################################################################################################################
# Assignment 2
# Subject - CSE535 Mobile Computing
# Author - Abhik Dey (1216907406), Sethu Manickam (1218452066), Rohith Eppepalli (1215350630), Sree Vashini Ravichandran (1217841794)
# Goal is:
#    1) Test Model to predict gestures - buy (1), communicate (2), fun (3), hope (4), mother (5), really (6)
#    2) File will be called by deploy.py
#
######################################################################################################################

import numpy as np
import pandas as pd
import scipy.fftpack as fftpack
import os
from sklearn.preprocessing import StandardScaler
import scipy.signal as signal
from sklearn.model_selection import KFold
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import Perceptron
from scipy.stats import kurtosis
import pickle
import json


# In[96]:


def normalizeData(data_frame):

    extracols = data_frame[['nose_x','nose_y','rightEye_x', 'rightEye_y','leftEye_x', 'leftEye_y']]
    data_frame.drop(['nose_x', 'nose_y', 'leftEye_x', 'leftEye_y', 'rightEye_x', 'rightEye_y'], axis=1, inplace=True)
    
    normalizedData = []
    df_cols = []
    fm = None
    for cols in data_frame.columns:
        df_cols.append(cols)
        col = data_frame[cols] # extracting each column
        mean = np.mean(col)
#         normData = (col - mean)/(np.max(col-mean) - np.min(col-mean))

        if cols.startswith("right") and cols.endswith("x"):
            normData = (col - extracols['nose_x'] / abs(extracols['leftEye_x'] - extracols['rightEye_x']))
        if cols.startswith("left") and cols.endswith("x"):
            normData = (col - extracols['nose_x'] / abs(extracols['leftEye_x'] - extracols['rightEye_x']))
        if cols.startswith("right") and cols.endswith("y"):
            normData = (col - extracols['nose_y'] / abs(extracols['leftEye_y'] - extracols['rightEye_y']))
        else:
            normData = (col - extracols['nose_y'] / abs(extracols['leftEye_y'] - extracols['rightEye_y']))
             
        df_norm_data = pd.DataFrame(normData, columns = [cols])
        
        rollMean = df_norm_data.rolling(window=10,min_periods=1).mean()
        fm = pd.concat([fm, rollMean], axis = 1, sort = False)
    return fm;


# In[97]:


#code for feature mean
def calMean(data_frame):
    #cols = data_frame.columns
    
    df_cols = []
    mean_array = []


    feature_matrix = pd.DataFrame() #return feature matrix
    
    for cols in data_frame.columns:
        df_cols.append('Mean'+cols)
        meanval  = np.mean(data_frame[cols])
        mean_array.append(meanval);
        
    feature_matrix = pd.DataFrame([mean_array],columns = df_cols)
    
    return feature_matrix


# In[98]:


#code for feature variance
def calVariance(data_frame):
    #cols = data_frame.columns
    
    df_cols = []
    variance_array = []


    feature_matrix = pd.DataFrame() #return feature matrix
    
    for cols in data_frame.columns:
        df_cols.append('Variance'+cols)
        varval  = np.var(data_frame[cols])
        variance_array.append(varval);
        
    feature_matrix = pd.DataFrame([variance_array],columns = df_cols)
    
    return feature_matrix

#code for feature 1
# Sample given as FFT
def calFFT(data_frame):
    #cols = data_frame.columns
    df_cols = []
    fft_val = []


    feature_matrix = pd.DataFrame() #return feature matrix
    
    for cols in data_frame.columns:
        df_cols.append('FFT_Peak1_'+cols)
        fft_values  = abs(fftpack.fft(data_frame[cols].values))
        val = set(fft_values)
        val = sorted(val, reverse = True)
        firstHighPeak = list(val)[1]
        fft_val.append(firstHighPeak)
        
    #return fft_val, df_cols
    feature_matrix = pd.DataFrame([fft_val],columns = df_cols)
    #print (feature_matrix)
    
    return feature_matrix


# In[101]:


def calWelch(data_frame):
    df_cols = []
    welch_val = []


    feature_matrix = pd.DataFrame() 
    for cols in data_frame.columns:
        df_cols.append('maxAmplitude'+cols)
        v, welch_values  = np.array((signal.welch(data_frame[cols].values)))
        welch_val.append(np.sqrt(max(welch_values)))
    feature_matrix = pd.DataFrame([welch_val],columns = df_cols)
        
    return feature_matrix


# In[102]:


#code for feature 2

def calMin(data_frame):
    #cols = data_frame.columns
    
    df_cols = []
    min_array = []


    feature_matrix = pd.DataFrame() #return feature matrix
    
    for cols in data_frame.columns:
        df_cols.append('Min'+cols)
        minval  = min(data_frame[cols])
        min_array.append(minval);
        
    feature_matrix = pd.DataFrame([min_array],columns = df_cols)
    
    return feature_matrix


# In[103]:


#code for feature 3

def calMax(data_frame):
    #cols = data_frame.columns
    
    df_cols = []
    max_array = []


    feature_matrix = pd.DataFrame() #return feature matrix
    
    for cols in data_frame.columns:
        df_cols.append('Max'+cols)
        maxval  = max(data_frame[cols])
        max_array.append(maxval);
        
    feature_matrix = pd.DataFrame([max_array],columns = df_cols)
    
    return feature_matrix


# In[104]:


#code for feature 4

def calSlope(data_frame):
    #cols = data_frame.columns
    
    df_cols = []
    zc_array = []


    feature_matrix = pd.DataFrame() #return feature matrix
    
    for cols in data_frame.columns:
        df_cols.append('Slope1'+cols)
        df_cols.append('Slope2'+cols)

        threshold = np.mean(data_frame[cols])
        posSlope = 0
        posCount = 0
        negSlope = 0
        negCount = 0
        for i in range(len(data_frame[cols]) - 1):
            if (data_frame[cols][i] > data_frame[cols][i+1]):
                posSlope += data_frame[cols][i] - data_frame[cols][i+1]
                posCount += 1
            elif (data_frame[cols][i] < data_frame[cols][i+1]):
                negSlope += data_frame[cols][i+1] - data_frame[cols][i]
                negCount += 1
        zc_array.append(posSlope/posCount)
        zc_array.append(negSlope/negCount)
        
    feature_matrix = pd.DataFrame([zc_array],columns = df_cols)
    
    return feature_matrix


def convert_to_dataframe(path_to_video):
    columns = ['score_overall', 'nose_score', 'nose_x', 'nose_y', 'leftEye_score', 'leftEye_x', 'leftEye_y',
               'rightEye_score', 'rightEye_x', 'rightEye_y', 'leftEar_score', 'leftEar_x', 'leftEar_y',
               'rightEar_score', 'rightEar_x', 'rightEar_y', 'leftShoulder_score', 'leftShoulder_x', 'leftShoulder_y',
               'rightShoulder_score', 'rightShoulder_x', 'rightShoulder_y', 'leftElbow_score', 'leftElbow_x',
               'leftElbow_y', 'rightElbow_score', 'rightElbow_x', 'rightElbow_y', 'leftWrist_score', 'leftWrist_x',
               'leftWrist_y', 'rightWrist_score', 'rightWrist_x', 'rightWrist_y', 'leftHip_score', 'leftHip_x',
               'leftHip_y', 'rightHip_score', 'rightHip_x', 'rightHip_y', 'leftKnee_score', 'leftKnee_x', 'leftKnee_y',
               'rightKnee_score', 'rightKnee_x', 'rightKnee_y', 'leftAnkle_score', 'leftAnkle_x', 'leftAnkle_y',
               'rightAnkle_score', 'rightAnkle_x', 'rightAnkle_y']
    data = path_to_video
    csv_data = np.zeros((len(data), len(columns)))
    for i in range(csv_data.shape[0]):
        one = []
        one.append(data[i]['score'])
        for obj in data[i]['keypoints']:
            one.append(obj['score'])
            one.append(obj['position']['x'])
            one.append(obj['position']['y'])
        csv_data[i] = np.array(one)
    return pd.DataFrame(csv_data, columns=columns)


# In[129]:


def get_key(val):
    gesture_labels = { 'buy' : 1,
                       'communicate' : 2,
                       'fun' : 3,
                       'hope': 4,
                       'mother': 5,
                       'really' : 6
                     }
    
    for key, value in gesture_labels.items(): 
         if val == value: 
             return key 
  
    return "key doesn't exist"


# In[143]:


def main(json_data):
    
    gesture_columns = ['leftElbow_x','leftElbow_y','rightElbow_x','rightElbow_y','leftWrist_y', 
                       'rightWrist_y','leftWrist_x', 'rightWrist_x', 'rightEye_x', 'rightEye_y', 
                       'leftEye_x', 'leftEye_y', 'nose_x', 'nose_y']
    
    fm = None
    
#     with open('Datasets/key_points.json') as f:
#         json_data = json.load(f)
    
    temp_key_points = convert_to_dataframe(json_data)[gesture_columns];
    unique_key_points = normalizeData(temp_key_points)
    

    # Feature Extractions - 

    #Feature 1 -- For feature extraction of FFT
    resFFT = calFFT(unique_key_points)
    fm = pd.concat([fm,resFFT], axis = 1, sort = False)

    resWelch = calWelch(unique_key_points)
    fm = pd.concat([fm,resWelch], axis = 1, sort = False)

    resMean = calMean(unique_key_points)    
    fm = pd.concat([fm,resMean], axis = 1, sort = False)

    #Feature 4 -- For feature extraction of Min
    resMin = calMin(unique_key_points)
    fm = pd.concat([fm,resMin], axis = 1, sort = False)

    #Feature 5 -- For feature extraction of Max
    resMax = calMax(unique_key_points)
    fm = pd.concat([fm,resMax], axis = 1, sort = False)

    #Feature 6 -- For feature extraction of Variance
    resVariance = calVariance(unique_key_points)
    fm = pd.concat([fm,resVariance], axis = 1, sort = False)

    #Feature 7 -- For feature extraction of Polyfit
    resSlope = calSlope(unique_key_points)
    fm = pd.concat([fm,resSlope], axis = 1, sort = False)
    
    predictions = {}
    # Exceuting pickle files
    for idx, i in enumerate(os.listdir('models/')):
        with open('models/'+i, 'rb') as file:
            loaded_file = pickle.load(file)
            predict = loaded_file.predict(fm)
    
        file.close()
        print('Prediction by model '+i+' - ',get_key(predict[0]))
        predictions[idx+1] = get_key(predict[0])

    json_ret = json.loads(json.dumps(predictions))
    return json_ret




