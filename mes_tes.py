# from roboflow import Roboflow
# rf = Roboflow(api_key="KF2dRqDKQcUuxUjZHxmo")
# project = rf.workspace("mesupper-frame").project("mes_upper_frame")
# version = project.version(2)
# dataset = version.download("yolov8")
                
from roboflow import Roboflow
rf = Roboflow(api_key="KF2dRqDKQcUuxUjZHxmo")
project = rf.workspace("mesupper-frame").project("mes_lower_frame")
version = project.version(2)
dataset = version.download("yolov8")
                