import datetime as dt
import logging
import picamera

class Recorder:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def test_log(self):
        self.logger.debug("debug")
        self.logger.info("info")
        self.logger.warning("warning")
        self.logger.error("error")

    def record(self, duration=5):
        with picamera.PiCamera() as camera:
            camera.resolution = (1280, 720)
            camera.framerate = 24
            # no need for preview unless a monitor is connected
            # camera.start_preview()
            camera.annotate_background = picamera.Color('black')
            camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            camera.start_recording('test_recording.h264')
            start = dt.datetime.now()
            while (dt.datetime.now() - start).seconds < duration:
                camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                camera.wait_recording(0.2)
            camera.stop_recording()
