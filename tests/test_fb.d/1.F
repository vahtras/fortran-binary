      integer, parameter :: n = 3
      double precision x(n)
      x = (/ 1.0D0, 2.0D0, 3.0D0 /)
      open(1, file='fort.1', status='new', form='unformatted')
      write(1) n
      write(1) x
      close(1)
      end
