from __future__ import annotations
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pathlib
import pandas as pd
# from osgeo import gdal
# from osgeo.gdalconst import * 
import gdal
from pandas import read_csv
from app import *
import sklearn

# from sklearn.utils.testing import ignore_warnings
from sklearn.utils._testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning

target=""

def ENVI_raster_binary_to_2d_array(file_name,x_min,y_min,x_max,y_max):
    '''
    Converts a binary file of ENVI type to a numpy array.
    Lack of an ENVI .hdr file will cause this to crash.
    '''
    print(file_name)
    inDs = gdal.Open(file_name, GA_ReadOnly)
    band_avg=[]
    if inDs is None:
        print("Couldn't open this file: " + file_name)
        print('\nPerhaps you need an .hdr file?')   
        print("Error here")             
        sys.exit("Try again!")
    else:
        print("%s opened successfully"%file_name)
            
        
        for k in range(168):
            band=inDs.GetRasterBand(k+1)
            arr=band.ReadAsArray()
            bound_region=arr[x_min:x_max,y_min:y_max]
            i,j=bound_region.shape
            count=0
            for row in range(i):
                for col in range(j):
                    count+=bound_region[row][col]
            band_avg.append(count/(i*j))
    return band_avg


def ENVI_raster_binary_to_image(file_name):
    '''
    Converts a binary file of ENVI type to a numpy array.
    Lack of an ENVI .hdr file will cause this to crash.
    '''
    
    print(" envi function file_name received = ",file_name)
    
    # file_name=file_name.replace("\\","/")
    inDs = gdal.Open(file_name, GA_ReadOnly)
    
    if inDs is None:
        print("Couldn't open this file: " + file_name)
        print('\nPerhaps you need an .hdr file?')   
        print("Error here")             
        sys.exit("Try again!")
    else:
        print("%s opened successfully"%file_name)
            
        
        band1=inDs.GetRasterBand(16)
        band2=inDs.GetRasterBand(17)
        band3=inDs.GetRasterBand(18)
        
        arr1=band1.ReadAsArray()
        arr2=band2.ReadAsArray()
        arr3=band3.ReadAsArray()

        h,w = arr1.shape
        data = np.zeros((h, w, 3), dtype=np.uint8)

        for a in range(0,h):
            for b in range(0,w):

                # normalize 
                v1=arr1[a,b]
                v2=arr2[a,b]
                v3=arr3[a,b]

                # print(f"RGB: ({v1},{v2},{v3})")

                max=8000
                if v1>8000:
                    v1=8000
                if v2>8000:
                    v2=8000
                if v3>8000:
                    v3=8000
                v1=int((v1/max)*255)
                v2=int((v2/max)*255)
                v3=int((v3/max)*255)


                data[a, b] = [v1, v2, v3] 
             
        # name extraction        
        img = Image.fromarray(data, 'RGB')
        return img
    
@ignore_warnings(category=ConvergenceWarning)
@ignore_warnings(category=UserWarning)
def Regression(values168):
    # df = read_csv(r"C:\Users\admin\Desktop\flasknew-Copy\region.csv", delim_whitespace=False, header=None)
    df = read_csv(os.getcwd()+"/region.csv", delim_whitespace=False, header=None)
    feature_names = ['Band_1', 'Band_2', 'Band_3', 'Band_4', 'Band_5', 'Band_6', 'Band_7', 'Band_8  ', 'Band_9', 'Band_10', 'Band_11', 'Band_12', 'Band_13', 'Band_14', 'Band_15', 'Band_16', 'Band_17', 'Band_18', 'Band_19', 'Band_20', 'Band_21', 'Band_22', 'Band_23', 'Band_24', 'Band_25', 'Band_26', 'Band_27', 'Band_28', 'Band_29', 'Band_30', 'Band_31', 'Band_32', 'Band_33', 'Band_34', 'Band_35', 'Band_36', 'Band_37', 'Band_38', 'Band_39', 'Band_40', 'Band_41', 'Band_42', 'Band_43', 'Band_44', 'Band_45', 'Band_46', 'Band_47', 'Band_48', 'Band_49', 'Band_50', 'Band_51', 'Band_52', 'Band_53', 'Band_54', 'Band_55', 'Band_56', 'Band_57', 'Band_58', 'Band_59', 'Band_60', 'Band_61', 'Band_62', 'Band_63', 'Band_64', 'Band_65', 'Band_66', 'Band_67', 'Band_68', 'Band_69', 'Band_70', 'Band_71', 'Band_72', 'Band_73', 'Band_74', 'Band_75', 'Band_76', 'Band_77', 'Band_78', 'Band_79', 'Band_80', 'Band_81', 'Band_82', 'Band_83', 'Band_84', 'Band_85', 'Band_86', 'Band_87', 'Band_88', 'Band_89', 'Band_90', 'Band_91', 'Band_92', 'Band_93', 'Band_94', 'Band_95', 'Band_96', 'Band_97', 'Band_98', 'Band_99', 'Band_100', 'Band_101', 'Band_102', 'Band_103', 'Band_104', 'Band_105', 'Band_106', 'Band_107', 'Band_108', 'Band_109', 'Band_110', 'Band_111', 'Band_112', 'Band_113', 'Band_114', 'Band_115', 'Band_116', 'Band_117', 'Band_118', 'Band_119', 'Band_120', 'Band_121', 'Band_122', 'Band_123', 'Band_124', 'Band_125', 'Band_126', 'Band_127', 'Band_128', 'Band_129', 'Band_130', 'Band_131', 'Band_132', 'Band_133', 'Band_134', 'Band_135', 'Band_136', 'Band_137', 'Band_138', 'Band_139', 'Band_140', 'Band_141', 'Band_142', 'Band_143', 'Band_144', 'Band_145', 'Band_146', 'Band_147', 'Band_148', 'Band_149', 'Band_150', 'Band_151', 'Band_152', 'Band_153', 'Band_154', 'Band_155', 'Band_156', 'Band_157', 'Band_158', 'Band_159', 'Band_160', 'Band_161', 'Band_162', 'Band_163', 'Band_164', 'Band_165', 'Band_166', 'Band_167', 'Band_168','Sugar']

    
    from sklearn.model_selection import train_test_split
    df.columns = feature_names

    #Split into features and target (Price)
    X = df.drop('Sugar', axis = 1)
    y = df['Sugar']
    d=pd.DataFrame(X)
    # display(d)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 20)

    #______________Lasso_____________
    from sklearn.linear_model import Lasso
    from sklearn.model_selection import GridSearchCV
    lasso=Lasso()
    parameter={'alpha':[1e-15,1e-10,1e-8,1e-3,1e-2,1,5,10,20,30,35,40,45,50,55,100]}
    lasso_regressor=GridSearchCV(lasso,parameter,scoring="neg_mean_squared_error",cv=5)
    lasso_regressor.fit(X,y)
    
    # RIDGE
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import GridSearchCV
    ridge=Ridge()
    parameter={'alpha':[1e-15,1e-10,1e-8,1e-3,1e-2,1,5,10,20,30,35,40,45,50,55,100]}
    ridge_regressor=GridSearchCV(ridge,parameter,scoring="neg_mean_squared_error",cv=5)
    ridge_regressor.fit(X,y)
    
    prediction_lasso=lasso_regressor.predict(values168)
    prediction_ridge=ridge_regressor.predict(values168)
    
    return prediction_lasso,prediction_ridge
    
def classification(sugar):
    from sklearn.model_selection import train_test_split
 
    # store the feature matrix (X) and response vector (y)
    # df = read_csv(r"C:\Users\admin\Desktop\flasknew-Copy\final.csv", delim_whitespace=False, header=None)
    df = read_csv(os.getcwd()+"/final.csv", delim_whitespace=False, header=None)

    feature_names = ['Sugar','Classification']

    df.columns = feature_names
    # print(df.head())

    #Split into features and target (Price)
    X = df.drop('Classification', axis = 1)
    y = df['Classification']

    # splitting X and y into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 20)
    
    # training the model on training set
    from sklearn.naive_bayes import GaussianNB
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
 
    final_prediction = gnb.predict(sugar) 
    
    return final_prediction

def hsi_to_image(hsipath):
    # get the jpg image file name in use
    # file=open(r"C:\Users\admin\Desktop\flasknew-Copy\target_file_name_store.txt",'r')
    file=open(os.getcwd()+"/target_file_name_store.txt",'r')
    target=file.read()
    file.close()
    img_name=target+'.jpg'
    
    # print("++++++++++______ hsi to image = ",img_name)
    
    # convert hsi to jpg
    converted_image=ENVI_raster_binary_to_image(hsipath)
    # converted_image.save(r"C:\Users\admin\Desktop\flasknew-Copy\static\uploads"+f"\\{img_name}",'JPEG')
    converted_image.save(os.getcwd()+"/static/uploads"+f"/{img_name}",'JPEG')
        
    return

# def find_result_file_path():
#     dir=r"C:\Users\Dell\Desktop\flasknew\yolov5\runs\detect"
    
#     target=get_current_file()
#     val=target.split('.')
#     annotation_file=str(val[0]+'.txt')
    
#     for root, dirs, files in os.walk(dir):
#         for name in files:
#             if name==annotation_file:
#                 file_wholepath=str(os.path.join(root, name))
#                 return str(os.path.join(root, name))

def complete():
    print("____COMPLETE CALLED")
    # change 1, argument in below function required
    
    # f=open(r"C:\Users\admin\Desktop\flasknew-Copy\target_file_name_store.txt",'r')
    f=open(os.getcwd()+"/target_file_name_store.txt",'r')
    target=f.read()
    f.close()
    
    # pth=r"C:\Users\admin\Desktop\flasknew-Copy\yolov5\runs\detect\exp\labels"+f"\\{target}.txt"
    pth=os.getcwd()+"/yolov5/runs/detect/exp/labels"+f"/{target}.txt"
    f=open(pth)
    prediction=[]
    
    for i in f.readlines():
        
        x=i.split(" ")
        x_center=(float(x[1])*100)*1.5
        y_center=float(x[2])*100*1.5
    
        x_min=round(x_center-(float(x[3])*100*1.5))
        y_min=round(y_center-(float(x[4])*100*1.5))

        x_max=round(x_center+(float(x[3])*100*1.5))
        y_max=round(y_center+(float(x[4])*100*1.5))

        #---------------GDAL---------------------
        
        # hsipath=r"C:\Users\admin\Desktop\flasknew-Copy\static\uploads"+f"\\{target}.bip"
        hsipath=os.getcwd()+"/static/uploads"+f"/{target}.bip"
        band_avg=ENVI_raster_binary_to_2d_array(hsipath,x_min,y_min,x_max,y_max)
        
        #---------------Lasso--------------------
        df_lasso=pd.DataFrame(band_avg)
        df_lasso=df_lasso.transpose()
        df_lasso.columns= ['Band_1', 'Band_2', 'Band_3', 'Band_4', 'Band_5', 'Band_6', 'Band_7', 'Band_8  ', 'Band_9', 'Band_10', 'Band_11', 'Band_12', 'Band_13', 'Band_14', 'Band_15', 'Band_16', 'Band_17', 'Band_18', 'Band_19', 'Band_20', 'Band_21', 'Band_22', 'Band_23', 'Band_24', 'Band_25', 'Band_26', 'Band_27', 'Band_28', 'Band_29', 'Band_30', 'Band_31', 'Band_32', 'Band_33', 'Band_34', 'Band_35', 'Band_36', 'Band_37', 'Band_38', 'Band_39', 'Band_40', 'Band_41', 'Band_42', 'Band_43', 'Band_44', 'Band_45', 'Band_46', 'Band_47', 'Band_48', 'Band_49', 'Band_50', 'Band_51', 'Band_52', 'Band_53', 'Band_54', 'Band_55', 'Band_56', 'Band_57', 'Band_58', 'Band_59', 'Band_60', 'Band_61', 'Band_62', 'Band_63', 'Band_64', 'Band_65', 'Band_66', 'Band_67', 'Band_68', 'Band_69', 'Band_70', 'Band_71', 'Band_72', 'Band_73', 'Band_74', 'Band_75', 'Band_76', 'Band_77', 'Band_78', 'Band_79', 'Band_80', 'Band_81', 'Band_82', 'Band_83', 'Band_84', 'Band_85', 'Band_86', 'Band_87', 'Band_88', 'Band_89', 'Band_90', 'Band_91', 'Band_92', 'Band_93', 'Band_94', 'Band_95', 'Band_96', 'Band_97', 'Band_98', 'Band_99', 'Band_100', 'Band_101', 'Band_102', 'Band_103', 'Band_104', 'Band_105', 'Band_106', 'Band_107', 'Band_108', 'Band_109', 'Band_110', 'Band_111', 'Band_112', 'Band_113', 'Band_114', 'Band_115', 'Band_116', 'Band_117', 'Band_118', 'Band_119', 'Band_120', 'Band_121', 'Band_122', 'Band_123', 'Band_124', 'Band_125', 'Band_126', 'Band_127', 'Band_128', 'Band_129', 'Band_130', 'Band_131', 'Band_132', 'Band_133', 'Band_134', 'Band_135', 'Band_136', 'Band_137', 'Band_138', 'Band_139', 'Band_140', 'Band_141', 'Band_142', 'Band_143', 'Band_144', 'Band_145', 'Band_146', 'Band_147', 'Band_148', 'Band_149', 'Band_150', 'Band_151', 'Band_152', 'Band_153', 'Band_154', 'Band_155', 'Band_156', 'Band_157', 'Band_158', 'Band_159', 'Band_160', 'Band_161', 'Band_162', 'Band_163', 'Band_164', 'Band_165', 'Band_166', 'Band_167', 'Band_168']
        
        lasso,ridge=Regression(df_lasso)
        
        
        
        print("\n\nSUGAR [LASSO] = ",lasso)
        print("\n\nRIDGE [RIDGE] = ",ridge,"\n\n")
        
        # prediction_lasso1=lasso_regressor.predict(df_lasso)
        # print(prediction_lasso1)
        
        #----------------Naive baised--------------
        df_sugar=pd.DataFrame(lasso)
        df_sugar.columns=["Sugar"]
                
        classif_result=classification(df_sugar)
        
        prediction.append(classif_result[0])

    true_value=sum(prediction)
    total_value=len(prediction)
    per=round((true_value/total_value)*100)
    if(per>30):
        print("Classification RESULT: Significant Bruises Detected\n")
        return True
    else:
        print("Classification RESULT: Acceptable Quality")
        return False