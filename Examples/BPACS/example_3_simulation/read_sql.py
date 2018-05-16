import os
import sys
"""add relative path to path"""

cwd=os.path.realpath(os.path.join(os.path.dirname(__file__), ".."))

for directory in os.listdir(cwd):
    folder=cwd+"\\"+directory
    if os.path.isdir(folder):
        print ("append to path: "+folder)
        sys.path.append(folder)

from collections import OrderedDict
from ebc_sql import EbcSql

import datetime as dt


import scipy
from scipy import io

def main():
    """EXAMPLE"""
    path_to_config = "D:\Sciebo\Programmierung\GIT\EBC_Database\Settings\settings_standard.ini"
    option_groups = "odbc_from"
    connection = EbcSql(option_files=path_to_config,
                                    option_groups=option_groups)
    connection.set_standard(option_files=path_to_config,
                            option_groups=["ts_database_from", "format"])

    ids_ordered_dict = OrderedDict([(1713, "b"), 
         (1714, "c"), 
         (1749, "d")])
    # ids_ordered_dict = OrderedDict([(1713, "B-4120//BOI.COND-H02_SEN.T-VL_WS.H.SUP.IN_MEA.T_AI"), 
    #      (1714, "B-4120//BOI.COND-H02_SEN.T-RL_WS.H.RET.OUT_MEA.T_AI"), 
    #      (1749, "B-4120//BOI.COND-H02_SEN.VF_WS.H_MEA.VF_AI")])
    # ids_ordered_dict = OrderedDict([(1713, "SEN.T-VL_WS.H.SUP.OUT_MEA.T_AI"), 
    #     (1714, "SEN.T-RL_WS.H.RET.IN_MEA.T_AI"), 
    #     (1749, "SEN.VF_WS.H_MEA.VF_AI")])



    time_start = "2016-12-02 00:00:00"
    time_end = "2016-12-03 00:00:00"






    time_start_df=dt.datetime.strptime(time_start, "%Y-%m-%d %H:%M:%S")
    data = connection.get_timeseries_df(ids=ids_ordered_dict,
                                    time_start=time_start,
                                    time_end=time_end,
                                    sort_by="ts_time_column",
                                    sort_order="ASC",
                                    use_query=True,
                                    get_last_value_before=True,
                                    replace_first_index=True)
    data.index = (data.index-time_start_df).total_seconds()
    data["e"]=data["d"]>0.0001
    data["e"]=data["d"]*1
    data["a"]=data.index.values
    data.reindex_axis(sorted(data.columns), axis=1)
    # df = data.to_string(header=False).split('\n')
    # print(data)
    # pd.options.display.float_format = '${:,.2f}'.format
    # print (data.to_string(formatters={'cost':'${:,.2f}'.format}))
    




    # s = df.index.tolist() + ',' + df["B-4120//BOI.COND-H02_SEN.T-VL_WS.H.SUP.OUT_MEA.T_AI"] + ',' + \
    #     df["B-4120//BOI.COND-H02_SEN.T-RL_WS.H.RET.IN_MEA.T_AI"] + ',' + \
    #     df["B-4120//BOI.COND-H02_SEN.VF_WS.H_MEA.VF_AI"] + ',' + \
    #     df["B-4120//BOI.COND-H02_SW_COM.CLEA_AO"]
    # s = df[["B-4120//BOI.COND-H02_SEN.T-VL_WS.H.SUP.OUT_MEA.T_AI", \
    #     "B-4120//BOI.COND-H02_SEN.T-RL_WS.H.RET.IN_MEA.T_AI", \
    #     "B-4120//BOI.COND-H02_SEN.VF_WS.H_MEA.VF_AI", \
    #     "B-4120//BOI.COND-H02_SW_COM.CLEA_AO"]].apply(lambda x: ', '.join(x), axis=1)
    # s = str(df.index.values.astype(str)) + ',' + str(df["B-4120//BOI.COND-H02_SEN.T-VL_WS.H.SUP.OUT_MEA.T_AI"].astype(str)) + ',' + \
    #     str(df["B-4120//BOI.COND-H02_SEN.T-RL_WS.H.RET.IN_MEA.T_AI"].astype(str)) + ',' + \
    #     str(["B-4120//BOI.COND-H02_SEN.VF_WS.H_MEA.VF_AI"].astype(str)) + ',' + \
    #     str(data["B-4120//BOI.COND-H02_SW_COM.CLEA_AO"].astype(str))
    # print(s)

    # data.to_csv("D:\Sciebo\Programmierung\GIT\_Standard\AixLib\AixLib\Fluid\BoilerCHP\Examples\export.csv")
    # scipy.io.savemat('test_struct.mat', {'struct':data.to_dict("list")}, long_field_names=True)
    scipy.io.savemat('test_struct.mat', {'struct': data.to_dict("list")}, long_field_names=False)
if __name__=="__main__":
    main()