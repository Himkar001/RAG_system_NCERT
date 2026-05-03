import re
import json
from pathlib import Path


# -----------------------------
# Text Cleaning
# -----------------------------
def clean_text(text):

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"[^a-zA-Z0-9\s=+\-*/().]", "", text)

    return text.strip()


# -----------------------------
# Query Preprocessing
# -----------------------------
def preprocess_query(query):

    query = clean_text(query)

    return query


# -----------------------------
# Safe JSON Loader
# -----------------------------
def load_json(file_path):

    with open(file_path, "r", encoding="utf-8") as f:

        data = json.load(f)

    return data


# -----------------------------
# Save JSON
# -----------------------------
def save_json(data, file_path):

    with open(file_path, "w", encoding="utf-8") as f:

        json.dump(data, f, indent=4)


# -----------------------------
# Ensure Folder Exists
# -----------------------------
def ensure_directory(path):

    Path(path).mkdir(parents=True, exist_ok=True)


# -----------------------------
# Remove Duplicate Results
# -----------------------------
def deduplicate_results(results):

    unique = {}

    for item in results:

        key = item.get("text", "")[:150]

        if key not in unique:

            unique[key] = item

    return list(unique.values())