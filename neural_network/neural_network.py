from neural_network.neural_for_webcamera.main import *
from neural_network.neural_for_video.facemask import *


class NeuralNetwork:
    def OpenFromWebCamera(self):
        main()

    def OpenVideo(self, name_city, path):
        if path != "":
            detect_by_video(name_city, path)
