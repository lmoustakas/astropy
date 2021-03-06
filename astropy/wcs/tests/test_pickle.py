import os
import cPickle

import numpy as np
from numpy.testing import assert_array_almost_equal

from ...config import get_data_contents, get_data_fileobj
from ...io import fits
from ...tests.helper import pytest
from ... import wcs


def test_basic():
    wcs1 = wcs.WCS()
    s = cPickle.dumps(wcs1)
    wcs2 = cPickle.loads(s)


def test_dist():
    hdulist = fits.open(get_data_fileobj(os.path.join("data", "dist.fits")))
    wcs1 = wcs.WCS(hdulist[0].header, hdulist)
    assert wcs1.det2im2 is not None
    s = cPickle.dumps(wcs1)
    wcs2 = cPickle.loads(s)

    x = np.random.rand(2 ** 16, wcs1.wcs.naxis)
    world1 = wcs1.all_pix2sky(x, 1)
    world2 = wcs2.all_pix2sky(x, 1)

    assert_array_almost_equal(world1, world2)


def test_sip():
    hdulist = fits.open(get_data_fileobj(os.path.join("data", "sip.fits")),
                        ignore_missing_end=True)
    wcs1 = wcs.WCS(hdulist[0].header)
    assert wcs1.sip is not None
    s = cPickle.dumps(wcs1)
    wcs2 = cPickle.loads(s)

    x = np.random.rand(2 ** 16, wcs1.wcs.naxis)
    world1 = wcs1.all_pix2sky(x, 1)
    world2 = wcs2.all_pix2sky(x, 1)

    assert_array_almost_equal(world1, world2)


def test_sip2():
    hdulist = fits.open(get_data_fileobj(os.path.join("data", "sip2.fits")),
                        ignore_missing_end=True)
    wcs1 = wcs.WCS(hdulist[0].header)
    assert wcs1.sip is not None
    s = cPickle.dumps(wcs1)
    wcs2 = cPickle.loads(s)

    x = np.random.rand(2 ** 16, wcs1.wcs.naxis)
    world1 = wcs1.all_pix2sky(x, 1)
    world2 = wcs2.all_pix2sky(x, 1)

    assert_array_almost_equal(world1, world2)


def test_wcs():
    header = get_data_contents(os.path.join("data", "outside_sky.hdr"))

    wcs1 = wcs.WCS(header)
    s = cPickle.dumps(wcs1)
    wcs2 = cPickle.loads(s)

    x = np.random.rand(2 ** 16, wcs1.wcs.naxis)
    world1 = wcs1.all_pix2sky(x, 1)
    world2 = wcs2.all_pix2sky(x, 1)

    assert_array_almost_equal(world1, world2)


class Sub(wcs.WCS):
    def __init__(self, *args, **kwargs):
        self.foo = 42


def test_subclass():
    wcs = Sub()
    s = cPickle.dumps(wcs)
    wcs2 = cPickle.loads(s)

    assert isinstance(wcs2, Sub)
    assert wcs.foo == 42
    assert wcs2.foo == 42
    assert wcs2.wcs is not None
