import sys
sys.path.insert(0, "/objaverse-xl")

import pandas as pd
from objaverse import xl
import json

print("📦 Downloading annotations and inspecting metadata...")

df = xl.get_annotations(download_dir="/tmp/objaverse-xl")

print("🧾 Columns:")
print(df.columns.tolist())

print("\n🔍 Metadata (first row):")
meta = df.iloc[0]["metadata"]
print(json.dumps(meta, indent=2) if isinstance(meta, dict) else meta)

print(f"\n✅ metadata type: {type(meta)}")
