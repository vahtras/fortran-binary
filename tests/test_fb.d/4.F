
      character*3 x
      x = 'ABC'
      open(4, file='fort.4', status='new', form='unformatted')
      write(4) x
      close(4)
      end
