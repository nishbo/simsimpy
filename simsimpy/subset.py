from math import floor, ceil
# from __future__ import print_function


class SubsetStorage(object):
    """Stores portion of input data, to save space.

    Does an injection of data of input size into a list of buf size. Supports
    __getitem__, __setitem__, __len__, __contains__, __delitem__, __str__
    magic, append.

    Attributes:
    buf_size: size of inner buffer of storage.

    Private attributes:
    _i: inner position in preallocated buffer.
    _j: current position in data for receiving.
    _dif: relative movement of _i when _j increases.
    _buf: buffer.

    """
    def __init__(self, buf_size, input_size):
        self.buf_size = buf_size
        self._dif = buf_size / (input_size + 1)
        self._i = 0
        self._j = 0

        self._buf = [None]*buf_size

    def append(self, d):
        self._i = int(floor(self._j * self._dif))
        if self._i >= self.buf_size:
            self._i -= 1
            raise BufferError('Stack is full.')

        self._buf[self._i] = d
        self._j += 1

    def __len__(self):
        return self._i + 1

    def __getitem__(self, sl):
        if isinstance(sl, slice):
            start, stop, step = sl.indices(len(self))
            sl = slice(start, stop, step)
        else:
            if sl > len(self):
                raise IndexError
            if sl < 0:
                sl += len(self)

        return self._buf[sl]

    def __setitem__(self, key, value):
        if key > len(self):
            raise IndexError
        if key < 0:
            key += len(self)

        self._buf[key] = value

    def __iter__(self):
        return self._buf[:len(self)]

    def __contains__(self, item):
        return item in self._buf[:len(self)]

    def __delitem__(self, key):
        if key > len(self):
            raise IndexError
        if key < 0:
            key += len(self)

        # print self._buf
        del self._buf[key]
        # print self._buf

        # print self._j, int(floor(self._j * self._dif)),
        self._j -= int(ceil(1./self._dif))
        # print 1./self._dif, self._j, int(floor(self._j * self._dif))
        self._buf.append(None)
        self._i = int(floor(self._j * self._dif))

    def __str__(self):
        return str(self._buf[:len(self)])


def test():
    a = SubsetStorage(5, 13)

    for i in range(13):
        a.append(i)
        print(i, len(a), a[-1], a)

    print(a)
    a[2] = -11
    print(a[1:3], a)
    if -11 in a:
        print('-11 is in a')
    if not 110 in a:
        print('but not 110')

    print('\n', a)
    del a[2]
    print(a)
    a.append(78)
    print(a)
    print(a[:], a[-1])


if __name__ == '__main__':
    test()
