import sys
import json
from tqdm import tqdm
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

# Add module path
sys.path.insert(0, "/objaverse-xl")
from objaverse import xl

# ===== Config =====
INDEX_SIZE = 1000
MODEL_NAME = "clip-ViT-B-32"
INDEX_PATH = "objaverse.index"
UID_MAP_PATH = "uid_map.json"

# ===== Load metadata =====
print("📦 Loading metadata from Objaverse-XL...")
df = xl.get_annotations(download_dir="/tmp/objaverse-xl")
uids = df["fileIdentifier"].tolist()[:INDEX_SIZE]

# ===== Prepare model & buffers =====
model = SentenceTransformer(MODEL_NAME)
texts, uid_map = [], []

print(f"🧠 Embedding {len(uids)} objects with {MODEL_NAME}...")

for uid in tqdm(uids):
    entry = df[df["fileIdentifier"] == uid].iloc[0]
    raw_meta = entry["metadata"]

    try:
        meta = json.loads(raw_meta) if isinstance(raw_meta, str) else {}
    except json.JSONDecodeError:
        meta = {}

    text = meta.get("name") or meta.get("description") or f"object {uid}"
    texts.append(text)
    uid_map.append(uid)

# ===== Encode and build FAISS index =====
embeddings = model.encode(texts, show_progress_bar=True)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# ===== Save index and map =====
faiss.write_index(index, INDEX_PATH)
with open(UID_MAP_PATH, "w") as f:
    json.dump(uid_map, f)

print(f"✅ Index saved to {INDEX_PATH}")
