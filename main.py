from gui import GuiApp
from imutils.video import VideoStream


print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=False).start()

gui = GuiApp(vs)
gui.root.mainloop()
