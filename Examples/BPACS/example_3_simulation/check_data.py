import modelicares
from read_budo_dymola import get_complete_variable_name
import sqlite3
from sqlalchemy import create_engine
import pandas as pd
from modelicares import SimRes
import numpy as np



def iae(measured_values, predicted_values):
    """calculated IAE criterion
    
    Arguments:
        measured_values {list} -- measured timeseries data
        predicted_values {list} -- predicted timeseries data
    
    Returns:
        float -- calculated IAE criterion
    """
    diff=0
    for a, b in zip(measured_values, predicted_values):
        diff+=abs(a-b)
    iae=diff.sum()# calculate IAE
    return iae


def rmse(measured_values, predicted_values):
    """calculates the root mean square error
    
    Arguments:
        measured_value {list} -- measured timeseries data
        predicted_value {list} -- predicted timeseries data
    
    Returns:
        float -- calculated root mean square error
    """
    measured_values=np.asarray(measured_values)
    predicted_values=np.asarray(predicted_values)
    rmse=np.sqrt(((measured_values - predicted_values) ** 2).mean())
    return rmse


def nrmse(measured_value, predicted_value):
    """calculates the min-max normalized root mean square error
    
    Arguments:
        measured_value {list} -- measured timeseries data
        predicted_value {list} -- predicted timeseries data
    
    Returns:
        float -- calculated normalized root mean square error
    """

    measured_value=np.asarray(measured_value)
    predicted_value=np.asarray(predicted_value)
    rmse_=rmse(measured_value, predicted_value)
    nrmse=rmse_/(measured_value.max()-measured_value.min())
    return nrmse
    

def reindex_int(df):
    df.index=pd.to_numeric(df.index)
    df=df[~df.index.duplicated(keep='last')]
    #    dfDymola.drop_duplicates(keep='last', inplace=True)
    max_range = max(df.index) + 1
    df = df.reindex(index=range(1, int(max_range)), method='ffill', fill_value=0)
    return df

def calculate_values(measured_values, predicted_values):
    iae_=iae(measured_values, predicted_values)
    rmse_=rmse(measured_values, predicted_values)
    nrmse_=nrmse(measured_values, predicted_values)
    return (iae_, rmse_, nrmse_)


def test_rmse():
    """test of rmse function"""
    test_ts_1=[1,2,3,4]
    test_ts_2=[1,2,3,4]
    test_ts_3=[5,10,20,40]
    assert rmse(test_ts_1,test_ts_2)==0
    assert rmse(test_ts_1,test_ts_3)==np.sqrt(416.25)



def preprocess_sim_data(dfDymola):
    #getting list of column names: names contain the unit
    df_col = list(dfDymola.columns)
    
    ##extract unit from column name
    df_col_split = []
    for x in df_col:
         df_col_split = df_col_split + [x.split()[0]]
         "check if Kelvin and convert it to °C"
         if x.split()[2]=="K":
             dfDymola[x]=dfDymola[x]-273.15
    
    #rename columns without units
    for i in range(len(df_col)):
        dfDymola=dfDymola.rename(index=str, columns={df_col[i]: df_col_split[i]})
    return dfDymola


def preprocess_monitoring_data(df):
    df.index=df["index"]
    df = reindex_int(df)
    return df

def check_length(df1, df2):
    if max(df1.index)==max(df2.index):
        pass
    elif max(df1.index)>max(df2.index):
        max_range = max(df1.index) + 1
        df2 = df2.reindex(index=range(1, int(max_range)), method='ffill', fill_value=0)
    else:
        max_range = max(df2.index) + 1
        df1 = df1.reindex(index=range(1, int(max_range)), method='ffill', fill_value=0)
    return (df1, df2)


def check_data(filename_model, filename_results, filename_database, budo_label):
    sim = SimRes(filename_results)
    variable_name_sim = get_complete_variable_name(filename_model, budo_label)
    dfDymola=sim.to_pandas([variable_name_sim]) 
    dfDymola=preprocess_sim_data(dfDymola)
    dfDymola=reindex_int(dfDymola)
    
    "read out of monitoring database"
    "(in real a specialized timeseries database)"
    disk_engine = create_engine('sqlite:///'+filename_database)
    df = pd.read_sql_query('SELECT * FROM timeseries', disk_engine)
    df = preprocess_monitoring_data(df)
    
    (df, dfDymola)=check_length(df, dfDymola)

    predicted_values = dfDymola[variable_name_sim]
    measured_values = df[budo_label]
    (iae_, rmse_, nrmse_)=calculate_values(measured_values, predicted_values)
    print("IAE between real and simulated data is: "+str(iae_))
    print("RMSE between real and simulated data is "+str(rmse_))
    print("NRMSE between real and simulated data is "+str(nrmse_))
    
    
    
    
    


if __name__=="__main__":
    check_data("Test_BUDO.mo",
    "demo_results.mat",
    "sqllite_test.db",
    "4120//BOI-H02.1_SEN.T-B06_WS.H.RET.PRIM_MEA.T_AI")
