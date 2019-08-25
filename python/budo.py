import configparser
import pymysql
import pandas as pd
import re
import pyld
import warnings


class Budo(object):
    def __init__(self, language='English', separator_budo='#', separator_category='_',
                 separator_specification='+'):
        self.sep_budo = separator_budo
        self.sep_cat = separator_category
        self.sep_spec = separator_specification

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
                              'Medium': 'Medium',
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

    def get_translation(self, budo_keys):
        budo_parts = self.decompose_budo_key(budo_keys)
        budo_key_list = [""] * 3
        budo_key_list[0] = self.get_translation_outside_parts(budo_parts[0])
        budo_key_list[1] = self.translate_budo_part(budo_parts[1])
        budo_key_list[2] = self.get_translation_outside_parts(budo_parts[2])

        return budo_key_list

    def decompose_budo_key(self, budo_key):
        budo_decompose = [""] * 3
        raw_key = budo_key.split(self.sep_budo)

        if len(raw_key) == 1:
            budo_decompose[0] = []
            budo_decompose[1] = raw_key[0].split(self.sep_cat)
            budo_decompose[2] = []

        elif len(raw_key) == 2:
            if raw_key[0].count(self.sep_cat) >= raw_key[1].count(self.sep_cat):
                budo_decompose[0] = []
                budo_decompose[1] = raw_key[0].split(self.sep_cat)
                budo_decompose[2] = raw_key[1].split(self.sep_cat)

            elif raw_key[0].count(self.sep_cat) < raw_key[1].count(self.sep_cat):
                budo_decompose[0] = raw_key[0].split(self.sep_cat)
                budo_decompose[1] = raw_key[1].split(self.sep_cat)
                budo_decompose[2] = []

        elif len(raw_key) == 3:
            budo_decompose[0] = raw_key[0].split(self.sep_cat)
            budo_decompose[1] = raw_key[1].split(self.sep_cat)
            budo_decompose[2] = raw_key[2].split(self.sep_cat)
        else:
            raise RuntimeError('{} {} {}'.format('Key', budo_key, 'is not in Budo format'))

        return budo_decompose

    def translate_budo_part(self, budo_part):
        # print(self.c_abb)
        budo_part_list = []
        last_element = ""
        for key, cat_r in zip(budo_part, self.categories_real):
            temp_list = []
            raw_element = self.decompose_element(key)

            for element, cat_temp in zip(raw_element, cat_r):
                if cat_temp in self.categories_db:
                    translation = self.get_translation_category(element, cat_temp)

                elif "designation" in cat_temp:
                    if len(element) > 0:
                        translation = element
                    else:
                        translation = ""
                else:
                    _, translation = self.get_translation_children(last_element, element)
                last_element = element
                temp_list.append([cat_temp, translation])
            budo_part_list.append(temp_list)
        return budo_part_list

    def decompose_element(self, element):
        raw_element = []
        keys = element.split(self.sep_spec)
        for key in keys:
            raw_element.append(key.split("-")[0])
        if "-" in element:
            raw_element.append(element.split("-")[1])
        return raw_element

    def get_translation_outside_parts(self, budo_part):
        outside_list = []
        # outside_elements = budo_part.split(self.sep_cat)
        for element in budo_part:
            translation = self.get_translation_outside_elements(element)
            outside_list.append(translation)
        return outside_list

    def get_translation_outside_elements(self, budo_element):
        if "-" in budo_element:
            chunks = budo_element.split("-")
            designation = chunks[1]
        else:
            designation = ""
        name = self.abb[self.abb['budo'] == chunks[0]][self.c_abb].to_string(
            index=False, header=False)
        return [name, designation]

    def get_translation_category(self, budo_element, category):
        if self.check_abbreviation(budo_element):
            budo_temp = self.abb[self.abb['budo'] == budo_element][self.c_abb].values.tolist()
            budo_translation = self.ca[(self.ca[self.c_abb].isin(budo_temp))]
            budo_translation = budo_translation[budo_translation[
                                                    self.c_cat] == self.categories_db[category]][self.c_abb].to_string(
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

            df_par = self.pc[(self.pc[self.c_par].isin(budo_parent_temp))]
            df_chi = self.pc[(self.pc[self.c_chi].isin(budo_children_temp))]

            budo_pct = df_par.merge(df_chi, on=[self.c_par, self.c_chi])

            parent = budo_pct[self.c_par].to_string(index=False, header=False)
            children = budo_pct[self.c_chi].to_string(index=False, header=False)
        else:
            warnings.warn('"' + budo_parent + '" and "' + budo_children + '" is not a valid relation',
                          RuntimeWarning)
            parent = "not available"
            children = "not available"

        return parent, children

    def check_abbreviation(self, abbreviation):
        return not self.abb[self.abb['budo'] == abbreviation].empty


if __name__ == "__main__":
    budo_key = "B-4120#BOI+COND-1_SEN+T-B01__W+H+FLO+IN_MEA+T_BO#U-DEGC"
    budo = Budo()

    # budo_parent, budo_children = budo.get_translation_children("BOI", "COND")
    # print(budo_parent)
    # print(budo_children)

    # budo_split = budo.decompose_budo(budo_key=budo_key)
    #
    # print(budo_split)
    #
    # budo_key = "B-4120#BOI+COND-1_SEN+T-B01__W+H+FLO+IN_MEA+T_BO"
    # budo_split = budo.decompose_budo(budo_key=budo_key)
    # print(budo_split)
    #
    # budo_key = "BOI+COND-1_SEN+T-B01__W+H+FLO+IN_MEA+T_BO"
    # budo_split = budo.decompose_budo(budo_key=budo_key)
    # print(budo_split)

    budo_list1 = budo.get_translation(budo_keys=budo_key)
    print(budo_list1)

    # list1 = budo.get_translation_outside("B-4120")
    # print(list1)

    # list1 = budo.decompose_element("W+H+FLO+IN")
    # print(list1)

    # print(budo.check_abbreviation("BOI"))

    # print(budo.get_translation("TESTITEST", "System"))
