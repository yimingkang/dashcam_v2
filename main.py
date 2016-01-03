import datetime
import logging
import os

from recorder import Recorder

class Dashcam:
    LOG_FILE = "/home/pi/dashcam_v2/dashcam.log"
    MINIMUM_FREE_SPACE = 500  # 500 MB

    def __init__(self):
        logging.basicConfig(
           level=logging.INFO,
           filename=Dashcam.LOG_FILE, 
           format="%(asctime)-15s %(name)-12s %(levelname)s %(message)s",
           datefmt='%y-%m-%d %H:%M:%S',
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.recorder = Recorder()

    def start(self):
        self.logger.info("Starting recorder")
        while True:
            free_MB = self.check_disk_usage()
            if free_MB < Dashcam.MINIMUM_FREE_SPACE:
                self.logger.error(
                    "Not enough free space! requried: {r}, have: {h}"
                    .format(r=Dashcam.MINIMUM_FREE_SPACE, h=free_MB)
                )
                while self.check_disk_usage() < Dashcam.MINIMUM_FREE_SPACE:
                    self.remove_oldest_file()
            # record for 30 minutes (on low resolution)
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            self.recorder.record(timestamp, duration=1800, low_resolution=True)
    
    def remove_oldest_file(self, extension=".h264"):
        try:
            oldest = min(
                (
                    os.path.join(dirname, filename)
                    for dirname, _, filenames in os.walk(Recorder.RECORDING_DIR)
                    for filename in filenames if filename.endswith(extension)
                ),
                key=lambda fn: os.stat(fn).st_mtime,
            )
        except ValueError:
            self.logger.error(
                "Could not find any file in {d} that ends with {ext}"
                .format(d=Recorder.RECORDING_DIR, ext=extension)
            )
            return
        self.logger.warning("Removing {f}".format(f=oldest))
        os.remove(oldest)

    def check_disk_usage(self, path="/"):
        """Return disk usage statistics about the given path.
        """
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        self.logger.debug(
            "Disk stats: free: {f}B, used: {u}B, total: {t}B"
            .format(f=free, u=used, t=total)
        )
        # return free space in MB
        return free / 1000000

if __name__ == "__main__":
    cam = Dashcam()
    cam.start()
