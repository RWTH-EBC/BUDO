import itertools
import os
import re
import sys
from collections import defaultdict
import modelicares
import pytest
import numpy as np


from dymola.dymola_interface import DymolaInterface

# def list_variables(filename, search_string):
#     dymola = DymolaInterface()
#     list_var=dymola.list(filename, variables={search_string})
#     return list_var



# def get_variable_name_old(filename, search_string):
#     lines, index = get_line_index(filename, search_string)
#     value = True
#     counter = 0
#     while value:
#         counter = count_braces(str(lines[index]), counter)
#         if counter == 0:
#             value = False
#         if str(lines[index]).count(";") >= 1:
#             index += 1
#             value = False
#         if value == False:
#             variable_name = get_string_name(str(lines[index]))
#         index -= 1
#     return variable_name


def get_variable_name(filename, search_string):
    lines, index = get_line_index(filename, search_string)

    while index>-1 and str(lines[index]).count(";") < 1:
        index -= 1
    index += 1 
    while count_letters(str(lines[index]))<=0:
        index += 1
    if str(lines[index]).count(" model ") >= 1:
        index += 1
    variable_name = get_string_name(str(lines[index]))
    return variable_name


# def count_braces(string, counter):
#     counter = counter+string.count(")")
#     counter = counter-string.count("(")
#     return counter



def get_complete_variable_name(filename, budo_label):
    (system_budo, subsystem_budo) = disjoin_chunks_budo(budo_label)
    system_sim=get_variable_name(filename, system_budo)
    subsystem_sim=get_variable_name(filename, subsystem_budo)
    # indizes=find(subsystem_sim, "_")
    data_point_type=get_data_point_type(subsystem_budo)
    complete_variable_name=system_sim+"."+subsystem_sim+"."+data_point_type
    return complete_variable_name


def get_data_point_type(budo_label):
    if "MEA.T" in budo_label:
        # temperature
        additional="T"
    elif "MEA.P" in budo_label:
        # absolute pressure
        additional="p"
    elif "HUM.REL" in budo_label:
        # relative humidity
        additional="phi"
    elif "MEA.MF" in budo_label:
        # mass flow
        additional="m_flow"
    elif "MEA.T.DIF" in budo_label:
        # temperature difference
        additional=""
    elif "MEA.VF" in budo_label:
        # volume flow
        additional="V_flow"
    elif "MEA.test" in budo_label:
        additional=""
    else:
        raise ValueError('data point type is not defined')
    return additional



def get_lines(filename):
    searchfile = open(filename, 'r')
    lines = [line.split('\n') for line in searchfile.readlines()]
    try:
        [r.pop(1) for r in lines]
    except:
        pass
    return lines

def get_line_index(filename, search_string):
    lines = get_lines(filename)
    for line1 in lines:
        if search_string in str(line1[0]):
            index = lines.index(line1)
            return lines, index
    try:
        index
    except NameError:
        print("No index found")
    return lines, index





def get_string_name(string):
    string = re.sub(r'\s+', ' ', string)
    if string.count(' ') > 1:
        index_start = string.find(' ')
        index_start = string.find(' ', index_start+1)
    else:
        index_start = string.find(' ')
    if string.count('(') >= 1:
        index_end = string.find('(')
    elif string.count('"') >= 1:
        index_end = string.find('"')-1
    else:
        index_end = len(string)

    value = string[index_start+1:index_end]
    # print(value)
    return value








def disjoin_chunks_budo(budo_label):
    # underscores = find(budo_label, "_")
    double_slash = budo_label.find("//")
    underscore = budo_label.find("_", double_slash)
    # system = budo_label[double_slash+2:underscore]
    system = budo_label[:underscore]
    subsystem = budo_label[underscore+1:]
    return system, subsystem


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def count_letters(line):
    count = len(re.findall('[a-zA-Z]', line))
    return count

def get_index(filename, search_string):
    
    with open(filename, 'r') as f:
        content = f.read()
        variable_name = content.index(search_string)
        print(variable_name)
    return variable_name

def test_get_line_index():
    print("to be tested")
    assert get_line_index("Test_BUDO.mo", 'switchToNightMode1')[1] == 31
    assert get_line_index(
        "Test_BUDO.mo", '"SEN.T-B06_WS.H.RET.PRIM_MEA.T_AI"')[1] == 43
    assert get_line_index("Test_BUDO.mo", '"BOI-H02.1"')[1] == 16
    assert get_line_index("test_get_variable_name.txt", "boiler")[1] == 0
    assert get_line_index("test_get_variable_name.txt", '"H02-B01"')[1] == 3
    assert get_line_index("Test_BUDO.mo", 'package Test_BUDO')[1] == 1


def test_get_string_name():
    assert get_string_name(
        '            AixLib.Fluid.BoilerCHP.Boiler boiler(redeclare package Medium =') == 'boiler'
    assert get_string_name(
        '    Modelica.Blocks.Interfaces.RealInput TAmbient1 "Ambient air temperature"') == 'TAmbient1'
    assert get_string_name(
        '    AixLib.Fluid.Sensors.Temperature temperature_sensor_2(redeclare package') == 'temperature_sensor_2'
    assert get_string_name(
        '    Modelica.Blocks.Interfaces.BooleanInput switchToNightMode1') == 'switchToNightMode1'

def test_get_data_point_type():
    assert get_data_point_type("SEN.T-B06_WS.H.RET.PRIM_MEA.T_AI")=="T"



def test_get_variable_name():
    assert get_variable_name("Test_BUDO.mo", '"BOI-H02.1"') == 'boiler'
    assert get_variable_name(
        "test_get_variable_name.txt", '"H02-B01"') == 'boiler'
    assert get_variable_name("Test_BUDO.mo", '"4120//BOI-H02.1"') == 'boiler_system'
    assert get_variable_name(
        "Test_BUDO.mo", '"SEN.T-B06_WS.H.RET.PRIM_MEA.T_AI"') == 'temperature_sensor_2'
    assert get_variable_name(
        "Test_BUDO.mo", '"SEN.T-B01_WS.H.SUP.PRIM_MEA.T_AI"') == 'temperature_sensor_1'
        
def test_get_complete_variable_name():
    assert get_complete_variable_name("Test_BUDO.mo", "4120//BOI-H02.1_SEN.T-B01_WS.H.SUP.PRIM_MEA.T_AI") =="boiler_system.temperature_sensor_1.T"
    assert get_complete_variable_name("Test_BUDO.mo", "4120//BOI-H02.1_SEN.T-B06_WS.H.RET.PRIM_MEA.T_AI") =="boiler_system.temperature_sensor_2.T"

# def test_count_braces():
#     assert count_braces(
#         '      m_flow_nominal=2)                                             "H02.1"', 0) == 1

def test_disjoint_chunks_budo():
    assert disjoin_chunks_budo(
        "4120//BOI-H02.1_SEN.T-B01_WS.H.SUP.PRIM_MEA.T_AI") == ("4120//BOI-H02.1", "SEN.T-B01_WS.H.SUP.PRIM_MEA.T_AI")

def test_count_letters():
    assert count_letters("abc1234543543")==3
    assert count_letters("          ")==0
    assert count_letters("    import AixLib;")==12
    assert count_letters("          rotation=90,")==8


if __name__ == "__main__":
    filename = "Test_BUDO.mo"
    search_string = '"H02.1"'
    # abc=get_variable_name(filename, search_string)
    budo_label = "4120//BOI-H02.1_SEN.T-B01_WS.H.SUP.PRIM_MEA.T_AI"
    # system, subsystem = disjoin_chunks_budo(budo_label)
    # print(system)
    # print(subsystem)


    # check_heatflow()

    # print(find(budo_label, "_"))
    

    # (system, subsystem) = disjoin_chunks_budo(budo_label)
    # print(system, subsystem)



    # abc=all_occurences(open("Test_BUDO.mo").read(),'(')
    # abc=all_occurences("Test_BUDO.mo",'(')
    # abc=list_variables("Test_BUDO.mo",'*"H02.1"*')
    # print(abc)
    # get_index(filename, search_string)
    # read_mat()


    # test_count_letters()
    test_get_line_index()
    test_get_string_name()

    test_get_variable_name()
    test_disjoint_chunks_budo()
    
    # test_get_data_point_type()
    test_get_complete_variable_name()
    