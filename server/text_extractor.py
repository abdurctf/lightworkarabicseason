from google.cloud import videointelligence
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cred/creds.json"
def extract_text_from_video(filename):
    """Extract text annotations from a video in Google Cloud Storage."""
    
    # Initialize the Video Intelligence client
    client = videointelligence.VideoIntelligenceServiceClient()

    # Construct the GCS URI dynamically using the filename
    gcs_uri = f"gs://lightworkarabicseason/{filename}"

    # Configure the request
    request = videointelligence.AnnotateVideoRequest(
        input_uri=gcs_uri,
        features=["TEXT_DETECTION"],
    )

    # Make the API call and get the operation
    operation = client.annotate_video(request=request)
    
    # Wait for the operation to complete
    result = operation.result(timeout=180)
    
    # Retrieve and print the text annotations
    text_annotations = result.annotation_results[0].text_annotations

    for text_annotation in text_annotations:
        print(text_annotation.text)


