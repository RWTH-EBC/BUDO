import configparser
import pymysql
import pandas as pd
import re
import pyld
import warnings


class Budo(object):
    def __init__(self, language='English', separator_budo='§', separator_category='_',
                 separator_specification='+', separator_designation='-', budo_file='budo_db.ini', translate=True):
        self.sep_budo = separator_budo
        self.sep_cat = separator_category
        self.sep_spec = separator_specification
        self.sep_desig = separator_designation
        self.language = language

        config = configparser.ConfigParser()
        config.read(budo_file)
        self.connection = pymysql.connect(host=config["budo"]["server"], port=int(config["budo"]["port"]),
                                          user=config["budo"]["user"],
                                          passwd=config["budo"]["password"], db=config["budo"]["database"])
        query = "SELECT * FROM `cpc_all`"
        self.cpc_all = pd.read_sql(query, self.connection)
        query = "SELECT * FROM `view.category`"
        self.categories = pd.read_sql(query, self.connection)
        self.translate = translate
        if translate:
            self.dict_cpc = self.get_index()
            self.dict_cat_budo = self._init_translation()

    def _init_translation(self):
        dict_cat_budo = dict()
        categories_dict_orig = {"medium 2nd specification": "medium specification 2",
                                "medium 3rd specification": "medium specification 3",
                                "signal type 2nd specification": "signal type specification 2",
                                "signal type 3rd specification": "signal type specification 3"}
        self.categories_budo = self.categories[["name_english", "budo"]]
        for index, row in self.categories_budo.iterrows():
            if row["name_english"] in categories_dict_orig.keys():
                dict_cat_budo[categories_dict_orig[row["name_english"]]] = row["budo"]
            else:
                dict_cat_budo[row["name_english"]] = row["budo"]
        return dict_cat_budo

    def get_index(self):
        cat_budo_stand = self.categories[self.categories['comment'] == 'not used as abbreviation']["budo"].tolist()

        df = self.cpc_all[['category_english', 'category_german', 'category_budo',
                           'ca_english', 'ca_german', 'ca_budo',
                           'children_english', 'children_german', 'children_budo']]

        # categories = self.categories[['name_english']]
        dict_all = dict()
        for index, row in self.categories.iterrows():
            budo_cat = row["budo"]

            dict_cat = dict()
            dict_cat["name_english"] = row["name_english"]
            dict_cat["name_german"] = row["name_german"]
            if row["parent_category_id"] > 0:
                name_category = row["parent_category_english"]
            else:
                name_category = row['name_english']
            cas = df[df['category_english'] == name_category]['ca_english'].unique()
            df_cas = df[df['category_english'] == name_category]
            for ca in cas:
                if ca is not None:
                    dict_ca = dict()
                    dict_ca["name_english"] = ca
                    dict_ca["name_german"] = df_cas[df_cas.ca_english == ca]["ca_german"].iloc[0]

                    df_ca = df_cas[df_cas.ca_english == ca]
                    children = df_cas[df_cas.ca_english == ca]['children_english'].tolist()

                    for child in children:
                        if child is not None:
                            dict_child = dict()
                            dict_child["name_english"] = child
                            dict_child["name_german"] = df_ca[df_ca.children_english == child]["children_german"].iloc[0]

                            budo_child = df_ca[df_ca.children_english == child]["children_budo"].iloc[0]
                            if budo_child is not None:
                                if budo_cat in cat_budo_stand:
                                    dict_ca[budo_child] = dict_child
                                else:
                                    dict_cat[budo_child] = dict_child

                    budo_ca = df_cas[df_cas.ca_english == ca]["ca_budo"].iloc[0]
                    if budo_ca is not None:
                        dict_cat[budo_ca] = dict_ca
            dict_all[budo_cat] = dict_cat
        return dict_all

    def split(self, budo_keys, translate=None):
        if translate is None:
            translate = self.translate

        dict_keys = dict()
        budo_cat = ""
        budo_ca = ""
        # budo_child = ""
        categories = ["system", "subsystem", "subsubsystem",
                      "medium", "signal type", "function type"]

        language = self.language.lower()

        for n, key in enumerate(budo_keys, start=0):
            dict_key = dict()
            free_cat_enumerator = 1
            name_category = ""
            parts = key.split(self.sep_budo)
            for i, part in enumerate(parts, start=0):
                elements = part.split(self.sep_cat)
                for j, element in enumerate(elements, start=0):
                    if i in [0, 2]:
                        name_category = "free category " + str(free_cat_enumerator)
                        free_cat_enumerator += 1
                    elif i == 1:
                        name_category = categories[j]
                    blocks = element.split(self.sep_desig)
                    for k, block in enumerate(blocks, start=0):
                        if k == 0:
                            chunks = block.split(self.sep_spec)

                            for m, chunk in enumerate(chunks, start=0):
                                if m == 0:
                                    if translate and chunk is not "":
                                        if i in [0, 2]:
                                            budo_cat = chunk
                                            dict_key[name_category] = self.dict_cpc[budo_cat][
                                                "name_"+language]
                                        elif i == 1:
                                            budo_cat = self.dict_cat_budo[name_category]
                                            budo_ca = chunk
                                            dict_key[name_category] = self.dict_cpc[budo_cat][chunk][
                                                    "name_"+language]
                                    else:
                                        dict_key[name_category] = chunk
                                elif m == 1:
                                    if translate and chunk is not "":
                                        if i in [0, 2]:
                                            dict_key[name_category + " specification " + str(m)] = self.dict_cpc[
                                                budo_cat][chunk]["name_" + language]
                                        elif i == 1:
                                            dict_key[name_category + " specification " + str(m)] = self.dict_cpc[
                                                budo_cat][budo_ca][chunk]["name_" + language]
                                    else:
                                        dict_key[name_category + " specification " + str(m)] = chunk
                                else:
                                    if translate and chunk is not "":
                                        # name_category_orig = categories_dict_orig[name_category + " specification " + str(m)]
                                        budo_spec = self.dict_cat_budo[name_category + " specification " + str(m)]
                                        dict_key[name_category + " specification " + str(m)] = self.dict_cpc[
                                            budo_spec]["name_" + language]
                                    else:
                                        dict_key[name_category + " specification " + str(m)] = chunk

                        elif k == 1:
                            dict_key[name_category + " designation"] = block
            dict_keys[key] = dict_key
        return dict_keys


if __name__ == '__main__':
    import pprint

    bt = Budo(language="German", translate=True)
    # dict_all0 = bt.get_index()
    pp = pprint.PrettyPrinter(depth=5)
    # pp.pprint(bt.dict_cpc)
    budo_keys = [
        "AE-abc_FL.CC+ROO-00_CTRY-GER_SZ-01_CN.N-1§BOI+COND-01_WST-01_SEN+P.ATM-01_WS+H+OUT+MID-1_MEA+T+SP-abc_AI§U+.C_B+GREEN_FL+BASE.1_DS-01_CG-01",
        "AE-abc_FL.CC+BASE-00_CTRY-GER_SZ-01_CN.N-1§BOI+COND-01_CH+ADS-01_SEN+T-01_WS+H++MID-1_MEA++SP-abc_AI§U+T_B+GREEN_FL+BASE.1_DS-01_CG-01",
        "B+RESP-4120_MG§CHP-01_SEN+T-01__WS+H+IN_MEA+T_§U+.C"]
    # dict_cc = bt.split(budo_keys)

    # print(dict_cc)

    import timeit, functools
    t = timeit.Timer(functools.partial(bt.split, budo_keys))
    print(t.timeit(10))
    print(t.timeit(100))
    print(t.timeit(1000))
    print(t.timeit(10000))
