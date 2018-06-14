from photoboothapp import PhotoBoothApp
from imutils.video import VideoStream
import argparse
import time


print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=False).start()

# start the app
pba = PhotoBoothApp(vs)
pba.root.mainloop()
