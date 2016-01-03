import datetime as dt
import logging
import picamera

class Recorder:
    RECORDING_DIR = "/home/pi/dashcam_v2/recordings/"

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def record(self, filename, duration=5, low_resolution=False):
        recording_path = Recorder.RECORDING_DIR + filename + ".h264"
        self.logger.info(
                "Recording {t}s into {path} (0s => inf)"
                .format(t=duration, path=recording_path)
        )
        with picamera.PiCamera() as camera:
            if low_resolution:
                camera.resolution = (640, 480)
            else:
                camera.resolution = (1296, 976)
            camera.framerate = 24
            # no need for preview unless a monitor is connected
            # camera.start_preview()
            camera.annotate_background = picamera.Color('black')
            camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            camera.start_recording(recording_path)
            start = dt.datetime.now()
            while duration == 0 or (dt.datetime.now() - start).seconds < duration:
                camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                camera.wait_recording(0.1)
            camera.stop_recording()
