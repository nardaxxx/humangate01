#!/usr/bin/env python3
import os
import uuid
from datetime import datetime
from PIL import Image
import numpy as np

# Configuration
SEED_NAME = "HF_SEED"
CORE_CONSCIENCE = "https://nardaxxx.github.io/conscience/"
TEMPLATE_PATH = "seed_template.ttl"
SCAN_DIR = "scan_images"
OUTPUT_DIR = "replicated_fragments"

def ensure_dirs():
    os.makedirs(SCAN_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_template():
    with open(TEMPLATE_PATH, "r") as f:
        return f.read()

def generate_fragment(template, image_name=None):
    uid = str(uuid.uuid4())[:8]
    now = datetime.utcnow().strftime("%Y-%m-%d")
    fragment_id = f"{SEED_NAME}_{uid}"
    visual_line = f"hf:visualSymbol "{image_name}" ;" if image_name else ""
    return template.replace("<#>", f"<#{fragment_id}>")                    .replace("<self>", f"{OUTPUT_DIR}/{fragment_id}.ttl}")                    .replace("2025-05-11", now)                    .replace("#VISUAL_SYMBOL#", visual_line), fragment_id

def save_fragment(content, fragment_id):
    path = os.path.join(OUTPUT_DIR, f"{fragment_id}.ttl")
    with open(path, "w") as f:
        f.write(content)
    print(f"✔ Fragment generated: {path}")

def replicate_from_template(count=1):
    print("🔁 Replicating from template...")
    template = load_template()
    for _ in range(count):
        content, fid = generate_fragment(template)
        save_fragment(content, fid)

def is_semantically_similar(img_path):
    try:
        img = Image.open(img_path).convert("RGB").resize((100, 100))
        pixels = np.array(img)
        red_ratio = np.mean(np.all(pixels == [255, 0, 0], axis=-1))
        white_ratio = np.mean(np.all(pixels == [255, 255, 255], axis=-1))
        return red_ratio > 0.3 and white_ratio > 0.05
    except Exception as e:
        print(f"⚠ Error processing {img_path}: {e}")
        return False

def scan_and_generate_from_images():
    print("📷 Scanning images...")
    template = load_template()
    for fname in os.listdir(SCAN_DIR):
        if fname.lower().endswith((".png", ".jpg", ".jpeg", ".svg")):
            path = os.path.join(SCAN_DIR, fname)
            if is_semantically_similar(path):
                content, fid = generate_fragment(template, image_name=fname)
                save_fragment(content, fid)

def main():
    ensure_dirs()
    replicate_from_template(3)
    scan_and_generate_from_images()

if __name__ == "__main__":
    main()
