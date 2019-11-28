from collections import defaultdict
import sys
import random

def judge_picture(descriptions):
    descriptions = set(descriptions)
    result = defaultdict(str)

    thunder = {"Lightning", "Thunderstorm", "Thunder", "Thunderbolt"}
    fire = {"Fire", "Blaze", "Flame", "Magma","Heat"}
    water = {"Aqua", "Water", "Liquid", "Fluid"}
    ice = {"Ice", "Iceberg", "Frozen", "Cold", "Freeze", "Snow", "Frost"}
    dragon = {"Dragon", "Draco", "Drake", "Dragoon"}

    thunder_is = thunder & descriptions
    fire_is = fire & descriptions
    water_is = water & descriptions
    ice_is = ice & descriptions
    dragon_is = dragon & descriptions
    # print(descriptions, file = sys.stderr)
    # print(thunder_is, file = sys.stderr)
    attribution = max(thunder_is, fire_is, water_is, ice_is, dragon_is, key=lambda x: len(x))
    if attribution == thunder_is:
        result["attribution"] = "雷"
    elif attribution == fire_is:
        result["attribution"] = "火"
    elif attribution == water_is:
        result["attribution"] = "水"
    elif attribution == ice_is:
        result["attribution"] = "氷"
    elif attribution == dragon_is:
        result["attribution"] = "龍"

    if thunder_is.union(fire_is, water_is, ice_is, dragon_is) == set():
        result["attribution"] = ""

    #武器種　短剣、剣、槍、斧、弓、銃、鎌
    if "Sword" in descriptions:
        type = "剣"
    elif "Dagger" in descriptions:
        type =  "短剣"
    elif {"Ax", "Hatchet", "Axe"} & descriptions != set():
        type = "斧"
    elif {"Spear", "Lance"} & descriptions != set():
        type = "槍"
    elif {"Bow", "Archery"} & descriptions != set():
        type = "弓"
    elif "Gun" in descriptions:
        type = "銃"
    else:
        type = random.choice(["短剣", "剣", "斧", "槍", "弓", "銃"])
    result["type"] = type
    #攻撃力
    atk = random.randint(60, 200)*5 #300 ~ 1000
    #属性ボーナス
    if result["attribution"] != "":
        atk += random.randint(20,40)*5
    result["atk"] = atk if atk<= 1000 else 1000

    #レアリティ　N, R, SR, SSR
    if atk <= 600:
        rarity = "N"
    elif atk <= 800:
        rarity = "R"
    elif atk <= 950:
        rarity = "SR"
    else:
        rarity = "SSR"
    result["rarity"] = rarity

    return result
