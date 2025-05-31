import sys, os, shutil
import json, faiss, objaverse.xl as oxl
from sentence_transformers import SentenceTransformer

EXPORT_DIR = "/export"

def main():
    if len(sys.argv) < 2:
        print("Usage: fetch_prompt.py \"your prompt\"")
        return

    prompt = sys.argv[1]

    # Load index + UID map
    index = faiss.read_index("objaverse.index")
    with open("uid_map.json") as f:
        uid_map = json.load(f)

    # CLIP embed
    model = SentenceTransformer("clip-ViT-B-32")
    vec = model.encode([prompt])
    _, I = index.search(vec, k=3)
    uids = [uid_map[i] for i in I[0]]

    print("🎯 Matching UIDs:", uids)

    # Download 3D files using Objaverse-XL
    print("📥 Downloading 3D objects...")
    downloaded_paths = oxl.load_objects(uids)

    print(f"💾 Dumping to {EXPORT_DIR}")
    os.makedirs(EXPORT_DIR, exist_ok=True)

    for uid, path in downloaded_paths.items():
        dst_path = os.path.join(EXPORT_DIR, uid)
        shutil.copytree(path, dst_path, dirs_exist_ok=True)
        print("✅ Copied:", dst_path)

if __name__ == "__main__":
    main()
