from neural_network.neural_for_video.facemask import *


class NeuralNetwork:
    def OpenVideo(self, path):
        return watch_video(path)

    def SaveVideo(self, path_in, path_out):
        save_video(path_in, path_out)
