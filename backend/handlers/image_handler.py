import json

IMAGE_METADATA_PATH = "data/processed/image_metadata.json"


def load_image_metadata():
    with open(IMAGE_METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return metadata


def image_search(query):

    query_lower = query.lower()
    image_metadata = load_image_metadata()

    scores = []

    for image in image_metadata:

        score = 0
        ocr_text = image.get("ocr_text", "").lower()

        for word in query_lower.split():
            if word in ocr_text:
                score += 1

        scores.append((score, image))

    # sort AFTER loop (important)
    scores.sort(reverse=True, key=lambda x: x[0])

    best_match = scores[0]

    if best_match[0] > 0:
        image_data = best_match[1]

        filename = image_data.get("image_path").split("/")[-1]

        return {
            "image_path": f"images/{filename}",
            "page": image_data.get("page"),
            "score": best_match[0]
        }

    return {
        "error": "No matching image found"
    }