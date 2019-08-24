import configparser
import pymysql
import pandas as pd
import re
import pyld
import warnings


class Budo(object):
    def __init__(self, language='English'):
        config = configparser.ConfigParser()
        config.read('budo_db.ini')
        self.connection = pymysql.connect(host=config["budo"]["server"], port=int(config["budo"]["port"]),
                                          user=config["budo"]["user"],
                                          passwd=config["budo"]["password"], db=config["budo"]["database"])
        # cursor = connection.cursor()
        # cursor.execute("SELECT * FROM abbreviation")
        # abbreviations = cursor.fetchall()
        query = "SELECT * FROM `abbreviation`"
        self.abb = pd.read_sql(query, self.connection)
        query = "SELECT * FROM `view.category_assignment`"
        self.ca = pd.read_sql(query, self.connection)
        query = "SELECT * FROM `view.parent_children`"
        self.pc = pd.read_sql(query, self.connection)
        query = "SELECT * FROM `languages`"
        languages = pd.read_sql(query, self.connection)
        self.c_abb = languages[languages['language'] == language]['column_abbreviation'][1]
        self.c_cat = languages[languages['language'] == language]['column_category'][1]
        self.c_par = languages[languages['language'] == language]['column_parent'][1]
        self.c_chi = languages[languages['language'] == language]['column_children'][1]

        self.categories_db = {'System': 'System',
                              'Subsystem': 'System',
                              'Subsubsystem': 'System',
                              'Medium 2nd specification': 'Medium 2nd specification',
                              'Medium 3rd specification': 'Medium 3rd specification',
                              'Signal type': 'Signal type',
                              'Signal type 2nd specification': 'Signal type 2nd specification',
                              'Function type': 'Function type'}

        self.categories_real = [['System', 'System specification', 'System designation'],
                                ['Subsystem', 'Subsystem specification', 'Subsystem designation'],
                                ['Subsubsystem', 'Subsubsystem specification', 'Subsubsystem designation'],
                                ['Medium', 'Medium specification', 'Medium 2nd specification',
                                 'Medium 3rd specification'],
                                ['Signal type', 'Signal type specification', 'Signal type 2nd specification'],
                                ['Function type']]

        # print(self.column_category)

    def decompose(self, budo_keys, category='all', separator_budo='#', separator_category='_',
                  separator_specification='+'):

        # print(self.c_abb)
        key_list = []
        raw_key = budo_keys.split(separator_budo)
        budo_c = raw_key[1].split(separator_category)
        last_element = ""
        for key, cat_r in zip(budo_c, self.categories_real):
            raw_element = key.split("-")
            if len(raw_element) == 2:
                raw_element = raw_element[0].split(separator_specification) + [raw_element[1]]
            elif len(raw_element) == 1:
                raw_element = raw_element[0].split(separator_specification)
            else:
                raw_element = []
            for element in raw_element:
                if cat_r in self.categories_db:
                    translation = self.get_translation(element, cat_r)
                elif "designation" in cat_r:
                    translation = element
                else:
                    translation = self.get_translation_children(last_element, element)
                last_element = element

            # key_list.append([cat_r, budo_translation])
            # print(budo_translation)
        # print(key_list)

        return raw_key, budo

    def get_translation(self, budo_element, category):
        if self.check_abbreviation(budo_element):
            budo_temp = self.abb[self.abb['budo'] == budo_element][self.c_abb].values.tolist()
            budo_translation = self.ca[(self.ca[self.c_abb].isin(budo_temp))]
            budo_translation = budo_translation[budo_translation[
                self.c_cat] == category][self.c_abb].to_string(
                index=False,
                header=False)
            if "Series([], )" in budo_translation:
                budo_translation = ""
            # print(budo_translation)
        else:
            warnings.warn('"' + budo_element + '" is not a Budo abbreviation', RuntimeWarning)
            budo_translation = "not available"

        return budo_translation

    def get_translation_children(self, budo_parent, budo_children):
        if self.check_abbreviation(budo_parent) and self.check_abbreviation(budo_children):
            budo_parent_temp = self.abb[self.abb['budo'] == budo_parent][self.c_abb].values.tolist()
            budo_children_temp = self.abb[self.abb['budo'] == budo_children][self.c_abb].values.tolist()
            # budo_parent_children_translation
            budo_pct = self.pc[(self.pc[self.c_par].isin(budo_parent_temp)) and
                               (self.pc[self.c_chi].isin(budo_children_temp))]
        else:
            warnings.warn('"' + budo_parent + '" and "' + budo_children + '" is not a valid relation',
                          RuntimeWarning)
            budo_translation = "not available"

        return budo_translation

    def check_abbreviation(self, abbreviation):
        return not self.abb[self.abb['budo'] == abbreviation].empty


if __name__ == "__main__":
    budo_key = "B-4120#BOI+COND-1_SEN+T-B01__W+H+FLO+IN_MEA+T_BO#U-DEGC"
    budo = Budo()
    budo_split, budo_parts = budo.decompose(budo_keys=budo_key)
    print(budo_split)
    # print(budo_parts)
    # print(budo.check_abbreviation("BOI"))

    # print(budo.get_translation("TESTITEST", "System"))
