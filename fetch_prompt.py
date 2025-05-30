import sys
import json
import faiss
import objaverse
from sentence_transformers import SentenceTransformer

def main():
    if len(sys.argv) < 2:
        print("Usage: fetch_prompt.py \"your prompt here\"")
        return

    prompt = sys.argv[1]

    # Load index + map
    index = faiss.read_index("objaverse.index")
    with open("uid_map.json") as f:
        uid_map = json.load(f)

    # Embed prompt
    print(f"🔮 Embedding prompt: {prompt}")
    model = SentenceTransformer("clip-ViT-B-32")
    vec = model.encode([prompt])

    # Search index
    print("🔍 Searching index...")
    _, I = index.search(vec, k=3)
    uids = [uid_map[i] for i in I[0]]

    print("🎯 Matched UIDs:", uids)

    # Download models
    print("⬇️ Downloading models from Objaverse...")
    paths = objaverse.load_objects(uids)
    print("✅ Download complete:")
    for p in paths:
        print(p)

if __name__ == "__main__":
    main()
