import sys
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")  # 384 dimensions
text = sys.argv[1]
embedding = model.encode([text])[0]

print(f"Text: {text}")
print(f"Dimensions: {len(embedding)}")
print(f"Embedding: {embedding}")
