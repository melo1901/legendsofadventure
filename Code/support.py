from csv import reader
from os import walk
import pygame


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def create_graphics_dict():
    resources = [
        "desert_ [resources].png",
        "forest_ [resources].png",
        "swamp_ [resources].png",
        "taiga_ [resources].png",
        "tundra_ [resources].png",
    ]
    resource_tiles = {}
    tile_width, tile_height = 16, 16

    for resource in resources:
        resource_type = resource.split("_")[0]

        tileset = pygame.image.load(f"graphics/elements/{resource}").convert_alpha()

        resource_tiles[resource_type + "_elements"] = []

        for y in range(0, tileset.get_height(), tile_height):
            for x in range(0, tileset.get_width(), tile_width):
                tile = tileset.subsurface(pygame.Rect(x, y, tile_width, tile_height))
                resource_tiles[resource_type + "_elements"].append(tile)

    return resource_tiles


import_folder("level/level_data/map_elements.csv")
