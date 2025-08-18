# utils/gcs.py
from google.cloud import storage

GCS_BUCKET_NAME = "vibe_marketing"

def upload_to_gcs(image_bytes: bytes, gcs_blob_path: str) -> str:
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(gcs_blob_path)
    blob.upload_from_string(image_bytes, content_type="image/png")
    return f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{gcs_blob_path}"