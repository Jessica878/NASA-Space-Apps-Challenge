#!/usr/bin/env python3
"""
Create realistic placeholder tiles for IR, Elevation, and Water Index layers
"""

from PIL import Image, ImageDraw
import os
import math

def create_ir_tile(size=256):
    """Create an infrared-style tile with red/orange colors"""
    img = Image.new('RGB', (size, size), color=(50, 20, 20))
    draw = ImageDraw.Draw(img)
    
    # Add some variation to simulate thermal data
    for x in range(0, size, 4):
        for y in range(0, size, 4):
            # Simulate thermal variations
            temp = math.sin(x * 0.1) * math.cos(y * 0.1) * 50 + 100
            color = (int(temp), int(temp * 0.3), int(temp * 0.1))
            draw.rectangle([x, y, x+3, y+3], fill=color)
    
    return img

def create_elevation_tile(size=256):
    """Create an elevation-style tile with blue/gray colors"""
    img = Image.new('RGB', (size, size), color=(30, 30, 50))
    draw = ImageDraw.Draw(img)
    
    # Add elevation-like patterns
    for x in range(0, size, 2):
        for y in range(0, size, 2):
            # Simulate elevation data
            elevation = math.sin(x * 0.05) * math.cos(y * 0.05) * 30 + 50
            color = (int(elevation), int(elevation), int(elevation + 20))
            draw.rectangle([x, y, x+1, y+1], fill=color)
    
    return img

def create_water_index_tile(size=256):
    """Create a water index-style tile with blue/green colors"""
    img = Image.new('RGB', (size, size), color=(20, 40, 60))
    draw = ImageDraw.Draw(img)
    
    # Add water-like patterns
    for x in range(0, size, 3):
        for y in range(0, size, 3):
            # Simulate water index data
            water = math.sin(x * 0.08) * math.cos(y * 0.08) * 40 + 60
            color = (int(water * 0.3), int(water), int(water + 40))
            draw.rectangle([x, y, x+2, y+2], fill=color)
    
    return img

def create_tile_structure():
    """Create the tile directory structure and generate tiles"""
    
    layers = {
        'layer_ir': create_ir_tile,
        'layer_elev': create_elevation_tile,
        'layer_index': create_water_index_tile
    }
    
    # Create tiles for zoom levels 0-3 (basic coverage)
    for layer_name, tile_func in layers.items():
        print(f"Creating {layer_name} tiles...")
        
        for z in range(4):  # zoom levels 0-3
            max_tiles = 2 ** z
            for x in range(max_tiles):
                for y in range(max_tiles):
                    # Create directory structure
                    tile_dir = f"tiles/{layer_name}/{z}/{x}"
                    os.makedirs(tile_dir, exist_ok=True)
                    
                    # Create tile
                    tile = tile_func()
                    tile_path = f"{tile_dir}/{y}.png"
                    tile.save(tile_path)
        
        print(f"✓ {layer_name} tiles created")

if __name__ == "__main__":
    print("Creating realistic placeholder tiles...")
    create_tile_structure()
    print("Done! Tiles created in tiles/ directory")
