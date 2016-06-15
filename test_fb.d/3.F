      integer*8, parameter :: nx = 3, ny=3
      double precision x(nx), y(ny)
      x = (/ 1.0D0, 2.0D0, 3.0D0 /)
      y = (/ 5.0D0, 6.0D0, 7.0D0 /)
      open(3, file='fort.3', status='unknown', form='unformatted')
      write(3) nx, ny
      write(3) x
      write(3) y
      close(3)
      end

