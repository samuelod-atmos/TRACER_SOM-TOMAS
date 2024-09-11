C     **************************************************
C     *  box                                           *
C     **************************************************

C     WRITTEN BY Peter Adams, October 1999

C     This program is a box model that is used to test the size
C     resolved aerosol code for the GISS GCM.

c      subroutine box(nucbase,H2SO4rate,life)a
      PROGRAM box

      IMPLICIT NONE
      
C-----INCLUDE FILES--------------------------------------------------

      include 'sizecode.COM'

      ! AliA ////////////////////////////////////////////////////////
      include 'modlspc.h'  
      include 'common.inc'
      include 'gaskin.h' 
      ! \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ AliA
      
C-----INPUTS---------------------------------------------------------

C-----VARIABLE DECLARATIONS------------------------------------------
      integer i,j,l,n,k,ttt,v,II      !counters
      integer iseed, getlen
      integer nsteps            !number of timesteps per hour
      integer hourint
      integer nintern,tstep ! number of internal mphys steps
      integer tvar 
      INTEGER INDOMFRACI

      logical dayflag, clearflag  !true/false for day/night or clear/cloudy

      external getlen, setoh

      double precision No1, Dp1, sigma1 !lognormal parameters (No in #/cm3,Dp in um)
      double precision No2, Dp2, sigma2 !lognormal parameters (No in #/cm3,Dp in um)
      double precision Nc, Dpc,sigmac
      double precision time     !elapsed time (seconds)
      double precision hour  !elapsed time (hours)
      double precision adt,aadt,aadtn      !aerosol microphysics time step (seconds)
      double precision aadtp ! previous dynamic timestep
      double precision Dpk, vd  !particle diameter (um) and drydep velocity (cm/s)
      double precision mnucl    !mass nucleating in a time step (kg)
      double precision Ntot     !used to check number conservation by condensation
      double precision area     !xsect area of plume (m2)
      double precision boxvolp     !previous boxvol (m3)
      double precision ohc   !OH conc (molec cm-3)
      double precision cyclet   !how far into 12-hour diurnal cycle we are (s)
      double precision setoh
      double precision u10
      double precision focean
      double precision endtime
      double precision tot_n_1, tot_n_2, tot_num
      double precision tot_s_1, tot_s_2
      double precision test     !test criteria for if we need to call report
      double precision tau(IBINS)
      double precision Nkout(IBINS), Mkout(IBINS,icomp)
      double precision Gcout(icomp-1)
      double precision Nkt(IBINS), Mkt(IBINS,icomp)
      double precision Gct(icomp-1)
      double precision nucrate ! nucleation rate [cm-3 s-1]
      double precision dilt, dilratio ! dilution timescale [hr]
      double precision timerem
      double precision soarate ! soa formation rate [ug m-3 hr-1]
      double precision sulfrate ! sulf formation rate [ug m-3 hr-1]
      double precision massin ! mass to condense in timestep [kg]
      double precision tmass1,tmass2
      double precision tt, tn, tsu, toa ! temporary variables
      double precision timeall(500) ! all times from input [hr]
      double precision nucall(500) ! all nuc rates from input [cm-3 s-1]
      double precision sulfall(500) ! all sulfate conc from input [molec cm-3]
      double precision soaall(500) ! all soa rates from input [ug m-3 hr-1]
      double precision tempnum
      double precision CS, sinkfrac(IBINS)
      double precision tmp
      double precision R,e_s,w_s,w ! gas constant,sat. vap. pres.
      double precision orgfracinit ! initial fraction of mass that is organic
      double precision soascale ! scale factor for VBS mass
      double precision totamass ! sum to get total aerosol mass [ug m-3]
      double precision totmass ! sum to get total mass [ug m-3]
      double precision faero(iorg) ! fraction of POA initially in the aerosol phase
      double precision ampb(iorg) ! organic aerosol mass in each volatility bin
      double precision fampb(iorg) ! fraction of organic aerosol mass in each volatility bin
      double precision guess ! check for initializing mass	  
!      double precision kw0,ke!dilt2, kw_turb(36) !add by Emily
      double precision kpar,kvap_on!dilt2, kw_turb(36) !add by Emily
      double precision WalVapMas(iorg), P_temp(icomp)
      double precision P_temp1(ibins,icomp), P_num(ibins)	  ! add by Emily
      double precision tau_p, tau_w(iorg),kw_HYBRID(ibins)
      double precision Nkout1(IBINS), Mkout1(IBINS,icomp),Gc_v(icomp-1)
      double precision Nk1(IBINS), Mk1(IBINS,icomp)	  
      double precision alpha_i(5), kOH(6), Gc_i(15,15)
      DOUBLE PRECISION omfraci_val
      DOUBLE PRECISION dz, Jdiff, dCdt, ratio, delmass, KZ, V1, V2
      
      character*120 runname, datname, diagname, infilename, vapname
      CHARACTER*120 NCONCFILE, GCONCFILE, AECONCFILE, SPECFILE
      CHARACTER*120 SAPRCGCFILE, OH_FILE, FN_FILE, CS_FILE, Kappa_FILE
      CHARACTER*120 DIRECTORY,HOM_file,VOC_FILE,FLOW_FILE
      character*120 tauname,kwname,cglname,walname
      character*120 binfilename

      common /FLNAMES/ datname,   diagname,
     &                 NCONCFILE, GCONCFILE, AECONCFILE,
     &                 SPECFILE,  OH_FILE, FN_FILE, CS_FILE,
     &                 Kappa_FILE

CCC   AliA \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

      INTEGER IERR
      REAL*4 SLA
      CHARACTER*16 MODL ! SAPRC Model name

      CHARACTER*8 MCHNAME1, MCHNAME2
      CHARACTER*16 POA_1STNAME
      CHARACTER*16, ALLOCATABLE :: EMISS_SPNAME(:)
      CHARACTER*16, ALLOCATABLE :: SAPRC_SPNAME2(:) ! SAPRC active species name
      CHARACTER*16, ALLOCATABLE :: SOMPREC(:)
      CHARACTER*6, ALLOCATABLE :: PREC_ID(:)
      
      INTEGER CTR, CTRW
      INTEGER NEQNT
      INTEGER VWL, PWL, COAG ! vapor wall loss, particle wall loss, coagulation switches
      INTEGER POA_1ST_LENNAME ! first poa species length name
      INTEGER NSOMPREC ! Number of SOM precursors
      INTEGER POA_1STINDX ! POA 1st index in SAPRC
      INTEGER SOM_1STINDX ! SOM 1st species index in SAPRC
      INTEGER NSPEMISS    ! Number of species in emission inputs
      INTEGER SO2_INDX, SO4_INDX ! index of SO2 and SO4 in active species in SAPRC

      REAL, ALLOCATABLE :: SAPRCGC(:)
      REAL, ALLOCATABLE :: EMISS_IPPM(:)
      REAL, ALLOCATABLE :: MWT_ACTSP(:)
C      REAL, ALLOCATABLE :: DWSW(:),PBL(:)

C Vertical layer variables
C--------------------------------------------------------------------------------

C      INTEGER :: nlayers
C      REAL, ALLOCATABLE :: EMISS_IPPM_lay(:,:),O3_lay(:)
C      DOUBLE PRECISION, ALLOCATABLE :: Mk_lay(:,:,:),Mk_lay_o(:,:,:)
C      DOUBLE PRECISION, ALLOCATABLE :: Nk_lay(:,:),Nk_lay_o(:,:)
C      DOUBLE PRECISION, ALLOCATABLE :: Gc_lay(:,:),RKZ_lay(:,:)
C      DOUBLE PRECISION, ALLOCATABLE :: RK_lay(:,:),OH_lay(:)
C      DOUBLE PRECISION, ALLOCATABLE :: SAPRCGC_lay(:,:)
C      DOUBLE PRECISION, ALLOCATABLE :: pstar_lay(:,:)
C      DOUBLE PRECISION, ALLOCATABLE :: mworg_lay(:,:),Hvap_lay(:,:)
C      DOUBLE PRECISION, ALLOCATABLE :: N_bg1_lay(:),Dpm_bg1_lay(:)
C      DOUBLE PRECISION, ALLOCATABLE :: sigma_bg1_lay(:),sigma_bg2_lay(:)
C      DOUBLE PRECISION, ALLOCATABLE :: N_bg2_lay(:),Dpm_bg2_lay(:)
C      DOUBLE PRECISION, ALLOCATABLE :: N_bg3_lay(:),Dpm_bg3_lay(:)
C      DOUBLE PRECISION, ALLOCATABLE :: sigma_bg3_lay(:)
C      DOUBLE PRECISION, ALLOCATABLE :: pres_lay(:),temp_lay(:)
C      DOUBLE PRECISION, ALLOCATABLE :: KZ_lay(:),rh_lay(:),QV_lay(:)
C      DOUBLE PRECISION, ALLOCATABLE :: boxvol_lay(:),temp_lay_old(:)
C      DOUBLE PRECISION, ALLOCATABLE :: lay_edge(:),Z_lay(:) 
C      DOUBLE PRECISION  :: Dp_pa, LR_K, upper_pres, T_bar
C      DOUBLE PRECISION  :: temp
C      CHARACTER :: FRMT*13,FRMT2*15
C--------------------------------------------------------------------------------

      DOUBLE PRECISION AutoFrac
      PARAMETER(AutoFrac = 0.1)

      DOUBLE PRECISION ORG_O2C(iORG)

C--------------------------------------------------------------------------------
      DOUBLE PRECISION, ALLOCATABLE :: DLVP(:)
      DOUBLE PRECISION, ALLOCATABLE :: SEED_FRAC(:)
      
      REAL TEMP1, TIN, TOUT
      REAL CALVALREAL
      DOUBLE PRECISION CALVALDBLE
      
      DOUBLE PRECISION Dbk ! particle-phase diffusion coefficient [m2/s] 
      DOUBLE PRECISION Kc  ! first-order loss rate of species in the particle phase [1/s]

      REAL a_oh, ax_oh, b_oh, bx_oh,OH_NIGHT ! OH parameters for changing
                                             ! the OH concentration over time
C      REAL lights_on       ! the time when lights were turned on in the experiments
                           ! that OH concentration is not zero anymore
      REAL X,Y,P1,P2,NOX   ! Variables for Stevens et al. 2012 OH proxy
      REAL OH_MULT         ! Scalar for the OH concentration 
      DATA  MODL / 'SAPRC14_REV1' /

      EXTERNAL DIFF
      DOUBLE PRECISION, EXTERNAL :: CALC_DB

      ! Dilution
      DOUBLE PRECISION time_new, time_old
      DOUBLE PRECISION p_dilt1, p_dilt2, p_dilt3, p_dilt4
      DOUBLE PRECISION dilt_rate_new, dilt_rate_old
      DOUBLE PRECISION boxvol_old, initial_boxvol

      ! Background size distribution
      DOUBLE PRECISION N_bg1, Dpm_bg1, sigma_bg1
      DOUBLE PRECISION N_bg2, Dpm_bg2, sigma_bg2
      DOUBLE PRECISION N_bg3, Dpm_bg3, sigma_bg3
      DOUBLE PRECISION density_bg, orgfrac_bg

      ! nucleation variables added in March 2020
      DOUBLE PRECISION CSTAR_NUC ! cstar limit for nucleation
      INTEGER ORG_NUC, INORG_NUC ! Ricco and Dunne nucleation switch
      DOUBLE PRECISION FION 
      DOUBLE PRECISION kappa_avg(ibins)
      ! NH3 and H2SO4 Variables: added by SamO on April 24, 2020
      DOUBLE PRECISION NH3MOLEC_CM3,NH3_ppt
C      DOUBLE PRECISION H2SO4_CM3
     
      INTEGER tester1
      CHARACTER*6 tester2
      CHARACTER*3 tester3
      CHARACTER*4 tester4

      INTEGER INDEX_VOC(6)
      DOUBLE PRECISION Gc_ppb(6) 
      DOUBLE PRECISION Fm,Fi
C      DATA INDEX_VOC /1,1,1,1,1,1/

C      INTEGER DEX
      DOUBLE PRECISION fHOM(6)
      DATA fHOM /0.002,0.002,0.001,0.014,0.0,0.034/
      DOUBLE PRECISION HOM,HOM2,dHOM
C      DOUBLE PRECISION, ALLOCATABLE :: HOM_lay(:)

C      LOGICAL file_test
CCC   ////////////////////////////////////////////////////////////////////////// AliA

C-----VARIABLE COMMENTS----------------------------------------------

C-----ADJUSTABLE PARAMETERS------------------------------------------

      parameter(R=8.314159)

C-----CODE-----------------------------------------------------------

      HOM = 0.0
      write(*,*) 'Enter name of run'
      read(*,'(A120)') runname

      datname='../../outputs/'//runname(1:getlen(runname))//
     &     '.dat'
      diagname='../../outputs/'//runname(1:getlen(runname))//
     &     '.diag'
      vapname='../../outputs/'//runname(1:getlen(runname))//
     &     '_vl.dat'
      tauname='../../outputs/'//runname(1:getlen(runname))//
     &     '_tau.dat'
      kwname='../../outputs/'//runname(1:getlen(runname))//
     &     '_kw.dat'  
      walname='../../outputs/'//runname(1:getlen(runname))//
     &     '_wal.dat'
      NCONCFILE='../../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
     &     '_noconc.dat'
      GCONCFILE='../../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
     &     '_gc.dat'
      SAPRCGCFILE='../../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
     &     '_saprcgc.dat'
      AECONCFILE='../../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
     & '_aemass.dat'
      SPECFILE='../../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
     &     '_spec.dat'
C      OH_FILE='../../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
C     &     '_oh.dat'
      FN_FILE='../../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
     &     '_fn.dat'
      CS_FILE='../../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
     &     '_cs.dat'
      Kappa_FILE='../../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
     &     '_kappa.dat'
      HOM_FILE='../../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
     &     '_hom.dat'
      VOC_FILE='../../inputs/'//RUNNAME(1:GETLEN(RUNNAME))//
     &     '_voc'
      FLOW_FILE='../../inputs/'//RUNNAME(1:GETLEN(RUNNAME))//
     &     '_flows'
      OH_FILE='../../inputs/'//RUNNAME(1:GETLEN(RUNNAME))//
     &     '_OH'

C      datname='../outputs/'//runname(1:getlen(runname))//
C     &     '.dat'
C      diagname='../outputs/'//runname(1:getlen(runname))//
C     &     '.diag'
C      vapname='../outputs/'//runname(1:getlen(runname))//
C     &     '_vl.dat'
C      tauname='../outputs/'//runname(1:getlen(runname))//
C     &     '_tau.dat'
C      kwname='../outputs/'//runname(1:getlen(runname))//
C     &     '_kw.dat'  
C      walname='../outputs/'//runname(1:getlen(runname))//
C     &     '_wal.dat'
C      NCONCFILE='../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
C     &     '_noconc.dat'
C      GCONCFILE='../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
C     &     '_gc.dat'
C      SAPRCGCFILE='../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
C     &     '_saprcgc.dat'
C      AECONCFILE='../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
C     & '_aemass.dat'
C      SPECFILE='../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
C     &     '_spec.dat'
C      OH_FILE='../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
C     &     '_oh.dat'
C      FN_FILE='../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
C     &     '_fn.dat'
C      CS_FILE='../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
C     &     '_cs.dat'
C      Kappa_FILE='../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
C     &     '_kappa.dat'
C      HOM_FILE='../outputs/'//RUNNAME(1:GETLEN(RUNNAME))//
C     &     '_hom.dat'
 
      write(*,*) datname
      write(*,*) diagname
      write(*,*) vapname
      write(*,*) kwname
      write(*,*) walname
      WRITE(*,*) NCONCFILE
      WRITE(*,*) GCONCFILE
      WRITE(*,*) SAPRCGCFILE
      WRITE(*,*) AECONCFILE
      WRITE(*,*) SPECFILE
C      WRITE(*,*) OH_FILE
      WRITE(*,*) FN_FILE  
      WRITE(*,*) CS_FILE
      WRITE(*,*) Kappa_FILE
      WRITE(*,*) HOM_FILE
      WRITE(*,*) VOC_FILE

      open(unit=30,file=datname,status='new')
      close(30)
      open(unit=31,file=vapname,status='new')
      close(31)
      open(unit=32,file=tauname,status='new')
      close(32)
      open(unit=33,file=kwname,status='new')
      close(33)
      OPEN(UNIT=34, FILE=NCONCFILE, STATUS='new')
      CLOSE(34)
      OPEN(UNIT=35, FILE=GCONCFILE, STATUS='new')
      CLOSE(35)
      OPEN(UNIT=36, FILE=AECONCFILE, STATUS='new')
      CLOSE(36)
      OPEN(UNIT=37, FILE=SPECFILE, STATUS='new')
      CLOSE(37)
      OPEN(UNIT=38, FILE=SAPRCGCFILE, STATUS='new')
      CLOSE(38)
C      OPEN(UNIT=39, FILE=OH_FILE, STATUS='new')
      OPEN(UNIT=39, FILE=OH_FILE, STATUS='old')
C      CLOSE(39)
      OPEN(UNIT=40, FILE=FN_FILE, STATUS='new')
      CLOSE(40)
      OPEN(UNIT=45, FILE=CS_FILE, STATUS='new')
      CLOSE(45)
      OPEN(UNIT=46, FILE=Kappa_FILE, STATUS='new')
      CLOSE(46)
      OPEN(UNIT=48, FILE=HOM_FILE, STATUS='new')
      CLOSE(48)
      OPEN(UNIT=49, FILE=VOC_FILE, STATUS='old')
      OPEN(UNIT=50, FILE=FLOW_FILE, STATUS='old')

      WRITE(*,*) 'Enter the microphysics timestep'
      READ(*,*) aadt
      PRINT*, 'aadt=', aadt
      WRITE(*,*) 'Enter the frequency of printing values'
      WRITE(*,*) 'Or number of internal microphysics steps'
      READ(*,*) nintern
      PRINT*, 'nintern=', nintern

      adt=aadt*nintern ! timestep for writing output [seconds]
      PRINT*, 'adt=', adt

      WRITE(*,*) 'Enter 0/1 to swith Off/On coagulation'
      read(*,'(I1)') COAG
C      VWL = 1
      print*, 'COAG=', COAG

      WRITE(*,*) 'Enter 0/1 to swith Off/On vapor wall losses'
      read(*,'(I1)') VWL
C      VWL = 1
      print*, 'VWL=', VWL

      WRITE(*,*) 'Enter 0/1 to swith Off/On particle wall losses'
      read(*,'(I1)') PWL
C      PWL = 1
      print*, 'PWL=', PWL

      read(*,*) kvap_on
C      ke = 1.074685063
      print*,'kvap_on =', kvap_on
      
      read(*,*) kpar
C      kw0 = 8.03E-05 
      print*, 'kpar =', kpar
      
C      WRITE(*,*) 'Lights On time [s]'
C      READ(*,*) lights_on
C      PRINT*, 'lights_on=', lights_on

C      WRITE(*,*) 'Enter OH concentration parameters [molecules cm-3]'
C      WRITE(*,*) 'a_oh*exp(-1.*ax_oh*t) + b_oh*exp(-1.*bx_oh*t)'
C      WRITE(*,*) 't in seconds'
C      READ(*,*) ohc
C      PRINT*, 'ohc =', ohc
C      READ(*,*) ax_oh
C      PRINT*, 'ax_oh =', ax_oh
C      READ(*,*) b_oh
C      PRINT*, 'b_oh =', b_oh
C      READ(*,*) bx_oh
C      PRINT*, 'bx_oh =', bx_oh

      READ(*,*) OH_MULT
      PRINT*, 'OH_MULT =', OH_MULT

C      READ(*,*) NOX
C      PRINT*, 'NOX =',NOX

      write(*,*) 'Enter the ion recombination coefficient' ! DONT FORGET TO CHECK !!!!!!!!!!!!!!!!!!!!!!!!!
      read(*,'(F15.4)') FION ! [cm-3 s-1]
C      FION = 0.0
      print*, 'FION=', FION

C      write(*,*) 'Enter Cstar Limit for nucleation'
C      read(*,'(E8.1)') CSTAR_NUC ! [ug m-3]
C      CSTAR_NUC = 0.0
C      print*, 'CSTAR_NUC=', CSTAR_NUC
      
      write(*,*) 'Turn Organic (Ricco) Nucleation On/Off'
      read(*,'(I1)') ORG_NUC
C      ORG_NUC = 0.0
      print*, 'ORG_NUC=', ORG_NUC

      write(*,*) 'Turn Inorganic (Dunne) Nucleation On/Off'
      read(*,'(I1)') INORG_NUC
C      DUNNE_NUC = 0.0
      print*, 'INORG_NUC=', INORG_NUC
      
      write(*,*) 'Enter the NH3 concentration [ppt]'
      read(*,'(E8.1)') NH3_ppt
C      NH3_ppt = 0.0
      print*, 'NH3_ppt=', NH3_ppt

      write(*,*) 'Enter the size of the bag'
      read(*,'(E15.1)') BOXVOL
C      boxvol = 7000000.0
      print*, 'boxvol=', BOXVOL
      
      write(*,*) 'Enter the hours of run time (make even hours)'
      read(*,'(F8.5)') endtime
C      endtime = 4.0
      print*, 'endtime=', endtime

      write(*,*) 'Enter the accommodation coefficient (alpha)'
      read(*,'(F8.5)') alpha
C      alpha = 1.0
      print*, 'alpha=', alpha
      
      write(*,*) 'Enter the particle phase diffusivity'
      read(*,'(F8.5)') Dbk
C      Dbk = 1.0d-10
      print*, 'Dbk=', Dbk

      write(*,*) 'first-order loss rate of species in the'
     &     //' particle phase'
      read(*,'(F10.8)') kc
      print*, 'kc =', kc     
      
      write(*,*) 'Enter surface tension [N/m]'
      read(*,'(F8.5)') storg
C      storg = 0.025
      print*, 'storg=', storg


C      read(*,'(F12.3)') upper_pres
C      print*,'upper_pres=', upper_pres

C      write(*,*) 'Just a format string'
C      read(*,'(A13)') FRMT
C      print*,'FRMT=', FRMT

C      write(*,*) 'Enter KZ value'
C      read(*,*) KZ
C      print*,'KZ=', KZ

      write(*,*) 'Enter temperature [K]'
      read(*,'(F8.5)') temp
C      temp = 292.85
      print*,'temp=', temp

C      write(*,*) 'Enter lapse rate [K/km]'
C      read(*,'(F12.3)') LR_K 
C      print*,'LR_K=', LR_K
      
C --- First number size distribution ------------------------------------
      write(*,*) 'Enter 1st background number conc'
      read(*,'(F8.5)') No1
C      No = 5843.0
      print*, 'No1=', No1

      write(*,*) 'Enter 1st background median diameter [microns]'
      read(*,'(F8.5)') Dp1
C      Dp = 0.157
      print*, 'Dp1=', Dp1

      write(*,*) 'Enter 1st background sigma'
      read(*,'(F8.5)') sigma1
C      sigma = 1.73
      print*, 'sigma1=', sigma1

C --- Second number size distribution -----------------------------------
      write(*,*) 'Enter 2nd background number conc'
      read(*,'(F8.5)') No2
C      No = 5843.0
      print*, 'No2=', No2

      write(*,*) 'Enter 2nd background median diameter [microns]'
      read(*,'(F8.5)') Dp2
C      Dp = 0.157
      print*, 'Dp2=', Dp2

      write(*,*) 'Enter 2nd background sigma'
      read(*,'(F8.5)') sigma2
C      sigma = 1.73
      print*, 'sigma2=', sigma2

CCC   AliA \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\  
      READ(*,'(I2)') NSOMPREC
      print*, 'NSOMPREC=', NSOMPREC
      ALLOCATE(SOMPREC(NSOMPREC),
     &         PREC_ID(NSOMPREC),
     &         DLVP(NSOMPREC))

      READ(*,*) SOMPREC
      PREC_ID = SOMPREC(:)(1:3)
      print*, 'SOMPREC=', SOMPREC
      print*, 'PREC_ID=', PREC_ID

      READ(*,*) DLVP
      print*, 'DLVP=', DLVP(:)

      READ(*,*) POA_1STNAME
      PRINT*, 'POA_1STNAME=', POA_1STNAME

      READ(*,*) POA_1ST_LENNAME
      PRINT*, 'POA_1ST_LENNAME=', POA_1ST_LENNAME

      READ(*, '(I3)') NSPEMISS
      PRINT*, 'NSPEMISS=', NSPEMISS
      ALLOCATE(EMISS_SPNAME(NSPEMISS),
     &         EMISS_IPPM(NSPEMISS),
     &         SEED_FRAC(NSPEMISS))

      READ(*,*) EMISS_SPNAME
      PRINT*, 'EMISS_SPNAME=', EMISS_SPNAME
      READ(*,*) EMISS_IPPM
      PRINT*,'EMISS_IPPM =',EMISS_IPPM
      READ(*,*) SEED_FRAC
      PRINT*, 'SEED_FRAC=', SEED_FRAC
C      STOP
CAliA READ the POA related values for initialization
      READ(*,*) SEED_DENS
      PRINT*, 'SEED_DENS=', SEED_DENS


CC      PRINT*, 'Just allocated bg arrays'
      READ(*,*) N_bg1
CC      PRINT*,'Successfully read'
      PRINT*, 'N_bg1=', N_bg1
      READ(*,*) Dpm_bg1
      PRINT*, 'Dpm_bg1', Dpm_bg1
      READ(*,*) sigma_bg1
      PRINT*, 'sigma_bg1=', sigma_bg1
      READ(*,*) N_bg2
      PRINT*, 'N_bg2=', N_bg2
      READ(*,*) Dpm_bg2
      PRINT*, 'Dpm_bg2=', Dpm_bg2
      READ(*,*) sigma_bg2
      PRINT*, 'sigma_bg2=', sigma_bg2
      READ(*,*) N_bg3
      PRINT*, 'N_bg3=', N_bg3
      READ(*,*) Dpm_bg3
      PRINT*, 'Dpm_bg3=', Dpm_bg3
      READ(*,*) sigma_bg3
      PRINT*, 'sigma_bg3=', sigma_bg3

      READ(*,*) density_bg
      PRINT*, 'density_bg=', density_bg

      READ(*,*) orgfrac_bg
      PRINT*, 'orgfrac=', orgfrac_bg

      ! dilution variables
      !READ(*,*) p_dilt1
      !PRINT*, 'p_dilt1=', p_dilt1 
      !READ(*,*) p_dilt2
      !PRINT*, 'p_dilt2=', p_dilt2
      !READ(*,*) p_dilt3
      !PRINT*, 'p_dilt3=', p_dilt3
      !READ(*,*) p_dilt4
      !PRINT*, 'p_dilt4=', p_dilt4
      
C      initial_boxvol = boxvol
C      PRINT*, 'initial_boxvol=', initial_boxvol

CCC   /////////////////////////////////////////////////////////////////////////// AliA
C-----------------------------------------------------------------------------------

C Temperature profile and pressure profile: 
C-----------------------------------------------------------------------------------
C      OPEN(UNIT = 43, FILE = '../../inputs/'// runname(1:8)
C     & //'_Temperatures',STATUS = 'old')
C      DO I=1,INT(endtime*360)

C      READ(43,FRMT) temp_lay
C      OPEN(UNIT = 44, FILE ='../../inputs/'// runname(1:8)
C     & //'_SfcPres',STATUS = 'old')
C      READ(44,*) sfcpres 
C      Dp_pa = (sfcpres - upper_pres)/nlayers
C      pres_lay(1) = sfcpres - 0.5*Dp_pa
C      lay_edge(1) = sfcpres
C
C      DO I=1,nlayers
C        lay_edge(I+1) = lay_edge(I)-Dp_pa
C      ENDDO
C
C      DO I=1,nlayers-1
C        pres_lay(I+1) = pres_lay(I)-Dp_pa
C      ENDDO

C      print*,'lay_edge =',lay_edge
C      print*,'Pressure levels = ',pres_lay
C      print*,'Initial Temperature levels =',temp_lay

C-----------------------------------------------------------------------------------
C      ALLOCATE(DWSW(INT(endtime*3600/aadt)))
C      OPEN(UNIT = 41, FILE = '../../inputs/'// runname(1:8)
C     &  //'_SW_Rad',STATUS = 'old')
C      DO I=1,INT(endtime*3600/aadt)
C       READ(41,100) DWSW(I)
C      ENDDO 
C      CLOSE(UNIT=41) 

C------ PBL Height ----------------------------------------------

C      ALLOCATE(PBL(INT(endtime*3600/aadt)))
C      OPEN(UNIT = 42, FILE = '../../inputs/'// runname(1:8)
C     & //'_PBL_Height',STATUS = 'old')
C      DO I=1,INT(endtime*3600/aadt)
c        READ(42,100) PBL(I)
C      ENDDO 
C      CLOSE(UNIT=42)

C-------initialize wall vapour concentration---------------------
      do j = 1,iorg
        WalVapMas(j) = 0.0
      enddo
      do j = 1,icomp
        P_temp(j) = 0.0
      enddo
      do j = 1,iorg
         tau_w(j) = 0.0
      enddo
      tau_p = 0.0
  
      do n = 1,ibins
         do j = 1,icomp
            P_temp1(n,j) = 0.0
            Mk1(n,j) = 0.0
         enddo
         P_num(n) = 0.0
         Nk1(n) = 0.0
      enddo
      
      do j=1,icomp-1
         Gc_v(j) = 0.0
      enddo

      do n=1,15
         do j=1,15
            Gc_i(n,j) = 0.0
         enddo
      enddo
      
C BEGINNING OF LAYER INITIALIZATION
C=================================================================================

C      DO v=1, nlayers
C      print*,'Initializing layer:',v
C      temp = temp_lay(v)
C      pres = pres_lay(v)
Cc      rh = rh_lay(v) 
C      print*,'temp =',temp
C      print*,'pres =',pres
C      N_bg1 = N_bg1_lay(v)
C      Dpm_bg1 = Dpm_bg1_lay(v)
C      sigma_bg1 = sigma_bg1_lay(v)
C      N_bg2 = N_bg2_lay(v)
C      Dpm_bg2 = Dpm_bg2_lay(v)
C      sigma_bg2 = sigma_bg2_lay(v)
C      N_bg3 = N_bg3_lay(v)
C      Dpm_bg3 = Dpm_bg3_lay(v)
C      sigma_bg3 = sigma_bg3_lay(v)
C      EMISS_IPPM(:) = EMISS_IPPM_lay(v,:)
C      Gc(:) = 0.0
C      time=0.0

      pres = 101325.0
      boxmass=0.0289*pres*boxvol*1.0e-6/R/temp
      hour=time/3600.

      ! get organic aerosol psats at current temperature 
      ! modified cstar as the function of temp

      print*, 'NSOMPREC=', NSOMPREC
      print*, 'PREC_ID=', PREC_ID
      print*, 'NSPEMISS=', NSPEMISS
      print*, 'DLVP=', DLVP
      print*, 'POA_1STNAME=', POA_1STNAME
      print*, 'POA_1ST_LENNAME=', POA_1ST_LENNAME
      print*, 'POA_1STINDX=', POA_1STINDX
      print*, 'SOM_1STINDX=', SOM_1STINDX
      print*, 'time=', time
      print*, 'pres =',pres
      print*, 'temp =',temp
      print*, 'boxmass =',boxmass
      print*, 'boxvol =',boxvol

C --- Call saprc_init to initialize gas-phase concentration and intial values ---------------------
      OPEN(UNIT=1, FILE='saprc14_rev1.mod', STATUS='old')
      OPEN(UNIT=3, FILE='saprc14_rev1.doc', STATUS='unknown')

      print*, '11111'
      
      TREF = 298.0
      TEMP1 = temp
      CALL RDMOD(MODL, 1, 3, .true., TEMP1, 0, IERR,
     &     NS, NACT, NSC, NSB, NDUM,
     &     NRXN, LENKBF, NCOC1, NCOC2,
     &     NCOEFV, NPHOTK, TREF, SLA,
     &     DECLN, TSTART, CZMIN, MWT,
     &     CONC0, CNO, NNO, SNO,
     &     ONO, XNO, NRHC1, INDRHC,
     &     RK, KPBUF, COEF, ABSQY,
     &     DPHOTK, LKBUF, IPHRK, IRXTYP,
     &     NAME, RXNLBL, COEFNM,
     &     PHOTNM, TITLE) 
      call flush(6) 
      CLOSE(UNIT=1)
      CLOSE(UNIT=3)

      print*, '22222'
      print*, 'NACT=', NACT
      
C      IF (v.eq.1) THEN
      ALLOCATE(SAPRCGC(NACT), MWT_ACTSP(NACT), SAPRC_SPNAME2(NACT)) ! initialize the array size of total gas concentration
C        ALLOCATE(SAPRCGC_lay(NACT,nlayers))
C      ENDIF

      SAPRCGC(:) = 0.0
      MWT_ACTSP(:) = 0.0

      print*, '33333'

      CALL SAPRC_INIT(SAPRCGC, NSOMPREC, PREC_ID,  
     &                NSPEMISS, EMISS_SPNAME, EMISS_IPPM,  
     &                SEED_FRAC, DLVP, MWT_ACTSP,
     &                SOM_1STINDX, SO2_INDX, SO4_INDX, time,
     &                ORG_O2C,SAPRC_SPNAME2,INDEX_VOC,kOH)
      
      print*,'INDEX_VOC =',INDEX_VOC
      print*,'kOH =',kOH
      
      print*, 'name(i), saprcgc(i)'
      do i=1,NACT
         print*, i, '-', name(i+13), saprcgc(i)
      enddo

      TOUT = REAL(time) + tstep*REAL(aadt)
      TOUT = TOUT/60.0
C      OPEN(UNIT=39, FILE=OH_FILE, STATUS='old', ACCESS='append')
C      WRITE(39,905) TOUT*60.0, CONST(6)
C      CLOSE(39)
      
      Nk(:) = 0.0
      Mk(:,:) = 0.0

C     call boxinit(time,No,Dp,sigma,SRTSO4)
      call boxinit(time,No1,Dp1,sigma1,No2,Dp2,sigma2)
      call loginit_bg(N_bg1, Dpm_bg1, sigma_bg1,
     &        N_bg2, Dpm_bg2, sigma_bg2, N_bg3, Dpm_bg3,
     &        sigma_bg3, density_bg,
     &        orgfrac_bg, boxvol, time+(tstep-1)*aadt)

      !print*,'N_bg2=',N_bg2,'Dpm_bg2=',Dpm_bg2,'sigma_bg2=',sigma_bg2
      ! read in background aerosol concentrations
      totamass=0.d0
      do n=1,ibins
         totamass=totamass+Nk(n)*sqrt(xk(n)*xk(n+1))
      enddo
      
      print*,'Nk(:) =',Nk(:) 
      print*,'SUM(Nk) =',SUM(Nk)
      print*,'totamass [ug m-3]', totamass*1.0e9/boxvol*1.0e6
      print*,'totalmass =', SUM(Mk(:,SRTORG1:SRTORGLAST))/boxvol*1e15
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
      DO N=1,IBINS
         IF (Nk(N) .LT. 1d-60) THEN
            Nk(N) = 0.d0
         END IF
         DO J=1,ICOMP
            IF (Mk(N,J) .LT. 1d-60) THEN
               Mk(N,J) = 0.d0
            END IF
         ENDDO !721
      ENDDO    !722 
      
      DO I=1,ICOMP-1
         IF (GC(I) .LT. 1d-60) THEN
            GC(I) = 0.d0
         END IF
      ENDDO
      DO I=1,NACT
         IF (SAPRCGC(I) .LT. 1d-60) THEN
            SAPRCGC(I) = 0.d0
         END IF
      ENDDO
      
      call report(time)
 999  FORMAT(556F40.20)
      OPEN(UNIT=38, FILE=SAPRCGCFILE, STATUS='old',ACCESS='APPEND')
      OPEN(UNIT=38, FILE=SAPRCGCFILE, STATUS='old',ACCESS='APPEND')
      WRITE(38,999) SAPRCGC(1:NACT)
      CLOSE(38)

C      Nk_lay(:,v) = Nk(:)
C      Gc_lay(:,v) = Gc(:)
C      RKZ_lay(:,v) = RKZ(:)
C      RK_lay(:,v) = RK(:)
C      SAPRCGC_lay(:,v) = SAPRCGC(:) 
C      cstar_lay(:,v) = CSTAR(:)
C      pstar_lay(:,v) = pstar(:)
C      mworg_lay(:,v) = mworg(:)
C      Hvap_lay(:,v)  = Hvap(:)
C      boxvol_lay(v)  = boxvol
C      O3_lay(v) = .055
      print*,'Here are some parameters:',N_bg1
      print*,Dpm_bg1
      print*,sigma_bg1
C      print*,N_bg2
C      print*,Dpm_bg2
C      print*,sigma_bg2
C      print*,N_bg3
C      print*,Dpm_bg3
C      print*,sigma_bg3
C      print*,'Mk_lay(v)=',Mk_lay(:,:,v)
C      print*,'Nk_lay(v)=',Nk_lay(:,v)
C      print*,'Gc_lay(v)=',Gc_lay(:,v)
      print*,temp
      print*,pres

C      END DO

C      DO N=1,NACT
C        SAPRCGC_lay(:,1) = 1E-30 
C        SAPRCGC_lay(:,2) = 1E-30 
C        SAPRCGC_lay(:,3) = 1E-30 
C        SAPRCGC_lay(:,4) = 1E-30 
C      ENDDO
C      DO N=1,icomp-1
C        Gc_lay(N,1) = 1E-30
C        Gc_lay(N,2) = 1E-30
C        Gc_lay(N,3) = 1E-30
C        Gc_lay(N,4) = 1E-30
C      ENDDO
C      DO N=1,IBINS
C         Nk_lay(n,1) = 1E-30
C         Nk_lay(n,2) = 1E-30
C         Nk_lay(n,3) = 1E-30
C         Nk_lay(n,4) = 1E-30
C         DO J=1,ICOMP
C            Mk_lay(n,j,1) = 1E-30
C            Mk_lay(n,j,2) = 1E-30
C            Mk_lay(n,j,3) = 1E-30
C            Mk_lay(n,j,4) = 1E-30
C         ENDDO !721
C      ENDDO    !722 
C END OF LAYER INITIALIZATION
C==============================================================================

      CTRW = 0

 10   continue  !beginning of new time step

      
      !OPEN(UNIT = 41, FILE = '../../inputs/'// runname(1:8)
     !@&  //'_SW_Rad',STATUS = 'old')
      !DO I=1,INT(endtime*3600/aadt)
      READ(50,'(f5.2,f5.2)') Fm,Fi
      print*,'Fm=',Fm,'Fi=',Fi
      READ(39,*) ohc
      print*,'ohc=',ohc
      READ(49,'(6(e10.4))') Gc_ppb(:)
      print*,'Gc_ppb =',Gc_ppb

      DO I = 1,6
C        DEX = INDEX_VOC(i)
C        print*,'INDEX_VOC(I) =',INDEX_VOC(I)
C        print*,'SAPRCGC(INDEX_VOC(I)):',SAPRCGC(INDEX_VOC(I))
C        print*,'DOUBLE PREC',DBLE(SAPRCGC(INDEX_VOC(I)))
C        print*,'kOH(I):',kOH(I)
C        print*,'fHOM(I):',fHOM(I)
C        print*,'CONST(6):',CONST(6)
C        Gc_ppb(INDEX_VOC(I)) = Gc_ppb(INDEX_VOC(I)) + 
C     &                     Ctube*(Fi+Fm)/boxvol*aadt +
C     &                     Gc_ppb(INDEX_VOC(I))*(Fi+Fm)/boxvol*aadt

        Gc(INDEX_VOC(I)) = Gc(INDEX_VOC(I)) + 

     &        Gc_ppb(INDEX_VOC(I))*(Fi+Fm)/boxvol*aadt*1.0E-6
     &      * PRES/R/TEMP * MWORG(INDEX_VOC(I)) *
     &      1.0E-3 * BOXVOL * 1.0e-6 -

     &      Gc(INDEX_VOC(I))*(Fi+Fm)/boxvol*aadt  !*1.0E-6
C     &      * PRES/R/TEMP * MWORG(INDEX_VOC(I)) *
C     &      1.0E-3 * BOXVOL * 1.0e-6



        !Gc(INDEX_VOC(I)) = Gc_ppb(INDEX_VOC(I))*XXXXXX
      END DO

      DO I=1,ibins
        Nk(I) = Nk(I) - Nk(I)*Fi/boxvol*aadt ! + inject 
      END DO
C      temp_lay_old = temp_lay
C      READ(43,FRMT) temp_lay
C      print*,'temp_lay = ',temp_lay
      
C      sfctemp = temp_lay(1)
C      READ(44,*) sfcpres 
C      Dp_pa = (sfcpres - upper_pres)/nlayers
C      pres_lay(1) = sfcpres - 0.5*Dp_pa
C      lay_edge(1) = sfcpres
C
C      OH_lay = OH_lay*OH_MULT
C      DO I=1,nlayers
C        lay_edge(I+1) = lay_edge(I)-Dp_pa
C        rh_lay(I) = 0.5
C      ENDDO
C      DO I=1,nlayers-1
C        pres_lay(I+1) = pres_lay(I)-Dp_pa
C      ENDDO

      
C      FRMT2 = '(00(F11.9,2x))'
C      write(FRMT2(2:3), '(I2)') nlayers

      

C      OPEN(UNIT = 49, FILE = '../../inputs/'// runname(1:8)
C     & //'_QV',STATUS = 'old')
C      READ(49,FRMT2) QV_lay
      
C      DO I=1,nlayers
C        w = QV_lay(I)/(1-QV_lay(I))
C        e_s = 611.0*exp((17.67*(temp_lay(I)-273.15))/
C     & (temp_lay(I)-29.65))
C        w_s = (e_s*287.05)/(461.552*(pres_lay(I)-e_s))
C
C        rh_lay(I) = w/w_s
C        IF (rh_lay(I).gt.0.95) THEN
C          rh_lay(I) = 0.95
C        ENDIF
C
C      ENDDO
      
C      print*,'rh_lay =',rh_lay 

C Now step through the layers
C ----------------------------------------------------------
C      do v=1, nlayers

C       print*,'Running layer',v
C       temp_lay(v) = sfctemp
C       temp = temp_lay(v)
C       pres = pres_lay(v) 
C       rh = rh_lay(v) 
       TREF = 298.0
       TEMP1 = temp
C       Mk(:,:) = Mk_lay(:,:,v)
C       Nk(:) = Nk_lay(:,v)
C       Gc(:) = Gc_lay(:,v)
C       RKZ(:) = RKZ_lay(:,v)
C       RK(:) = RK_lay(:,v)
C       mworg(:) = mworg_lay(:,v)
C       SAPRCGC(:) = SAPRCGC_lay(:,v)
C       CSTAR(:) = cstar_lay(:,v)
C       pstar(:) = pstar_lay(:,v)
C       Hvap(:) = Hvap_lay(:,v)
C       HOM = HOM_lay(v)
C       N_bg1 = N_bg1_lay(v)
C       Dpm_bg1 = Dpm_bg1_lay(v)
C       sigma_bg1 = sigma_bg1_lay(v)
C       N_bg2 = N_bg2_lay(v)
C       Dpm_bg2 = Dpm_bg2_lay(v)
C       sigma_bg2 = sigma_bg2_lay(v)
       NH3MOLEC_CM3 = NH3_ppt*1.E-12*pres*6.022E23/17.03/temp/R*1.e-6
       print*,'NH3MOLEC_CM3 =',NH3MOLEC_CM3  
C       boxvol_lay(v) = (temp_lay(v)*boxvol_lay(v))/temp_lay_old(v)
C       boxvol = boxvol_lay(v)
       boxmass=0.0289*pres*boxvol*1.0e-6/R/temp
       CONST(6) = ohc*1.0E6/6.022E23/PRES*R*TEMP*1.0E6
C       CONST(6) = DWSW(INT(TOUT*60/aadt))
       
C------------------------------------------------
C Now timestep through
       CTR = 0      
       do tstep=1,nintern

C HOM formation 
C ----------------------------------------------------------------

C     AUTOXIDATION: CHARLES
         dHOM = 0.d0
         HOM2 = 0.d0
C         print*,'INDEX_VOC =',INDEX_VOC
C         print*,'kOH =',kOH
         DO I = 1,6
C             DEX = INDEX_VOC(i)
C           print*,'INDEX_VOC(I) =',INDEX_VOC(I)
C           print*,'SAPRCGC(INDEX_VOC(I)):',SAPRCGC(INDEX_VOC(I))
C           print*,'DOUBLE PREC',DBLE(SAPRCGC(INDEX_VOC(I)))
C           print*,'kOH(I):',kOH(I)
C           print*,'fHOM(I):',fHOM(I)
C           print*,'CONST(6):',CONST(6)
           CALVALDBLE = DBLE(SAPRCGC(INDEX_VOC(I)))*1e-6*PRES/
     &      R/TEMP*6.022e23*ohc*1e-6
           dHOM = CALVALDBLE*kOH(I)*fHOM(I)*aadt
           HOM2 = HOM2 + dHOM
C           print*,'HOM2 in loop =',HOM2
         END DO
C         HOM = HOM*1e-6*PRES/R/TEMP*6.022E23
         HOM = HOM + HOM2*BOXVOL/6.022e23*300.0/1000.0  ! HOM in kg
         print*,'HOM at 989 = ',HOM
C         print*,'After Auto-ox'
C         OPEN(UNIT=48, FILE=HOM_FILE, STATUS='old', ACCESS='append')
C         WRITE(48,905) TOUT*60.0, HOM
C         CLOSE(48)


C------------------------------------------------          
C        ! get organic aerosol psats at current temperature
C         do j=1,iorg
C            psatorg(j)=pstar(j)*exp(Hvap(j)*1.d3*(1.d0/T1-1.d0/sfctemp)
C     &      /R)
C            CSTAR(j)=psatorg(j)/R/sfctemp*MWORG(j)*1.0e6
C         enddo

         do j=1,iorg
            psatorg(j)=pstar(j)*exp(Hvap(j)*1.d3*(1.d0/T1-1.d0/temp)/R)
            CSTAR(j)=psatorg(j)/R/temp*MWORG(j)*1.0e6
         enddo

CCCC  Dilution rate
C ----------------------------------------------------------
C         time_new = (time+tstep*aadt)/3600.
C         time_old = (time+(tstep-1)*aadt)/3600.
C         dilt_rate_new = 1.0 !p_dilt1*(time_new**3) +
C         dilt_rate_old = 1.0 !p_dilt1*(time_old**3) +
C         BOXVOL = initial_boxvol*dilt_rate_new
C         BOXVOL_old = initial_boxvol*dilt_rate_old

CCCCC Call Wall loss subroutine
C ----------------------------------------------------------------
C         call wallloss(ke, kw0, VWL, PWL,
C     &        Gc, Nk, Mk, aadt, time, P_temp, P_num,
C     &        WalVapMas, tau_w, kw_HYBRID, aadt) !for normal case
         call wallloss(kvap_on, kpar, VWL, PWL,
     &        Gc, Nk, Mk, 1, Temp, BOXVOL, time, aadt) ! mWSORB = 1 ? 

CCCCC add soa to gas phase
C ----------------------------------------------------------------         
         soarate = 0.0
         do j=1,iorg
            Gc(srtorg1+j-1)=Gc(srtorg1+j-1)
         enddo
         
         do k=1,ibins
            if (isnan(Nk(k)))then
               print*,'NaN 1'
               stop
            endif
            Nkout(k)=Nk(k)
            do j=1,icomp
               IF (ISNAN(Mk(k,j))) THEN
                 print*,'Mk NaN 1'
                 STOP
               ENDIF
               Mkout(k,j)=Mk(k,j)
            enddo
         enddo
        
         !print*,'Mk(1) =',Mk(1,:)
         !print*,'Nk(1) =',Nk(1)
CCCCC Coagulation
C ----------------------------------------------------------------         
         call storenm() 
         call multicoag(aadt)

         do k=1,ibins
            if (isnan(Nk(k)))then
               print*,'NaN 2'
               do n=1,ibins
                  print*,n,Nk(n),Nkout(n)
                  do j=1,icomp
                     print*,n,j,Mk(n,j),Mkout(n,j)
                  enddo
               enddo
               stop
            endif
         enddo

CCCCC Do water eqm at appropriate times
C ----------------------------------------------------------------         
         call eznh3eqm(Gc,Mk)
         call ezwatereqm(Mk,ORG_O2C,kappa_avg)

         do k=1,ibins
            if (isnan(Nk(k)))then
               print*,'NaN 3'
               stop
            endif
         enddo

CCCCC Nucleation
C ----------------------------------------------------------------         
         call storenm()
         call nucleation(Nk,Mk,Gc,Nkout,Mkout,Gcout,
     &        adt, fion, cstar_nuc, org_nuc, inorg_nuc, NH3MOLEC_CM3,
     &        MWORG, HOM) ! Orginally from JRP codes, SamO added NH3
         print*,'HOM at 1075 = ',HOM
         do k=1,ibins
            if (isnan(Nk(k)))then
               print*,'NaN 3'
               do n=1,ibins
                  print*,n,Nk(n),Nkout(n)
                  do j=1,icomp
                     print*,n,j,Mk(n,j),Mkout(n,j)
                  enddo
               enddo
               stop
            endif
         enddo

         do n=1,IBINS
            do j=1,icomp
               Mk(n,j)=Mkout(n,j)
            enddo
            Nk(n)=Nkout(n)
         enddo

C         print*,'Calling HOMCOND'
C ========================================================== 
         print*,'HOM before HOMCOND = ',HOM
         call HOMCOND(Nk,Mk,Nkout,Mkout,HOM,aadt,tau_p,
     &     Dbk,kc,ORG_O2C,kappa_avg)
         print*,'HOM after HOMCOND = ',HOM

C         print*,'Just after HOMCOND'
C ========================================================== Need to update for prognostic H2SO4
         GC(srtso4)=GCOUT(srtso4)
         GC(SRTORG1:SRTORGLAST) = GCOUT(SRTORG1:SRTORGLAST) ! Added by AliA - IS IT RIGHT???????
C ==========================================================         
C         print*,'Problem with GC'
         do k=1,ibins
            if (isnan(Nk(k)))then
               print*,'NaN 4'
               stop
            endif
         enddo
C         print*,'before ezwatereqm'
         call ezwatereqm(Mk,ORG_O2C,kappa_avg)
C         print*,'before eznh3eqm'
         call eznh3eqm(Gc,Mk)
         do k=1,ibins
            if (isnan(Nk(k)))then
               print*,'NaN 5'
               stop
            endif
         enddo

CCCCC Sulfate condensation
C ----------------------------------------------------------------
C         call storenm()
C         call getCondSink(Nk,Mk,srtso4,CS,sinkfrac)
C         OPEN(UNIT=45, FILE=CS_FILE, STATUS='old', ACCESS='append')
C         WRITE(45,905) TOUT*60.0, CS
C
C         massin=0.0 !sulfconc/6.022D23*0.098d0*boxvol*CS*aadt
C         massin = GC(srtso4)*CS*aadt
C         print*,'GC(srtso4) =',GC(srtso4)
C         GC(srtso4) = GC(srtso4) - massin
C         print*,'massin =',massin
C         print*,'CS =',CS
C         print*,'aadt =',aadt
C         call ezcond(Nk,Mk,massin,srtso4,Nkout,Mkout)
C         tmass1=massin
C         tmass2=0.d0
C         do n=1,IBINS
C            do j=1,icomp
C               tmass1=tmass1+Mk(n,j)
C               tmass2=tmass2+Mkout(n,j)
C               Mk(n,j)=Mkout(n,j)
C            enddo
C            Nk(n)=Nkout(n)
C         enddo
C         if((abs(tmass1-tmass2)/massin.gt.1.E-3).and.
C     &      (abs(massin/tmass1).gt.1.d-10)) then
C            print*,'ERROR IN BOX.f'
C            print*,'no conservation of mass in sulf cond'
C            print*,tmass1,tmass2
C            print*,massin
C            stop
C         endif
C
C         do k=1,ibins
C            if (isnan(Nk(k)))then
C               print*,'NaN 6'
C               stop
C            endif
C         enddo
C 
CCCCC SOA condensation
C ----------------------------------------------------------------
C         print*,'1136' 
         call storenm()

         CTRW = CTRW + 1

C ***********************
C End of aerosol dynamics
C ***********************

CCCCC Gas phase chemistry
C ----------------------------------------------------------------         
         IF (CTRW.GT.1) THEN

C --- Update SAPRC based on TOMAS gas-phase concentration of SO4 species ----------------------   
            CALVALDBLE = GC(SRTSO4) * 1.0E+6 / ! TOMAS gas-phase of SO4
     &           PRES * R * TEMP / 96.06 *
     &           1.0E+3 / BOXVOL * 1.0e+6 ! kg/bag -> g/m3 -> ppm
            SAPRCGC(SO4_INDX) = REAL(CALVALDBLE)

C --- Update SAPRC based on TOMAS gas-phase concentration of SOM species --------------------
            DO I=1,IORG-1
               CALVALDBLE = GC(I+SRTORG1-1) * 1.0E+6 / ! TOMAS gas-phase SOM
     &                      PRES * R * TEMP / MWORG(I) *
     &                      1.0E+3 / BOXVOL * 1.0e+6 ! kg/bag -> g/m3 -> ppm
               SAPRCGC(I-1+SOM_1STINDX) = REAL(CALVALDBLE)
            ENDDO
C --- Update gas concentrations of parent species to initial values  -----------------------
C            DO I=1,NSPEMISS
C               WHERE(SAPRC_SPNAME2==EMISS_SPNAME(I))
C                  SAPRCGC = EMISS_IPPM(I) ! saprc gas-phase
C               END WHERE
C            END DO
         END IF

         CTR = CTR + 1
         TOUT = REAL(time) + tstep*REAL(aadt)
         TIN = (TOUT - REAL(aadt))/60.0
         TOUT = TOUT/60.0
         NEQNT = NACT


         call INTEGR2(TIN,TOUT,NEQNT,SAPRCGC,DIFF,
     &        2.e-3, 1.0, 1.e-3, 0., 1.0E-30, 1.0e-09, 1, 5)

C --- Update gas concentrations of parent species to initial values  -----------------------
C         DO I=1,NSPEMISS
C            WHERE(SAPRC_SPNAME2==EMISS_SPNAME(I))
C               SAPRCGC = EMISS_IPPM(I) ! saprc gas-phase
C            END WHERE
C         END DO

C --- Update TOMAS based on SAPRC gas-phase concentration of SO4 species ----------------------
         CALVALREAL = SAPRCGC(SO4_INDX)*1.0E-6 * ! SAPRC gas-phase of SO4
     &        PRES/R/TEMP * 96.06 *
     &        1.0E-3 * BOXVOL * 1.0e-6 ! ppm -> g/m3 -> kg/bag
         GC(SRTSO4) = DBLE(CALVALREAL)
C --- Update TOMAS based on SAPRC gas-phase concentration of SOM species ----------------------
         DO I=1,IORG-1
            CALVALREAL = SAPRCGC(I-1+SOM_1STINDX)*1.0E-6 ! SAPRC gas-phase SOM
     &                   * PRES/R/TEMP * MWORG(I) *
     &                   1.0E-3 * BOXVOL * 1.0e-6 ! ppm -> g/m3 -> kg/bag
            GC(I+SRTORG1-1) = DBLE(CALVALREAL)
         ENDDO

C         print*,'Before Auto-ox'
C HOM formation 
C ----------------------------------------------------------------

C     AUTOXIDATION: CHARLES
C         dHOM = 0.0
C         print*,'INDEX_VOC =',INDEX_VOC
C         print*,'kOH =',kOH
C         DO I = 1,6
C             DEX = INDEX_VOC(i)
C           print*,'INDEX_VOC(I) =',INDEX_VOC(I)
C           print*,'SAPRCGC(INDEX_VOC(I)):',SAPRCGC(INDEX_VOC(I))
C           print*,'kOH(I):',kOH(I)
C           print*,'fHOM(I):',fHOM(I)
C           print*,'CONST(6):',CONST(6)
C           dHOM = SAPRCGC(INDEX_VOC(I))*kOH(I)
C     &      *fHOM(I)*CONST(6)
C           HOM = HOM + dHOM
C         END DO
C         HOM = HOM*1e-6*PRES/R/TEMP*6.022E23
C         HOM = HOM*1e-6*PRES/R/TEMP*300.0/1000.0  ! HOM in kg
C         print*,'After Auto-ox'

C         print*,'SAPRCGC(10:20) Before HOM =',SAPRCGC(10:20)
C         CALL STEP_AUTOOX(AutoFrac,CONST(6),time,aadt,SAPRCGC,
C     &        SOM_1STINDX)
C
C         print*,'SAPRCGC(10:20) After HOM =',SAPRCGC(10:20)
C Particle Phase Diffusion Coefficient 
C ----------------------------------------------------------------

C         Dbk = 1.0E-20
C         print*,'SAPRCGC(29) before =',SAPRCGC(29)
C         print*,'GC(iCOMP-4) before =',GC(iCOMP-4)
C         Dbk = CALC_DB(time,ORG_O2C)
C         print*,'Dbk =',Dbk 
C         print*,'SAPRCGC(29) after =',SAPRCGC(29)
C         print*,'GC(iCOMP-4) after =',GC(iCOMP-4)


CCCCC Sulfate condensation
C ----------------------------------------------------------------
         call storenm()
         call getCondSink(Nk,Mk,srtso4,CS,sinkfrac)
C         OPEN(UNIT=45, FILE=CS_FILE, STATUS='old', ACCESS='append')
C         WRITE(45,905) TOUT*60.0, CS

         massin=0.0 !sulfconc/6.022D23*0.098d0*boxvol*CS*aadt
         massin = GC(srtso4)*CS*aadt
         print*,'GC(srtso4) =',GC(srtso4)
         GC(srtso4) = GC(srtso4) - massin
         print*,'massin =',massin
         print*,'CS =',CS
         print*,'aadt =',aadt
         call ezcond(Nk,Mk,massin,srtso4,Nkout,Mkout)
         tmass1=massin
         tmass2=0.d0
         do n=1,IBINS
            do j=1,icomp
               tmass1=tmass1+Mk(n,j)
               tmass2=tmass2+Mkout(n,j)
               Mk(n,j)=Mkout(n,j)
            enddo
            Nk(n)=Nkout(n)
         enddo
         if((abs(tmass1-tmass2)/massin.gt.1.E-3).and.
     &      (abs(massin/tmass1).gt.1.d-10)) then
            print*,'ERROR IN BOX.f'
            print*,'no conservation of mass in sulf cond'
            print*,tmass1,tmass2
            print*,massin
            stop
         endif

         do k=1,ibins
            if (isnan(Nk(k)))then
               print*,'NaN 6'
               stop
            endif
         enddo

CCCCC SOA condensation
C ----------------------------------------------------------------
         call soacond(Nk,Mk,Gc,Nkout,Mkout,Gcout,aadt,tau_p,Dbk,kc,
     &                  ORG_O2C,kappa_avg)
         
         totamass=0.d0
         print*, 'totalae =',SUM(Mk(:,SRTORG1:SRTORGLAST))/boxvol*1e15
         print*, 'totalgs =',SUM(Gc(SRTORG1:SRTORGLAST))/boxvol*1e15
         print*, 'ae + gs =',SUM(Mk(:,SRTORG1:SRTORGLAST))/boxvol*1e15+
     &   SUM(Gc(SRTORG1:SRTORGLAST))/boxvol*1e15
         do n=1,IBINS
            do j=1,icomp
               Mk(n,j)=Mkout(n,j)
            enddo
            Nk(n)=Nkout(n)
         enddo

         do j=1,icomp-idiag
            Gc(j)=Gcout(j)
         enddo
         
         do k=1,ibins
            if (isnan(Nk(k)))then
               print*,'NaN 7'
               stop
            endif
         enddo
         call eznh3eqm(Gc,Mk)
         call ezwatereqm(Mk,ORG_O2C,kappa_avg)
         call mnfix(Nk,Mk)

         do k=1,ibins
            if (isnan(Nk(k)))then
               print*,'NaN 8'
               stop
            endif
         enddo

         DO N=1,IBINS
            IF (Nk(N) .LT. 1d-60) THEN
               Nk(N) = 0.d0
            ENDIF
            DO J=1,ICOMP
               IF (Mk(N,J) .LT. 1d-60) THEN
                  Mk(N,J) = 0.d0
               ENDIF
            ENDDO
         ENDDO
            
         DO I=1,ICOMP-1
            IF (GC(I) .LT. 1d-60) THEN
               GC(I) = 0.d0
            ENDIF
         ENDDO
         DO I=1,NACT
            IF (SAPRCGC(I) .LT. 1d-60) THEN
               SAPRCGC(I) = 0.d0
            ENDIF
         ENDDO

      DO N=1,IBINS
         IF (Nk(N) .LT. 1d-60) THEN
            Nk(N) = 0.d0
         END IF
         DO J=1,ICOMP
            IF (Mk(N,J) .LT. 1d-60) THEN
               Mk(N,J) = 0.d0
            END IF
         ENDDO
      ENDDO

      DO I=1,ICOMP-1
         IF (GC(I) .LT. 1d-60) THEN
            GC(I) = 0.d0
         END IF
      ENDDO

      call report(time)
      totmass = 0.0
      do n=1,ibins
        totmass=totmass+Nk(n)*sqrt(xk(n)*xk(n+1))
      enddo
      print*,'Total mass =',totmass*1.0e9/boxvol*1.0e6
C      Mk_lay(:,:,v) = Mk
C      Nk_lay(:,v) = Nk
C      Gc_lay(:,v) = Gc
C      SAPRCGC_lay(:,v) = SAPRCGC
C      cstar_lay(:,v) = CSTAR(:)
C      mworg_lay(:,v) = mworg(:)
C      Hvap_lay(:,v) = Hvap(:)
C      HOM_lay(v) = HOM
      OPEN(UNIT=38, FILE=SAPRCGCFILE, STATUS='old',ACCESS='APPEND')      
      WRITE(38,999) SAPRCGC(1:NACT)
      CLOSE(38)

 4    FORMAT(41E15.6)
      OPEN(UNIT=46, FILE=Kappa_FILE, STATUS='old',ACCESS='APPEND')      
      WRITE(46,4) time/3600.,(kappa_avg(K),K=1,IBINS)
      CLOSE(46)
      ENDDO
C      ENDDO

C Vertical Diffusion 
C====================================================================

C      print*,'Calling layer_diff'
C      call layer_diff(KZ,nlayers,temp_lay,pres_lay,
C     & Nk_lay, Mk_lay, aadt, icomp, ibins)
C
C      print*,'Finished calling layer_diff'
C      Nk_lay = Nk_lay_o
C      Mk_lay = Mk_lay_o


C      OPEN(UNIT = 42, FILE = '../../inputs/'// runname(1:8)
C     & //'_PBL_Height',STATUS = 'old')
C      DO I=1,INT(endtime*360)
C        READ(42,100) PBL(I)
C      ENDDO 
C      CLOSE(UNIT=42)

C Calculate layer center heights and edges
C--------------------------------------------------------
C      Z_lay(1) = (287.0*temp_lay(1)/9.8 * 
C     & log(lay_edge(1)/lay_edge(2)))*0.5 
C
C      DO I=1,nlayers-1
C        Z_lay(I+1) = Z_lay(I) + (287.0*temp_lay(I)/9.8 * 
C     &  log(lay_edge(I)/lay_edge(I+1)))*0.5 + 
C     &  (287.0*temp_lay(I+1)/9.8 * log(lay_edge(I+1)/lay_edge(I+2)))*
C     &  0.5
C      ENDDO
C Set KZ values based on PBL height
C--------------------------------------------------------
C      DO v=1,nlayers 
C        IF (Z_lay(v).ge.PBL(INT(TOUT*60/aadt))) THEN
C          KZ_lay(v) = 0.d0
CC          O3_lay(v) = 0.055
C        ELSE 
C          KZ_lay(v) = KZ
CC          O3_lay(v) = 0.040
C        ENDIF
C      ENDDO
C
C      print*,'PBL Height =',PBL(INT(TOUT*60/aadt))
C      print*,'KZ_lay =',KZ_lay
C      print*,'Gc_lay(13,1)=',Gc_lay(13,1) 

C Now the mixing routine
C--------------------------------------------------------

C      DO v=1,nlayers-1
C        print*,'v =',v
C        print*,'looping through bins:'
C        IF (dz*v.ge.PBL(INT(TOUT*60/10))) THEN

C Convert box volumes to STP
C--------------------------------------------------------
C        V1 = (pres_lay(v)*boxvol/10000000.0*sfctemp)/
C     &    (temp_lay(v)*sfcpres)
C        V2 = (pres_lay(v+1)*boxvol/10000000.0*sfctemp)/
C     &    (temp_lay(v+1)*sfcpres)
C        print*,'V1 =',V1,'V2 =',V2
CC Vertical mixing of gas-phase species
CC--------------------------------------------------------
C        DO I=1,icomp-1
C          Jdiff = KZ_lay(v)*((Gc_lay(I,v)/V1)-(Gc_lay(I,v+1)/V2))/
C     &      (Z_lay(v+1)-Z_lay(v))
C          dCdt = Jdiff/(Z_lay(v+1)-Z_lay(v))
C          Gc_lay(I,v) = Gc_lay(I,v)-dCdt !*aadt
C          Gc_lay(I,v+1) = Gc_lay(I,v+1)+dCdt !*aadt
C        ENDDO
C
CC       SAPRC VOCs        
C        DO II=1,6
C          I = INDEX_VOC(II)
C          Jdiff = KZ_lay(v)*((SAPRCGC_lay(I,v))-(SAPRCGC_lay(I,v+1)))/
C     &      (Z_lay(v+1)-Z_lay(v))
C          dCdt = Jdiff/(Z_lay(v+1)-Z_lay(v))
C          SAPRCGC_lay(I,v) = SAPRCGC_lay(I,v)-dCdt !*aadt
C          SAPRCGC_lay(I,v+1) = SAPRCGC_lay(I,v+1)+dCdt !*aadt
C        ENDDO
C
CC       SO2
C        I = SO2_INDX
C        Jdiff = KZ_lay(v)*((SAPRCGC_lay(I,v))-(SAPRCGC_lay(I,v+1)))/
C     &    (Z_lay(v+1)-Z_lay(v))
C        dCdt = Jdiff/(Z_lay(v+1)-Z_lay(v))
C        SAPRCGC_lay(I,v) = SAPRCGC_lay(I,v)-dCdt !*aadt
C        SAPRCGC_lay(I,v+1) = SAPRCGC_lay(I,v+1)+dCdt !*aadt
C
CC       SULF 
C        I = SO4_INDX
C        Jdiff = KZ_lay(v)*((SAPRCGC_lay(I,v))-(SAPRCGC_lay(I,v+1)))/
C     &    (Z_lay(v+1)-Z_lay(v))
C        dCdt = Jdiff/(Z_lay(v+1)-Z_lay(v))
C        SAPRCGC_lay(I,v) = SAPRCGC_lay(I,v)-dCdt !*aadt
C        SAPRCGC_lay(I,v+1) = SAPRCGC_lay(I,v+1)+dCdt !*aadt
CC HOM mixing
CC--------------------------------------------------------
C        Jdiff = KZ_lay(v)*((HOM_lay(v)/V1)-(HOM_lay(v+1)/V2))/
C     &      (Z_lay(v+1)-Z_lay(v))
C        dCdt = Jdiff/(Z_lay(v+1)-Z_lay(v))
C        HOM_lay(v) = HOM_lay(v)-dCdt !*aadt
C        HOM_lay(v+1) = HOM_lay(v+1)+dCdt !*aadt
C        
CC Vertical mixing based on aerosol number concentration 
CC--------------------------------------------------------
C        DO n=1,ibins
CC          print*,'bin =',n
CC          print*,'KZ_lay(v) =',KZ_lay(v)
C          Jdiff = KZ_lay(v)*((Nk_lay(n,v)/V1)-(Nk_lay(n,v+1)/V2))/
C     &    (Z_lay(v+1)-Z_lay(v))
CC          print*,'KZ_lay(v) =',KZ_lay(v)
CC          print*,'DiffConc =',Nk_lay(n,v)-Nk_lay(n,v+1)
CC          print*,'Jdiff =',Jdiff
CC          print*,'Bin number =',n 
CC          print*,'Number of particles moving =',dCdt*aadt
C          dCdt = Jdiff/(Z_lay(v+1)-Z_lay(v))
CC          print*,'dCdt =',dCdt
C          Nk_lay(n,v) = Nk_lay(n,v)-dCdt
C          Nk_lay(n,v+1) = Nk_lay(n,v+1)+dCdt
C          delmass = 0.d0
CC Now we take the appropriate amount from Mk
CC--------------------------------------------------------
C          IF (Jdiff.gt.0.d0) THEN
C            ratio = ABS(dCdt/Nk_lay(n,v))
C            DO I=1,icomp
C              delmass = delmass+Mk_lay(n,I,v)*ratio
C              Mk_lay(n,I,v) = Mk_lay(n,I,v)-Mk_lay(n,I,v)*ratio
C              Mk_lay(n,I,v+1) = Mk_lay(n,I,v+1)+Mk_lay(n,I,v)*ratio
C            ENDDO
C          ELSEIF(Jdiff.lt.0.d0) THEN
C            ratio = ABS(dCdt/Nk_lay(n,v+1))
C            DO I=1,icomp
C              delmass = delmass+Mk_lay(n,I,v+1)*ratio
C              Mk_lay(n,I,v+1)=Mk_lay(n,I,v+1)-Mk_lay(n,I,v+1)*ratio
C              Mk_lay(n,I,v) = Mk_lay(n,I,v) + Mk_lay(n,I,v+1)*ratio
C            ENDDO
C          ENDIF
CC          print*,'Mass moving =',delmass
CC          print*,'M/N moving =',delmass/(dCdt*aadt)
CC          print*,'ratio =',ratio
CC          ELSEIF(Jdiff.eq.0.d0) THEN
CC            ratio = 0.d0
CC          ENDIF
CC          Nk_lay(n,v) = Nk_lay(n,v)-dCdt*aadt
CC          Nk_lay(n,v+1) = Nk_lay(n,v+1)+dCdt*aadt
C        ENDDO
C      ENDDO
C  
C
C      print*,'Just finished vert. diff.'
C      do v=1,nlayers
       do k=1,ibins
          if (isnan(Nk(k)))then
             print*,'NaN 9'
             do n=1,ibins
                print*,n,Nk(n)
             enddo
             stop
          endif
       enddo
C      enddo

C====================================================================      
C End of time step
      time=time+adt
      hour=time/3600.d0

      if (hour .lt. endtime) goto 10

      CLOSE(UNIT=39)
      CLOSE(UNIT=43)
      CLOSE(UNIT=44)
      CLOSE(UNIT=45)
      CLOSE(UNIT=47)
      CLOSE(UNIT=49)
      CLOSE(UNIT=50) 
C      do v=1,nlayers
      totmass = 0.0

      do n=1,ibins
         totmass=totmass+Nk(N)*sqrt(xk(n)*xk(n+1))
      enddo
      print*,'totmass [ug m-3]', totmass*1.0e9/boxvol*1.0e6
      print*,'Nk=',Nk(:)

      END   !of main


