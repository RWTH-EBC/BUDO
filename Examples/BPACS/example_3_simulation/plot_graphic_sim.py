import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import modelicares
import numpy as np
import sys
from dymola.dymola_interface import DymolaInterface
from modelicares import SimRes
import pandas as pd
from check_data import iae, rmse, nrmse, calculate_values, reindex_int

def graphic_sim():
    
    sns.set_palette("muted")
    sims, __ = modelicares.load('demo_results.mat')
    time = sims['combiTimeTable.y[1]'].values()
    T_out = sims['combiTimeTable.y[3]'].values()
    T_out_sim = sims['boiler_system.temperature_sensor_2.T'].values()
    sns.set_style("darkgrid")
#    sns.set(style="whitegrid", color_codes=True)
    np.transpose(T_out)
    np.transpose(time)
    T_out[0]=T_out[0]-273.15
    T_out_sim[0]=T_out_sim[0]-273.15
    plt.plot(time[0], T_out[0], label="B-4120//BOI.COND-H02_SEN.T-RL_WS.H.RET.OUT_MEA.T_AI")
    plt.plot(time[0], T_out_sim[0], label="B-4120//BOI.COND-H02_SEN.T-RL_WS.H.RET.OUT_MEA.T_SIM")
    
    axes=plt.gca()
    axes.set_ylim([50, 100])
    for tick in axes.xaxis.get_major_ticks():
                tick.label.set_fontsize(30) 
    for tick in axes.yaxis.get_major_ticks():
                tick.label.set_fontsize(30)     
    for tick in axes.get_xticklabels():
            tick.set_rotation(30)
    axes.legend(prop={'size': 30})
    plt.xlabel("time (in s)", fontsize = 32)
    plt.ylabel("temperature (in °C)", fontsize = 32)
    
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 35}
    
    mpl.rc('font', **font)
    fig=plt.gcf()
    fig.set_size_inches(18.5, 10.5, forward=True)
    
    
    plt.show()
    fig.savefig('simulation_results.png', dpi=fig.dpi, bbox_inches='tight')

def simulate():
    dir_aixlib = r"D:\Sciebo\Programmierung\GIT\_Standard\AixLib\AixLib"
    dir_result = r"D:\Sciebo\Programmierung\Tests\Dymola"
    dymola = DymolaInterface()
    try:
        dymola.openModel(path=os.path.join(dir_aixlib, 'package.mo'))
        # dymola.openModel(r"D:\Sciebo\Programmierung\Tests\Dymola\Test_BUDO.mo")
        dymola.translateModel(
            'AixLib.Fluid.BoilerCHP.Examples.Test_BUDO.CompleteModel')

        output = dymola.simulateExtendedModel(
            problem='AixLib.Fluid.BoilerCHP.Examples.Test_BUDO.CompleteModel',
            startTime=0.0,
            stopTime=86400,
            outputInterval=500,
            method="Dassl",
            tolerance=0.0001,
            resultFile=os.path.join(dir_result, 'demo_results'),
            finalNames=['boiler_system.temperature_sensor_2.T'],
        )
        print(output[1])

        error = dymola.getLastError()
        print(error)
        # dymola.plot(
        #     ["boiler_system.temperature_sensor_2.T", "combiTimeTable.y[3]"])
        # dymola.ExportPlotAsImage(os.path.join(dir_result, "plot.png"))

        # list_var = dymola.list(
        #     r"D:\Sciebo\Programmierung\Tests\Dymola\Test_BUDO.txt", variables='*"H02.1"*')
        # print(list_var)
        # list_var = dymola.variables(
        #     r"D:\Sciebo\Programmierung\Tests\Dymola\Test_BUDO.txt")
        # print(list_var)
        # list_var = dymola.getExperiment()
        # print(list_var)
        # list_var = dymola.listfunctions(filter="*")
        # print(list_var)

        dymola.exit()
    except:
        print("Unexpected error:", sys.exc_info())
        dymola.exit()

def list_variables(filename, search_string):
    dymola = DymolaInterface()
    list_var = dymola.list(variables={search_string})
    return list_var
    




def check_heatflow():
    """simulates the model of the example and calculates different criterias (deviation, IAE, RMSE, NRMSE)
    """

    simulate()
    sims, __ = modelicares.load('demo_results.mat')
    budo_labels=["time",
                "",
                ]
    
    T_in = sims['combiTimeTable.y[2]'].values()
    T_out = sims['combiTimeTable.y[3]'].values()
    T_out_sim = sims['boiler_system.temperature_sensor_2.T'].values()
    V_flow = sims['combiTimeTable.y[4]'].values()

    heat_sim=[0]
    heat_real=[0]
    for a, b, c, d in zip(T_in, T_out_sim, T_out, V_flow):
        heat_sim+=(b-a)*d
        heat_real+=(c-a)*d
    sum_sim=heat_sim.sum()
    sum_real=heat_real.sum()
    print(sum_sim)
    print(sum_real)
    print((sum_real-sum_sim)/sum_real)

    IAE_=iae(T_out, T_out_sim)
    print(IAE_)
    rmse_=rmse(T_out, T_out_sim)
    print(rmse_)
    nrmse_=nrmse(T_out, T_out_sim)
    print(nrmse_)
    print("ready")

def get_sim_data():
    sim = SimRes('demo_results.mat')
    dfDymola=sim.to_pandas(['combiTimeTable.y[2]', 'combiTimeTable.y[3]', 'boiler_system.temperature_sensor_2.T', 'combiTimeTable.y[4]']) 
    
    #getting list of column names: names contain the unit
    df_col = list(dfDymola.columns)
    
    ##extract unit from column name
    df_col_split = []
    for x in df_col:
         df_col_split = df_col_split + [x.split()[0]]
    
    #rename columns without units
    for i in range(len(df_col)):
        dfDymola=dfDymola.rename(index=str, columns={df_col[i]: df_col_split[i]})
    # print(dfDymola)
    dfDymola.index=pd.to_numeric(dfDymola.index)
    dfDymola["time_diff"]=dfDymola.index
    # dfDymola["time_diff"]=pd.to_numeric(dfDymola["time_diff"])
    dfDymola["time_diff"] = (dfDymola["time_diff"].shift(-1) - dfDymola["time_diff"])
#    dfDymola=dfDymola[~dfDymola.index.duplicated(keep='last')]
##    dfDymola.drop_duplicates(keep='last', inplace=True)
#    max_range = max(dfDymola.index) + 1
#    
#    
#    dfDymola = dfDymola.reindex(index=range(1, int(max_range)), method='ffill', fill_value=0)
    dfDymola=reindex_int(dfDymola)
    return dfDymola








if __name__ == "__main__":
    # graphic_sim()
    # check_heatflow()
    dfDymola=get_sim_data()
    measured_values = dfDymola['combiTimeTable.y[3]']
    predicted_values = dfDymola['boiler_system.temperature_sensor_2.T']   
    (iae_, rmse_, nrmse_)=calculate_values(measured_values, predicted_values)

    print(iae_)
    print(rmse_)
    print(nrmse_)
    
    T_in = dfDymola['combiTimeTable.y[2]']
    T_out = dfDymola['combiTimeTable.y[3]']
    T_out_sim = dfDymola['boiler_system.temperature_sensor_2.T']
    V_flow = dfDymola['combiTimeTable.y[4]']

    heat_sim=[0]
    heat_real=[0]
    for a, b, c, d in zip(T_in, T_out_sim, T_out, V_flow):
        heat_sim+=(b-a)*d
        heat_real+=(c-a)*d
    sum_sim=heat_sim.sum()
    sum_real=heat_real.sum()
    print(sum_sim)
    print(sum_real)
    print((sum_real-sum_sim)/sum_real)

    
    
    
    
    