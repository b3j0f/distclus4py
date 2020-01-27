import time
import unittest
import numpy as np

from distclus.streaming import Streaming
from tests.util import sample, rmse


class TestStreaming(unittest.TestCase):

    def setUp(self):
        self.data = sample(10, 2)

    def test_streaming(self):
        algo = Streaming(sigma=.3, seed=1367098323)
        algo.push(self.data[:1])
        algo.play()
        algo.push(self.data[1:])
        time.sleep(.3)
        self.check_online(algo)
        algo.close()
        self.assertGreater(algo.max_distance, 10.)

    def check_online(self, algo):
        centroids, labels = algo.predict_online(self.data)
        self.assertLessEqual(rmse(self.data, centroids, labels), 1.)
