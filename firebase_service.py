import sys
import json
import cv2
import firebase_admin
import numpy as np
from firebase_admin import storage, auth, credentials
class Firebase:
    def __init__(self):
        cred = credentials.Certificate(f"{sys.path[0]}//firebase_config//certificate.json")
        with open(f"{sys.path[0]}//firebase_config//config.json") as config:
            config = json.loads(config.read())
        self.firebase_service = firebase_admin.initialize_app(cred, options = config)
        self.storage = storage.bucket(app= self.firebase_service)

    
    def upload(self, filestream : bytes, filename : str, public : bool = False):
        blob = self.storage.blob(f"295c7c8dcfe32fec113bd6698042976f90784048/{filename}")
        if public:
            blob.upload_from_string(filestream, content_type="image/jpeg")
            blob.make_public()
            return blob.public_url
        blob.upload_from_string(filestream)
        return f"295c7c8dcfe32fec113bd6698042976f90784048/{filename}"
        
    
    def download(self, file):        
        blob = self.storage.blob(file)
        nparr = np.frombuffer(blob.download_as_bytes(), np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR )

