    
C     **************************************************
C     *  report                                        *
C     **************************************************

C     WRITTEN BY Peter Adams, November 1999

C     Used by box model for testing aerosol microphysics code.  This
C     routine outputs the simulation status.

C-----INPUTS------------------------------------------------------------

C-----OUTPUTS-----------------------------------------------------------

      SUBROUTINE report(time,HOM2,CS2,kappa_avg2,SAPRCGC2,Dbk)

      IMPLICIT NONE

C-----INCLUDE FILES-----------------------------------------------------

CAliA      include 'BB192SM9.COM'
CAliA      include 'BT263box.COM'
      include 'sizecode.COM'
      include 'modlspc.h'  
      include 'common.inc'
      include 'gaskin.h' 

C-----ARGUMENT DECLARATIONS---------------------------------------------

      double precision time
      DOUBLE PRECISION HOM2
      DOUBLE PRECISION CS2
      DOUBLE PRECISION kappa_avg2(ibins)
      DOUBLE PRECISION Dbk         ! particle-phase diffusion coefficient [m2/s]
      REAL :: SAPRCGC2(NACT)

C-----VARIABLE DECLARATIONS---------------------------------------------

      integer n,k,j

C      character*120 diagname
C      CHARACTER*120 NCONCFILE, GCONCFILE, AECONCFILE
      CHARACTER*120 NCONCFILE, GCONCFILE, AECONCFILE, SPECFILE
      CHARACTER*120 SAPRCGCFILE, OH_FILE, FN_FILE, CS_FILE, Kappa_FILE
      CHARACTER*120 HOM_file!,VOC_FILE,FLOW_FILE,INJECT_FILE
      character*120 WALL_GC, WALL_MK, WALL_NK, O3_FILE, DBK_FILE

!       common /FLNAMES/ SAPRCGCFILE, 
!      &                 NCONCFILE, GCONCFILE, AECONCFILE,
!      &                 SPECFILE,  OH_FILE, FN_FILE, CS_FILE,
!      &                 Kappa_FILE, O3_FILE,
!      &                 WALL_GC, WALL_MK, WALL_NK, HOM_FILE,
!      &                 DBK_FILE
      common /FLNAMES/ SAPRCGCFILE,
     &                 NCONCFILE, GCONCFILE, AECONCFILE,
     &                 SPECFILE,  OH_FILE, FN_FILE, CS_FILE,
     &                 Kappa_FILE, O3_FILE,
     &                 WALL_GC, WALL_MK, WALL_NK

C      common /FLNAMES/ datname, diagname,
C     &                 NCONCFILE, GCONCFILE, AECONCFILE

C     VARIABLE COMMENTS...

C-----ADJUSTABLE PARAMETERS---------------------------------------------
 1    FORMAT(A15,40E15.6)
 2    FORMAT(41E15.6)
 3    FORMAT(459E15.6)  !Icomp -1 
 4    FORMAT(557F40.20) !NACT
 5    FORMAT(F8.1,2x,E10.4)         
C-----CODE--------------------------------------------------------------

C Time

      write(*,1) 'Time (s): ', time
      write(*,1) 'Time (h): ', time/3600.
      print*, NCONCFILE,GCONCFILE,AECONCFILE,CS_FILE,HOM_FILE,DBK_FILE
      OPEN(UNIT=34, FILE=NCONCFILE, STATUS='OLD', ACCESS='APPEND')
      print*, 'Opened 34'
      WRITE(34,2) time/3600., (Nk(K)/boxvol,K=1,IBINS)
      print*, ''
      CLOSE(34)

      OPEN(UNIT=35, FILE=GCONCFILE, STATUS='OLD', ACCESS='APPEND')
      print*, 'Opened 35'
      WRITE(35,3) time/3600. , (Gc(N),N=1,ICOMP-1)
      CLOSE(35)
      
      OPEN(UNIT=36, FILE=AECONCFILE, STATUS='OLD', ACCESS='APPEND')
      print*, 'Opened 36'
      DO J=1,ICOMP
         WRITE(36,2) time/3600., (Mk(N,J)*1.0E9 / 
     &                boxvol * 1.0E6, N=1, IBINS)
      END DO
      CLOSE(36)

      OPEN(UNIT=38, FILE=SAPRCGCFILE, STATUS='old',ACCESS='APPEND')
      print*, 'Opened 38'
      WRITE(38,4) SAPRCGC2(1:NACT)
!      WRITE(38,FRMT2) SAPRCGC(1:NACT)
      CLOSE(38)

      OPEN(UNIT=46, FILE=Kappa_FILE, STATUS='old',ACCESS='APPEND')
      print*, 'Opened 46' 
      WRITE(46,2) time/3600.,(kappa_avg2(K),K=1,IBINS)
      CLOSE(46)

!      OPEN(UNIT=55, FILE=WALL_MK, STATUS='OLD', ACCESS='APPEND')
!      DO J=1,ICOMP
!         WRITE(55,2) time/3600., (Mk_wall(N,J)*1.0E9 / 
!     &                boxvol * 1.0E6, N=1, IBINS)
!      END DO
!      CLOSE(55)
      
!      OPEN(UNIT=54, FILE=WALL_NK, STATUS='OLD', ACCESS='APPEND')
!      WRITE(54,2) time/3600., (Nk_wall(K)/boxvol,K=1,IBINS)
!      CLOSE(54)
      
!      OPEN(UNIT=53, FILE=WALL_GC, STATUS='OLD', ACCESS='APPEND')
!      WRITE(53,3) time/3600., (Gc_wall(N),N=1,ICOMP-1)
!      CLOSE(53)

      print*, CS_FILE, HOM_FILE, DBK_FILE
      OPEN(UNIT=45, FILE=CS_FILE, STATUS='old', ACCESS='append')
      print*, 'Opened 45'
      WRITE(45,5) time/3600., CS2
      CLOSE(45)

      OPEN(UNIT=48, FILE=HOM_FILE, STATUS='old', ACCESS='append')
      print*, 'Opened 48'

      WRITE(48,5) time/3600., HOM2
      CLOSE(48)
      
      OPEN(UNIT=56, FILE=DBK_FILE, STATUS='old', ACCESS='append')
      WRITE(56,5) time/3600., Dbk
      CLOSE(56)

      RETURN
      END
