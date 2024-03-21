import array
import os
import pathlib
from unittest import mock

import numpy as np
import pytest

from fortran_binary import FortranBinary, main


class TestFortranBinary:
    def setup_method(self):
        self.tdir = pathlib.Path(__file__).parent / "test_fb.d"

    def test_1(self):
        """Read int, float

          integer, parameter :: n = 3
          double precision x(n)
          x = (/ 1.0D0, 2.0D0, 3.0D0 /)
          open(1, file='fort.1', status='new', form='unformatted')
          write(1) n
          write(1) x
          close(1)
          end
        """
        ffile = self.tdir / "fort.1"
        fb = FortranBinary(ffile)
        # first record is int 3
        next(fb)
        n = fb.readbuf(1, "i")[0]
        assert n == 3

        # first record is float 1. 2. 3.
        next(fb)
        xref = (1.0, 2.0, 3.0)
        x = fb.readbuf(n, "d")
        np.testing.assert_allclose(x, xref)
        fb.close()

    def test_1_cm(self):
        """Case 1 with context manager"""
        ffile = self.tdir / "fort.1"
        with FortranBinary(ffile) as fb:
            n = next(fb).read(1, "i")[0]
            x = next(fb).read(n, "d")
        np.testing.assert_allclose(x, (1.0, 2.0, 3.0))

    def test_1_as_float(self):
        ffile = self.tdir / "fort.1"
        for record in FortranBinary(ffile):
            pass

        assert record.as_array() == array.array('d', (1.0, 2.0, 3.0))

    def test_2(self):
        """Find and read label

          character*5 lab
          integer n
          lab = 'LABEL'
          n = 0
          open(1, file='fort.2', status='new', form='unformatted')
          write(1) n
          write(1) lab
          close(1)
          end
        """
        ffile = self.tdir / "fort.2"
        fb = FortranBinary(ffile)
        rec = fb.find(b"LABEL")

        assert rec.data == b"LABEL"
        fb.close()

    def test_2_cm(self):
        """
        Case 2 with context manager
        """
        ffile = self.tdir / "fort.2"
        with FortranBinary(ffile) as fb:
            rec = fb.find(b"LABEL")
        assert rec.data == b"LABEL"

    def test_2_str(self):
        """
        Case 2 with str method
        """
        ffile = self.tdir / "fort.2"
        with FortranBinary(ffile) as fb:
            rec = fb.find(b"LABEL")
        assert rec.data.decode("utf-8") == "LABEL"

    def test_2b(self):
        """Handle label not found

          character*5 lab
          integer n
          lab = 'LABEL'
          n = 0
          open(1, file='fort.2', status='new', form='unformatted')
          write(1) n
          write(1) lab
          close(1)
          end
        """
        ffile = self.tdir / "fort.2"
        fb = FortranBinary(ffile)
        rec = fb.find(b"NOLABEL")
        fb.close()

        assert rec is None

    def test_2b_cm(self):
        """
        Case 2b with context manager
        """
        ffile = self.tdir / "fort.2"
        with FortranBinary(ffile) as fb:
            rec = fb.find(b"NOLABEL")
        assert rec is None

    def test_3a(self):
        """Integer*8 dimensions

          integer*8, parameter :: nx = 3, ny=3
          double precision x(nx), y(ny)
          x = (/ 1.0D0, 2.0D0, 3.0D0 /)
          y = (/ 5.0D0, 6.0D0, 7.0D0 /)
          open(3, file='fort.3', status='new', form='unformatted')
          write(3) nx, ny
          write(3) x
          write(3) y
          close(3)
          end

        """
        ffile = self.tdir / "fort.3"
        fb = FortranBinary(ffile)
        # first record is int 3, 3
        nx, ny = fb.next().read("q", 2)
        np.testing.assert_allclose((nx, ny), (3, 3))
        fb.close()

    def test_3a_cm(self):
        """Case 3a with context manager """
        ffile = self.tdir / "fort.3"
        with FortranBinary(ffile) as fb:
            nx, ny = fb.next().read("q", 2)
        np.testing.assert_allclose((nx, ny), (3, 3))

    def test_3b(self):
        """Read vecs

          integer, parameter :: nx = 3, ny=3
          double precision x(nx), y(ny)
          x = (/ 1.0D0, 2.0D0, 3.0D0 /)
          y = (/ 5.0D0, 6.0D0, 7.0D0 /)
          open(3, file='fort.3', status='new', form='unformatted')
          write(3) nx, ny
          write(3) x
          write(3) y
          close(3)
          end

        """
        ffile = self.tdir / "fort.3"
        fb = FortranBinary(ffile)
        # first record is int 3
        fb.next()
        x = []
        for rec in fb:
            x += list(fb.readbuf(3, "d"))
        xref = (1.0, 2.0, 3.0, 5.0, 6.0, 7.0)
        np.testing.assert_allclose(x, xref)
        fb.close()

    def test_3b_cm(self):
        """Case 3b with context manager"""
        ffile = self.tdir / "fort.3"
        with FortranBinary(ffile) as fb:
            fb.next()
            x = []
            for rec in fb:
                x += list(fb.readbuf(3, "d"))
        xref = (1.0, 2.0, 3.0, 5.0, 6.0, 7.0)
        np.testing.assert_allclose(x, xref)

    def test_4(self):
        """Read string

        character*3 x
        x = 'ABC'
        open(4, file='fort.4', status='new', form='unformatted')
        write(4) x
        close(4)
        end
        """
        ffile = self.tdir / "fort.4"
        fb = FortranBinary(ffile)
        rec = fb.find("ABC")
        assert b"ABC" in rec

    def test_4_cm(self):
        """Case 4 with context manager"""
        ffile = self.tdir / "fort.4"
        with FortranBinary(ffile) as fb:
            rec = fb.find("ABC")
        assert b"ABC" in rec

    def test_4b(self):
        """Read string"""
        ffile = self.tdir / "fort.4"
        fb = FortranBinary(ffile)
        rec = fb.find(b"ABC")
        assert b"ABC" in rec
        fb.close()

    def test_4b_cm(self):
        """Read string with context manager"""
        ffile = self.tdir / "fort.4"
        with FortranBinary(ffile) as fb:
            rec = fb.find(b"ABC")
        assert b"ABC" in rec

    def test_4c(self):
        """Read string"""
        ffile = self.tdir / "fort.4"
        fb = FortranBinary(ffile)
        with pytest.raises(ValueError):
            fb.find(1.0)
        fb.close()

    def test_4c_cm(self):
        """Read string with context manager"""
        ffile = self.tdir / "fort.4"
        with FortranBinary(ffile) as fb:
            with pytest.raises(ValueError):
                fb.find(1.0)

    def test_4d(self):
        """Read string"""
        ffile = self.tdir / "fort.4"
        fb = FortranBinary(ffile)
        rec = next(fb)
        assert len(rec) == 3
        fb.close()

    def test_4d_warn(self):
        """Read string"""
        ffile = self.tdir / "fort.4"
        fb = FortranBinary(ffile)
        next(fb)
        with pytest.deprecated_call():
            fb.reclen
        fb.close()

    def test_4d_cm(self):
        """Read string with context manager"""
        ffile = self.tdir / "fort.4"
        with FortranBinary(ffile) as fb:
            rec = next(fb)
        assert len(rec) == 3

    def test_count_records_and_lengths(self):
        ffile = self.tdir / "fort.3"
        fb = FortranBinary(ffile)
        assert fb.record_byte_lengths() == (16, 24, 24)
        fb.close()

    def test_count_records_and_lengths_cm(self):
        ffile = self.tdir / "fort.3"
        with FortranBinary(ffile) as fb:
            assert fb.record_byte_lengths() == (16, 24, 24)

    def test_as_script(self):
        import sys

        sys.argv[1:] = [f'{self.tdir / "fort.3"}', "--records"]
        main()
        if hasattr(sys.stdout, "getvalue"):
            print_output = sys.stdout.getvalue().strip()
            assert print_output == "(16, 24, 24)"

    def test_open_non_existing(self):
        ffile = self.tdir / "nofile"
        with pytest.raises(IOError):
            FortranBinary(ffile)

    @mock.patch("fortran_binary.open")
    def test_open_new(self, mock_open):
        ffile = self.tdir / "newfile"
        FortranBinary(ffile, "wb")
        mock_open.assert_called_once_with(ffile, "wb")
