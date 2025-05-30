import objaverse
import faiss
import json
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# ===== Config =====
INDEX_SIZE = 1000  # Adjust this for more/fewer models
MODEL_NAME = "clip-ViT-B-32"  # CLIP model
INDEX_PATH = "objaverse.index"
UID_MAP_PATH = "uid_map.json"

# ===== Load Objaverse metadata =====
print("📦 Loading Objaverse metadata...")
uids = objaverse.load_uids()
metadata = objaverse.load_metadata()

# ===== Embed text descriptions =====
model = SentenceTransformer(MODEL_NAME)
uid_map = []
texts = []

print(f"🧠 Embedding {INDEX_SIZE} objects using {MODEL_NAME}...")
for uid in tqdm(uids[:INDEX_SIZE]):
    entry = metadata.get(uid, {})
    label = ""

    # Build semantic string for embedding
    if "tags" in entry:
        label += " ".join(entry["tags"])
    if "name" in entry:
        label += f" {entry['name']}"
    if "source" in entry:
        label += f" from {entry['source']}"

    if not label.strip():
        continue  # skip empty entries

    texts.append(label)
    uid_map.append(uid)

embeddings = model.encode(texts, show_progress_bar=True)

# ===== Build FAISS index =====
print("🔧 Building FAISS index...")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# ===== Save artifacts =====
faiss.write_index(index, INDEX_PATH)
with open(UID_MAP_PATH, "w") as f:
    json.dump(uid_map, f)

print(f"✅ Done. Saved index to {INDEX_PATH} and UIDs to {UID_MAP_PATH}")
