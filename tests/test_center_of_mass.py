import numpy as np
from scipy import ndimage
import mahotas.center_of_mass

np.random.seed(2321)
def _mean_out(img, axis):
    if len(img.shape) == 2: return img.mean(1-axis)
    if axis == 0:
        return _mean_out(img.mean(1), 0)
    return _mean_out(img.mean(0), axis - 1)

def slow_center_of_mass(img):
    '''
    Returns the center of mass of img.
    '''
    xs = []
    for axis,si in enumerate(img.shape):
        xs.append(np.mean(_mean_out(img, axis) * np.arange(si)))
    xs = np.array(xs)
    xs /= img.mean()
    return xs


def test_cmp_ndimage():
    R = (255*np.random.rand(128,256)).astype(np.uint16)
    R += np.arange(256)
    m0,m1 = mahotas.center_of_mass(R)
    n0,n1 = ndimage.center_of_mass(R)
    assert np.abs(n0 - m0) < 1.
    assert np.abs(n1 - m1) < 1.

def test_cmp_ndimage3():
    R = (255*np.random.rand(32,128,8,16)).astype(np.uint16)
    R += np.arange(16)
    m = mahotas.center_of_mass(R)
    n = ndimage.center_of_mass(R)
    p = slow_center_of_mass(R)
    assert np.abs(n - m).max() < 1.
    assert np.abs(p - m).max() < 1.

def test_simple():
    R = (255*np.random.rand(128,256)).astype(np.uint16)
    R += np.arange(256)
    m0,m1 = mahotas.center_of_mass(R)

    assert 0 < m0 < 128
    assert 0 < m1 < 256

