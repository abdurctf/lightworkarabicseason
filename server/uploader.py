import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google.cloud import storage  
from text_extractor import extract_text_from_video


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cred/creds.json"

def clear_directory(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

class Handler(FileSystemEventHandler):
    def process(self, event):

        filename = os.path.basename(event.src_path)

        if event.is_directory:
            print(f"Received directory event - {event.src_path}.")
            return
        
        elif event.event_type == 'created' and 'mp4' in filename:
            print(f"Received created event for .mp4 file - {filename}.")
        
            time.sleep(5)

            blob_name = event.src_path.replace('.temp', '')
            bucket_name = "lightworkarabicseason"  
            storage_client = storage.Client.from_service_account_json('cred/creds.json')  
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(os.path.basename(blob_name))
            

            blob.upload_from_filename(blob_name)
            public_url = blob.public_url

            print(f"File {blob_name} uploaded to {bucket_name} at {public_url}.")

            time.sleep(3)

            # call the text extractor
            uploadedFileName= blob_name.split('\\')[-1]
            print("Extracting text from video", uploadedFileName)
            
            extract_text_from_video(uploadedFileName)
            print("Text extracted from video.")

            time.sleep(2)
            # Delete the file from the local directory
            print("Clearing directory...")
            clear_directory('：saved')
    

        else:
            print(f"Ignored non-.mov event.")

    def on_created(self, event):
        self.process(event)


if __name__ == "__main__":

    observer = Observer()
    event_handler = Handler()
    directory_path = '：saved' 
    observer.schedule(event_handler, path=directory_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
