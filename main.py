import requests
import json
import os
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from utils import luatable
import getopt
import sys

engine = sqlalchemy.create_engine("sqlite:///kancolle.db")
db_base = declarative_base()


class Equipment(db_base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)
    jp_name = Column(String(128))
    cn_name = Column(String(128), default="-1")
    type_0 = Column(Integer)
    type_1 = Column(Integer)
    type_2 = Column(Integer)
    type_3 = Column(Integer)
    type_4 = Column(Integer)
    rarity = Column(Integer)
    state = Column(Integer, default=-1)
    fire = Column(Integer)
    torpedo = Column(Integer)
    bomb = Column(Integer)
    airpower = Column(Integer)
    antisubmarine = Column(Integer)
    hit = Column(Integer)
    dodge = Column(Integer)
    scout = Column(Integer)
    range = Column(String(128))
    adapt = Column(String, default="-1")
    disassembly_fuel = Column(Integer)
    disassembly_ammo = Column(Integer)
    disassembly_steel = Column(Integer)
    disassembly_bauxite = Column(Integer)
    armor = Column(Integer)

    def __repr__(self):
        if self.id < 10:
            str_id = "00" + str(self.id)
        elif self.id < 100:
            str_id = "0" + str(self.id)
        else:
            str_id = str(self.id)

        lst_type = [self.type_0, self.type_1, self.type_2, self.type_3, self.type_4]
        dict_disassembly = {"燃料": self.disassembly_fuel,
                            "弹药": self.disassembly_ammo,
                            "钢材": self.disassembly_steel,
                            "铝": self.disassembly_bauxite}
        str_rarity = ""
        for count in range(self.rarity):
            str_rarity = str_rarity + "☆"
        dict_attribute = {"射程": self.range}
        if self.fire != 0:
            dict_attribute["火力"] = self.fire
        elif self.torpedo != 0:
            dict_attribute["雷装"] = self.torpedo
        elif self.airpower != 0:
            dict_attribute["对空"] = self.airpower
        elif self.armor != 0:
            dict_attribute["装甲"] = self.armor
        elif self.bomb != 0:
            dict_attribute["爆装"] = self.bomb
        elif self.antisubmarine != 0:
            dict_attribute["对潜"] = self.antisubmarine
        elif self.hit != 0:
            dict_attribute["命中"] = self.hit
        elif self.dodge != 0:
            dict_attribute["回避"] = self.dodge
        elif self.scout != 0:
            dict_attribute["索敌"] = self.scout
        repr_dict = {
                    str_id: {
                             "ID": str_id,
                             "日文名": self.jp_name,
                             "类别": lst_type,
                             "稀有度": str_rarity,
                             "属性": dict_attribute,
                             "废弃": dict_disassembly,
                             "装备适用": {}}}

        return json.dumps(repr_dict, ensure_ascii=False)


class Ship(db_base):
    __tablename__ = "ship"

    id = Column(Integer, primary_key=True)
    kcwiki_id = Column(Integer)
    illustrate_id = Column(Integer)
    jp_name = Column(String(128))
    yomi_name = Column(String(128))
    cn_name = Column(String(128), default="-1")
    ship_type = Column(Integer)
    ship_class = Column(Integer)
    durability_original = Column(Integer)
    durability_married = Column(Integer)
    fire_original = Column(Integer)
    fire_max = Column(Integer)
    torpedo_original = Column(Integer)
    torpedo_max = Column(Integer)
    airpower_original = Column(Integer)
    airpower_max = Column(Integer)
    armor_original = Column(Integer)
    armor_max = Column(Integer)
    antisubmarine = Column(Integer)
    dodge_original = Column(Integer, default=-1)
    dodge_max = Column(Integer, default=-1)
    scout_original = Column(Integer, default=-1)
    scout_max = Column(Integer, default=-1)
    luck_original = Column(Integer)
    luck_max = Column(Integer)
    speed = Column(Integer)
    range = Column(Integer)
    rarity = Column(Integer)
    slots = Column(Integer)
    aircraft_mount_1 = Column(Integer, default=-1)
    aircraft_mount_2 = Column(Integer, default=-1)
    aircraft_mount_3 = Column(Integer, default=-1)
    aircraft_mount_4 = Column(Integer, default=-1)
    aircraft_mount_5 = Column(Integer, default=-1)

    original_equipment_1 = Column(Integer, default=-1)
    original_equipment_2 = Column(Integer, default=-1)
    original_equipment_3 = Column(Integer, default=-1)
    original_equipment_4 = Column(Integer, default=-1)
    original_equipment_5 = Column(Integer, default=-1)

    can_drop = Column(Integer, default=-1)
    can_build = Column(Integer, default=-1)
    can_remodel = Column(Integer, default=-1)
    build_time = Column(Integer)

    max_fuel = Column(Integer)
    max_ammo = Column(Integer)

    powerup_fire = Column(Integer)
    powerup_torpedo = Column(Integer)
    powerup_airpower = Column(Integer)
    powerup_armor = Column(Integer)

    disassembly_fuel = Column(Integer)
    disassembly_ammo = Column(Integer)
    disassembly_steel = Column(Integer)
    disassembly_bauxite = Column(Integer)

    remodel_level = Column(Integer)
    remodel_ammo = Column(Integer)
    remodel_steel = Column(Integer)
    remodel_before = Column(Integer, default=-1)
    remodel_after = Column(Integer, default=-1)

    illustrator = Column(String(128), default="-1")
    character_voice = Column(String(128), default="-1")

    def __repr__(self):
        slots = []
        if self.id < 10:
            str_id = "00" + str(self.id)
        elif self.id < 100:
            str_id = "0" + str(self.id)
        else:
            str_id = str(self.id)

        for count in range(self.slots):
            slots.append(-1)

        repr_dict = {
            str_id: {
                     "ID": self.kcwiki_id,
                     "图鉴号": self.illustrate_id,
                     "日文名": self.jp_name,
                     "假名": self.yomi_name,
                     "中文名": self.cn_name,
                     "舰种": self.ship_type,
                     "级别": "-1",
                     "数据": {
                              "耐久": [self.durability_original, self.durability_married],
                              "火力": [self.fire_original, self.fire_max],
                              "雷装": [self.torpedo_original, self.torpedo_max],
                              "对空": [self.airpower_original, self.airpower_max],
                              "装甲": [self.armor_original, self.armor_max],
                              "对潜": [self.antisubmarine],
                              "回避": [self.dodge_original, self.dodge_max],
                              "索敌": [self.scout_original, self.scout_max],
                              "运": [self.luck_original, self.luck_max],
                              "速力": self.speed,
                              "射程": self.range,
                              "稀有度": self.rarity
                      },
                     "装备": {
                             "格数": self.slots,
                             "搭载": slots,
                             "初期装备": slots,
                            },
                     "获得": {
                             "掉落": self.can_drop,
                             "改造": self.can_remodel,
                             "建造": self.can_build,
                             "时间": self.build_time
                             },
                     "消耗": {
                             "燃料": self.max_fuel,
                             "弹药": self.max_ammo,
                            },
                     "改修": {
                              "火力": self.powerup_fire,
                              "雷装": self.powerup_torpedo,
                              "对空": self.powerup_airpower,
                              "装甲": self.powerup_armor
                             },
                     "解体": {
                              "燃料": self.disassembly_fuel,
                              "弹药": self.disassembly_ammo,
                              "钢材": self.disassembly_steel,
                              "铝": self.disassembly_bauxite
                             },
                     "改造": {
                              "等级": self.remodel_level,
                              "弹药": self.remodel_ammo,
                              "钢材": self.remodel_steel,
                              "改造前": self.remodel_before,
                              "改造后": self.remodel_after
                            },
                     "画师": self.illustrator,
                     "声优": self.character_voice
            }
        }

        return json.dumps(repr_dict, ensure_ascii=False)


db_base.metadata.create_all(engine)
db_session = sessionmaker(bind=engine)


r = requests.get("http://api.kcwiki.moe/start2")


dict_start2 = r.json()
map_range = {"0": "-1",
             "1": "短",
             "2": "中",
             "3": "长",
             "4": "超长",
             "5": "超超长"}

# print(json.dumps(dict_start2["api_mst_ship"][0], ensure_ascii=False))
# print(json.dumps(dict_start2["api_mst_slotitem"][0], ensure_ascii=False))


def process_equipment():
    db = db_session()
    dict_equipment = dict_start2["api_mst_slotitem"]
    for equipment in dict_equipment:
        if "api_distance" in equipment.keys():
            equip_range = equipment["api_distance"]
        else:
            equip_range = map_range[str(equipment["api_leng"])]

        equipment_info = Equipment(id=equipment["api_id"], jp_name=equipment["api_name"], type_0=equipment["api_type"][0],
                                   type_1=equipment["api_type"][1], type_2=equipment["api_type"][2], type_3=equipment["api_type"][3],
                                   type_4=equipment["api_type"][4], rarity=equipment["api_rare"], fire=equipment["api_houg"],
                                   torpedo=equipment["api_raig"], bomb=equipment["api_baku"], airpower=equipment["api_tyku"],
                                   antisubmarine=equipment["api_tais"], hit=equipment["api_houm"], dodge=equipment["api_houk"],
                                   scout=equipment["api_saku"], armor=equipment["api_souk"], range=equip_range,
                                   disassembly_fuel=equipment["api_broken"][0], disassembly_ammo=equipment["api_broken"][1],
                                   disassembly_steel=equipment["api_broken"][2], disassembly_bauxite=equipment["api_broken"][3])

        db.add(equipment_info)
        db.commit()


def process_ships():
    db = db_session()
    dict_ships = dict_start2["api_mst_ship"]
    for ship in dict_ships:
        if ship["api_sort_id"] == 0:
            continue
        if "api_tais" in ship.keys():
            antisubmarine = ship["api_tais"][0]
        else:
            antisubmarine = 0
        ship_info = Ship(id=ship["api_id"], kcwiki_id=ship["api_id"], illustrate_id=ship["api_sortno"], jp_name=ship["api_name"],
                         yomi_name=ship["api_yomi"], ship_type=ship["api_stype"], ship_class=ship["api_ctype"],
                         durability_original=ship["api_taik"][0], durability_married=ship["api_taik"][1],
                         armor_original=ship["api_souk"][0], armor_max=ship["api_souk"][1], fire_original=ship["api_houg"][0],
                         fire_max=ship["api_houg"][1], torpedo_original=ship["api_raig"][0], torpedo_max=ship["api_raig"][1],
                         airpower_original=ship["api_tyku"][0], airpower_max=ship["api_tyku"][1],
                         antisubmarine=antisubmarine, luck_original=ship["api_luck"][0],
                         luck_max=ship["api_luck"][1], speed=ship["api_soku"], range=ship["api_leng"], slots=ship["api_slot_num"],
                         build_time=ship["api_buildtime"], disassembly_fuel=ship["api_broken"][0], disassembly_ammo=ship["api_broken"][1],
                         disassembly_steel=ship["api_broken"][2], disassembly_bauxite=ship["api_broken"][3],
                         powerup_fire=ship["api_powup"][0], powerup_torpedo=ship["api_powup"][1], powerup_airpower=ship["api_powup"][2],
                         powerup_armor=ship["api_powup"][3], rarity=ship["api_backs"], remodel_ammo=ship["api_afterbull"],
                         remodel_steel=ship["api_afterfuel"], remodel_level=ship["api_afterlv"], max_fuel=ship["api_fuel_max"],
                         max_ammo=ship["api_bull_max"])
        db.add(ship_info)
        db.commit()


def generate_db():
    db = db_session()
    if not db.query(Equipment).all():
        print("generating new DB from start2 api:")
        process_equipment()
        process_ships()


if __name__ == "__main__":
    try:
        options, args = getopt.getopt((sys.argv[1:]), "hce:s:", ["help", "clean", "equip", "ship"])

    except getopt.GetoptError:
        print("usage: generator.py (--celan) ")
    db = db_session()
    for name, value in options:
        if name in ("-c", "--clean"):
            os.remove(os.getcwd()+"/kancolle.db")
            print("Database has been removed.")
            sys.exit(0)
        elif name in ("-h", "--help"):
            print("usage: generator.py (--celan) (--equip) (--ship)")

    generate_db()
    equip = db.query(Equipment).all()
    for each in equip:

        name = os.getcwd() + '/equipments/' + str(list(json.loads(str(each)))[0]) + ".lua"
        with open(name, 'w') as f:
            f.write(luatable(json.loads(str(each))))

    ship = db.query(Ship).all()
    for each in ship:
        name = os.getcwd() + '/ships/' + str(list(json.loads(str(each)))[0]) + ".lua"
        with open(name, 'w') as f:
            f.write(luatable(json.loads(str(each))))
