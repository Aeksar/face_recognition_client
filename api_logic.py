import cv2 as cv
from datetime import datetime, timedelta
import requests
import logging
import io
import asyncio
import threading
import multiprocessing
import aiohttp


logger = logging.getLogger(__name__)

class ApiLogic:
    def __init__(self,camera_source: int=0):
        self.camera_source = camera_source

        self.__last_request = datetime.now()
        self.__wait_response = False
        
        self.cap = cv.VideoCapture(self.camera_source)
        

        self.face_cascade = cv.CascadeClassifier("cascade.xml")
        self.url_find = "http://127.0.0.1:8000/faces/find"

    def screenshot(self):
        ok, frame = self.cap.read()
        if ok:
            cv.imwrite("screenshot.jpg", cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            logger.debug("Image saved")
            with open("screenshot.jpg", "rb") as f:
                return f.read()

    def update(self):
        ok, frame = self.cap.read()
        if ok:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            gray_img = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
            faces = self.face_cascade.detectMultiScale(gray_img, 1.1, 4)
            
            for (x, y, w, h) in faces:
                face = (x, y, w, h)
                cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                if not self.__wait_response:
                    try:
                        asyncio.create_task(self.get_face(face))
                    except RuntimeError:
                        asyncio.run(self.get_face(face)) 

                    
        return frame
      
    async def get_face(self, face: tuple[int]):
        if datetime.now() - self.__last_request > timedelta(seconds=3):
            
            logger.debug("send request")
            file = self.screenshot()
            form = aiohttp.FormData()
            form.add_field("file", file)
            self.__wait_response = True
            async with aiohttp.ClientSession() as session:
                async with session.post(url=self.url_find, data=form) as response:
                    logger.debug(f"start proccess face {face}")
                    if response.status == 200:
                        self.__last_request = datetime.now()
                        self.__wait_response = False
                        js = await response.json()
                        print(js)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
        # asyncio.run(self.session.close())