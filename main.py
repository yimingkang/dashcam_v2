import logging

from recorder import Recorder

class Dashcam:
    LOG_FILE = "./dashcam.log"

    def __init__(self):
        logging.basicConfig(
           level=logging.DEBUG,
           filename=Dashcam.LOG_FILE, 
           format="%(asctime)-15s %(name)-12s %(levelname)s %(message)s",
           datefmt='%y-%m-%d %H:%M:%S',
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.recorder = Recorder()

    def start(self):
        self.logger.debug("debug")
        self.logger.info("info")
        self.logger.warning("warning")
        self.logger.error("error")
        self.recorder.test_log()

if __name__ == "__main__":
    cam = Dashcam()
    cam.start()



