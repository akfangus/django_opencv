import threading

import cv2
from django.contrib.auth.models import User
from django.http import StreamingHttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators import gzip


@gzip.gzip_page
def Home(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass

    return render(request, 'mainapp/main.html')


# 웹캠 클래스 생성
class VideoCamera(object):
    # 초기화 함수
    def __init__(self):
        # 클래스의 video인자를 만들고 opencv의 VideoCapture값을 저장
        self.video = cv2.VideoCapture(0)

        (self.grabbed, self.frame) = self.video.read()

        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        # image에 초기설정한 frame을 가져와서
        image = self.frame
        # jpg형태로 인코딩을 해서 저장한다고함.
        _, jpeg = cv2.imencode('.jpg', image)
        # 그 인코딩된 jpg를 바이트 형식으로 반환해야한다고함.
        # 이래야 프레임별로 라이브 영상을 뽑을수 있다고함.
        return jpeg.tobytes()

    def update(self):
        while True:
            # 루프를 돌려서 지속적으로 frame 값을 업데이트 한다고함.
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
