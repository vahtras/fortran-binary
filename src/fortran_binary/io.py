import struct
import warnings
import array


class FortranBinary:
    """
    Class for binary files compatible with Fortran Unformatted I/O
    """

    pad = 4

    def __init__(self, name, mode="rb"):
        self.name = name
        self.file = open(name, mode)
        self.rec = None

    @property
    def reclen(self):
        warnings.warn("FortranBinary.reclen deprecated", DeprecationWarning)
        return self.rec.reclen

    def __iter__(self):
        return self

    def __next__(self):
        """
        Read a Fortran record
        """
        head = self.file.read(self.pad)
        if head:
            record_size = struct.unpack("i", head)[0]
            record_data = self.file.read(record_size)
            tail = self.file.read(self.pad)
            assert head == tail
            self.rec = Rec(record_data)
            return self.rec
        else:
            raise StopIteration

    def find(self, label):
        """
        Find string label in file
        """
        if isinstance(label, str):
            try:
                blabel = bytes(label, "utf-8")
            except TypeError:
                blabel = label
        elif isinstance(label, bytes):
            blabel = label
        else:
            raise ValueError

        for rec in self:
            if blabel in rec:
                return rec

    def record_byte_lengths(self):
        """
        Return record byte lengths in file as tuple
        """

        reclengths = [record.reclen for record in self]
        return tuple(reclengths)

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args):
        self.file.close()

    def __getattr__(self, attr):
        """
        Delegate unknown attributes to file member
        """
        return getattr(self.file, attr)


class Rec:
    """
    Representation of a single Fortran record
    """

    def __init__(self, data):
        self.data = data
        self.loc = 0

    def __str__(self):
        return str(self.data)

    def __contains__(self, obj):
        return obj in self.data

    def __len__(self):
        return len(self.data)

    @property
    def reclen(self):
        return len(self.data)

    def read(self, num, fmt):
        """
        Read data from current record
        """
        start, stop = self.loc, self.loc + struct.calcsize(fmt * num)
        vec = struct.unpack(fmt * num, self.data[start:stop])
        self.loc = stop
        return array.array(fmt, vec)
