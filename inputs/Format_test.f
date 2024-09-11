
      IMPLICIT NONE

      REAL ::  TESTER(3) 
      INTEGER :: I 

      OPEN(UNIT = 20, FILE ='04272016_Temperatures',
     & STATUS ='old')


      DO I=1,3
       READ(20,'(3(F6.2,2x))') TESTER 
      ENDDO

      print*,TESTER

      STOP 
      END 
