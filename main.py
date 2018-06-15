from gui import GuiApp
from imutils.video import VideoStream
import argparse
import time


print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=False).start()

pba = GuiApp(vs)
pba.root.mainloop()
