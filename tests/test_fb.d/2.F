      character*5 lab
      integer n
      lab = 'LABEL'
      open(1, file='fort.2', status='new', form='unformatted')
      write(1) 0
      write(1) lab
      close(1)
      end
