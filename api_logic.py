import cv2 as cv
from cv2.typing import MatLike
from datetime import datetime, timedelta
import logging
from concurrent.futures import ThreadPoolExecutor
import requests
from deepface import DeepFace
from numpy import ndarray

from api_base import ApiHandler


logger = logging.getLogger(__name__)

class ApiLogic(ApiHandler):
    def __init__(self,camera_source: int=0):
        super().__init__()
        self.camera_source = camera_source

        self.__last_request = datetime.now()
        
        self.cap = cv.VideoCapture(self.camera_source)
        self.thread_pool = ThreadPoolExecutor(2)
        self.task = None

        self.face_detector = cv.CascadeClassifier("models/face_alt.xml")

    def frame2bytes(self, frame: MatLike):
        return cv.imencode(".jpg", frame)[1].tobytes()

    def screenshot(self):
        logger.debug("Image saved")
        ok, frame = self.cap.read()
        if ok:
            cv.imwrite("screenshot.jpg", frame)
        
    def update(self):
        ok, frame = self.cap.read()
        if ok:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            gray_img = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
            faces = self.face_detector.detectMultiScale(gray_img, scaleFactor=1.2, minNeighbors=3, minSize=(100,100))
            for (x, y, w, h) in faces:
                cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                if datetime.now() - self.__last_request > timedelta(seconds=3) and self.task is None:
                    face_slice = frame[y:y+h, x:x+w]
                    self.task = self.thread_pool.submit(self.get_face, face_slice)   
        return frame
      

    def get_face(self, frame: MatLike):
        try:
            
            logger.debug("process request")
            file = self.frame2bytes(frame)

            
            resp = super().get_face(file)
            logger.debug("send requset")
            self.__last_request = datetime.now()
            
            logger.info(resp.status_code)
            logger.debug(resp.json())
            return resp
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при отправке запроса {e}")
        except Exception as e:
            logger.error(f"Ошибка в get_face {e}")
        finally:
            self.task = None
    
    
        
            
      
    # async def get_face(self, face: tuple[int]):
    #     logger.debug("send request")
    #     if datetime.now() - self.__last_request > timedelta(seconds=3):
            
            
    #         file = self.screenshot()
    #         form = aiohttp.FormData()
    #         form.add_field("file", file)
    #         self.__wait_response = True
    #         async with aiohttp.ClientSession() as session:
    #             async with session.post(url=self.url_find, data=form) as response:
    #                 logger.debug(f"start proccess face {face}")
    #                 if response.status == 200:
    #                     self.__last_request = datetime.now()
    #                     self.__wait_response = False
    #                     js = await response.json()
    #                     print(js)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
        self.thread_pool.shutdown(wait=True)
        # asyncio.run(self.session.close())