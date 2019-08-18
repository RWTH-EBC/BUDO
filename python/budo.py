import configparser
import pymysql


class budo():
    config = configparser.ConfigParser()
    config.read('budo_db.ini')
    conn=pymysql.connect(host=config["budo"]["server"], port=int(config["budo"]["port"]), user=config["budo"]["user"],
                    passwd=config["budo"]["password"], db=config["budo"]["database"])
    cur = conn.cursor()

    def get(self, budo_keys, type='english', category='all', seperator_budo='|', seperator_category='_', seperator_specification='+'):
        self.cur.execute("SELECT * FROM users")

        return budo_keys










if __name__ == "__main__":
    budo_key="B-4120|BOI+COND-1_SEN+T-B01__W+H+FLO+IN_MEA+T_BO|U-DEGC"
    budo=budo()











