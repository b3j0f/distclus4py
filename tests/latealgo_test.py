import time
import unittest
from threading import Thread

import numpy as np

from distclus import MCMC
from distclus.latealgo import LateAlgo
from tests.util import rmse, sample


class TestLateInit(unittest.TestCase):

    def setUp(self):
        self.data = sample(10, 2)

    def test_build(self):
        late = LateMCMC(init_k=2, mcmc_iter=20, seed=166348259467)
        self.assertIsNone(late._algo)

    def test_push(self):
        late = LateMCMC(init_k=2, mcmc_iter=20, seed=166348259467)
        late.push(self.data[0:1])
        self.assertIsNone(late._algo)
        self.assertEqual(1, len(late._buffer))
        late.push(self.data[1:2])
        self.assertIsNotNone(late._algo)
        self.assertEqual(0, len(late._buffer))
        algo = late._algo
        late.push(self.data[2:3])
        self.assertIs(algo, late._algo)

    def test_run_sync(self):
        late = LateMCMC(init_k=2, mcmc_iter=20, seed=166348259467, dim=12)
        self.assertRaises(ValueError, late.batch)
        late.push(self.data)
        late.batch()

    def test_run_async(self):
        late = LateMCMC(init_k=2, mcmc_iter=20, seed=166348259467)
        late.play()
        self.assertIsNone(late._algo)
        late.push(self.data)
        late.stop()

    def test_centroids(self):
        late = LateMCMC(init_k=2, mcmc_iter=20, seed=166348259467)
        self.assertRaises(ValueError, lambda: late.centroids)
        late.play()
        late.push(self.data)
        time.sleep(.3)
        self.assertGreaterEqual(len(late.centroids), 2)
        late.stop()

    def test_predict_batch(self):
        late = LateMCMC(init_k=2, mcmc_iter=20, seed=166348259467)
        late.push(self.data)
        late.batch()
        self.check_static(late)

    def test_predict(self):
        late = LateMCMC(init_k=2, mcmc_iter=20, seed=166348259467)
        late.play()
        self.assertRaises(ValueError, late.predict, self.data)
        late.push(self.data)
        time.sleep(.3)
        self.check_online(late)
        late.stop()

    def test_context(self):
        with LateMCMC(init_k=2, mcmc_iter=20, seed=166348259467) as late:
            late.push(self.data)
            time.sleep(.3)
            self.check_online(late)

    def test_push_parallel(self):
        late = LateMCMC(init_k=2, mcmc_iter=20, seed=166348259467)
        late.play()
        threads = []
        for d in self.data:
            t = Thread(target=late.push, args=(np.array([d]),))
            threads.append(t)
        for thread in threads:
            thread.start()
        for t in threads:
            t.join()
        late.wait()
        late.stop()
        self.check_static(late)

    def check_static(self, late):
        centroids = late.centroids
        _, labels = late.predict(self.data)
        self.assertLessEqual(rmse(self.data, centroids, labels), 1.)

    def check_online(self, late):
        centroids, labels = late.predict(self.data)
        self.assertLessEqual(rmse(self.data, centroids, labels), 1.)


def LateMCMC(init_k, **kwargs):
    def builder(data):
        if len(data) >= init_k:
            kw = {**kwargs, 'init_k': init_k, 'dim': len(data[0])}
            return MCMC(**kw, data=data)

    return LateAlgo(builder)
