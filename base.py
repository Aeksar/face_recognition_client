from abc import ABC, abstractmethod
import requests
import io
import json

class BaseApiHandler(ABC):    
    @abstractmethod
    def get_face(self):
        ...
    
    @abstractmethod 
    def add_face(self):
        ...
      
    @abstractmethod  
    def delete_face(self):
        ...
        
    @abstractmethod
    def update_face(self):
        ...
        
        
class ApiHandler(BaseApiHandler):
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/faces/"
        self.face_url = self.base_url + "find"
        self.add_url = self.base_url + "add"
        self.delete_url = self.base_url + "delete"
        self.update_url = self.base_url + "update"
            
    def add_face(self, name: str, file: bytes):
        data = {"name": name}
        files = {'file': ('chelik.jpg', io.BytesIO(file))}
        return requests.post(url=self.add_url, data=data, files=files)
    
    def get_face(self, file: bytes):
        files = {'file': ('chelik.jpg', io.BytesIO(file))}
        return requests.post(url=self.face_url, files=files)
    
    def update_face(self, id: str, file: bytes, name: str):
        data = {
            "face_id": id,
            "name": name
        }
        files = {'file': ('chelik.jpg', io.BytesIO(file))}
        data = json.dumps(data)
        requests.put(self.update_url, data=data, files=files)
        
    def delete_face(self, id: str):
        data = {"face_id": id}
        return requests.delete(self.delete_url, data=data)
        