#!/usr/bin/env python3
"""
Create realistic thermal/IR placeholder tiles
"""

from PIL import Image, ImageDraw
import os
import math
import random

def create_thermal_tile(size=256):
    """Create a thermal infrared-style tile"""
    img = Image.new('RGB', (size, size), color=(20, 10, 10))
    draw = ImageDraw.Draw(img)
    
    # Create thermal-like patterns
    for x in range(0, size, 2):
        for y in range(0, size, 2):
            # Simulate thermal variations
            temp = math.sin(x * 0.05) * math.cos(y * 0.05) * 40 + 80
            # Add some randomness for realism
            temp += random.uniform(-10, 10)
            temp = max(0, min(255, temp))
            
            # Thermal color scheme (red/orange for hot, blue for cold)
            if temp > 120:
                color = (int(temp), int(temp * 0.6), int(temp * 0.2))
            elif temp > 80:
                color = (int(temp), int(temp * 0.8), int(temp * 0.4))
            else:
                color = (int(temp * 0.3), int(temp * 0.5), int(temp))
            
            draw.rectangle([x, y, x+1, y+1], fill=color)
    
    return img

def create_water_index_tile(size=256):
    """Create a water index-style tile"""
    img = Image.new('RGB', (size, size), color=(10, 20, 30))
    draw = ImageDraw.Draw(img)
    
    # Create water-like patterns
    for x in range(0, size, 3):
        for y in range(0, size, 3):
            # Simulate water content
            water = math.sin(x * 0.08) * math.cos(y * 0.08) * 30 + 50
            water += random.uniform(-5, 5)
            water = max(0, min(255, water))
            
            # Water index color scheme (blue/green for water)
            color = (int(water * 0.2), int(water * 0.7), int(water))
            
            draw.rectangle([x, y, x+2, y+2], fill=color)
    
    return img

def create_tiles():
    """Create tiles for all layers"""
    
    # Create IR tiles
    print("Creating IR tiles...")
    for z in range(4):
        max_tiles = 2 ** z
        for x in range(max_tiles):
            for y in range(max_tiles):
                tile_dir = f"tiles/layer_ir/{z}/{x}"
                os.makedirs(tile_dir, exist_ok=True)
                tile = create_thermal_tile()
                tile.save(f"{tile_dir}/{y}.png")
    
    # Create water index tiles
    print("Creating water index tiles...")
    for z in range(4):
        max_tiles = 2 ** z
        for x in range(max_tiles):
            for y in range(max_tiles):
                tile_dir = f"tiles/layer_index/{z}/{x}"
                os.makedirs(tile_dir, exist_ok=True)
                tile = create_water_index_tile()
                tile.save(f"{tile_dir}/{y}.png")
    
    print("✓ Tiles created successfully!")

if __name__ == "__main__":
    create_tiles()
