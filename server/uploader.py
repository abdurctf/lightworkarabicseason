import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from google.cloud import storage  # make sure to install google-cloud-storage package

def clear_directory(dir_path):
    print("Clearing directory...")
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

class Handler(FileSystemEventHandler):
    def process(self, event):
        # Extract file extension
        filename = os.path.basename(event.src_path)

        if event.is_directory:
            print(f"Received directory event - {event.src_path}.")
            return
        elif event.event_type == 'created' and 'mp4' in filename:
            print(f"Received created event for .mp4 file - {event.src_path}.")
            # Wait for 2 seconds before starting the upload
            time.sleep(10)
            blob_name = event.src_path.replace('.temp', '')
            bucket_name = "lightworkarabicseason"  # Replace with your bucket name
            storage_client = storage.Client.from_service_account_json('cred/creds.json')  # Replace with your credentials path
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(os.path.basename(blob_name))

            blob.upload_from_filename(blob_name)

            print(f"File {blob_name} uploaded to {bucket_name}.")
            time.sleep(10)
            # Delete the file from the local directory
            clear_directory('：saved')

            

        else:
            print(f"Ignored non-.mov event - {event.src_path}.")

    def on_created(self, event):
        self.process(event)

import threading

def print_files_in_directory(directory_path):
    while True:
        time.sleep(10)
        with os.scandir(directory_path) as dir_entries:
            files = [entry.name for entry in dir_entries if entry.is_file()]
            print(f"Current list of .mp4 files in {directory_path}: {files}")

if __name__ == "__main__":
    observer = Observer()
    event_handler = Handler()
    directory_path = '：saved'  # Replace with the path of your directory
    observer.schedule(event_handler, path=directory_path, recursive=False)
    observer.start()
    
    # # Start a new thread that prints the list of files every 10 seconds
    # list_files_thread = threading.Thread(target=print_files_in_directory, args=(directory_path,))
    # list_files_thread.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
