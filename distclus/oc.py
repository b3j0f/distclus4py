import random
import weakref

from . import bind
from .ffi import lib


class OnlineClust:
    """
    Base class for algorithm implementation using a native library
    """

    def __init__(
        self, space='real', par=True, init='kmeanspp', seed=None, *args
    ):
        space = bind.space(space)
        init = bind.initializer(init)
        seed = random.randint(0, 2 ** 63) if seed is None else seed
        par = 1 if par else 0
        descr = getattr(lib, self.__class__.__name__.upper())
        self.descr = descr(space, par, init, seed, *args)

    def __finalize(self):
        weakref.finalize(self, lambda: lib.Free(self.descr))

    def fit(self, data):
        """Execute sequentially push, run and close methods.

        :param data: data to process
        """
        self.push(data)
        self.run()
        self.close()

    def push(self, data):
        """Push input data to process.

        :param data: data to push in the algorithme.
        """
        arr, l1, l2 = bind.to_c_2d_array(data)
        lib.Push(self.descr, arr, l1, l2)

    def __radd__(self, data):
        return self.push(data)

    def run(self, rasync=False):
        """Execute (a-)synchronously the alogrithm

        :param bool rasync: Asynchronous execution if True. Default is False.
        """
        lib.Run(self.descr, 1 if rasync else 0)

    def __call__(self, rasync=False):
        return self.run(rasync)

    def close(self):
        """Close algorithm execution."""
        lib.Close(self.descr)

    def predict(self, data, push=False):
        """Predict """
        arr, l1, l2 = bind.to_c_2d_array(data)
        result = lib.Predict(self.descr, arr, l1, l2, 1 if push else 0)
        return bind.to_managed_1d_array(result)

    @property
    def centroids(self):
        """Get centroids."""
        result = lib.RealCentroids(self.descr)
        return bind.to_managed_2d_array(result)

    def __len__(self):
        return len(this.centroids)

    def __getitem__(self, key):
        return this.centroids[key]

    def __iter__(self):
        return iter(this.centroids)

    def __contains__(self, data):
        return data in this.centroids