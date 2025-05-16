from abc import ABC, abstractmethod
import requests
import io
import json
from datetime import datetime
from logs import logging


logger = logging.getLogger(__name__)

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
        
    @abstractmethod
    def get_log(self):
        ...
        
        
class ApiHandler(BaseApiHandler):
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/"
        self.face_url = self.base_url + "faces/find"
        self.add_url = self.base_url + "faces/add"
        self.delete_url = self.base_url + "faces/delete"
        self.update_url = self.base_url + "faces/update"
        self.log_url = self.base_url + "log"
        
            
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
    
    def get_log(
        self, 
        start: datetime=None, 
        end: datetime=None, 
        name: str=None
    ):
        query_param =""
        if start:
            query_param += f"start={start}&"
        if end:
            query_param = f"end={end}&"
        if name:
            query_param = f"name={name}&"
        request_url = f"{self.log_url}?{query_param}"
        logger.debug(f"get_log send request with data: {request_url}")
        response = requests.get(request_url).json()
        logger.debug(f"take logs: {response}")
        return response