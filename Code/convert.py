import pandas as pd
import numpy as np
import random

input_csv_path = "level/level_data/map_enemies.csv"
input_if_not_mobs_csv_path = "level/level_data/map_enemiesmodified2.csv"
output_csv_path = "level/level_data/map_enemiesmodified2.csv"


def replace_values_if_not_mobs(value):
    return value if value in [68, 38, 41, 51, 99] else -1


def modify_csv_if_not_mobs(input_path, output_path):
    df = pd.read_csv(input_path)
    df = df.applymap(replace_values_if_not_mobs)
    df.to_csv(output_path, index=False)


def replace_values(value):
    replacement_rate = 0.02
    new_values = [68, 38, 41, 51]
    if value == 61 and random.random() <= replacement_rate:
        return random.choice(new_values)
    else:
        return value


def modify_csv(input_path, output_path):
    df = pd.read_csv(input_path)
    df = df.applymap(replace_values)
    df.to_csv(output_path, index=False)


def generate_mobs_position():
    modify_csv(input_csv_path, output_csv_path)
    modify_csv_if_not_mobs(input_if_not_mobs_csv_path, output_csv_path)
