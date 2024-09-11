C ==============================================================================
C This function calculates the aerosol bulk diffusivity based on its composition
C (monomers, dimers and water).
C ==============================================================================

      DOUBLE PRECISION FUNCTION CALC_DB(timer,ORG_O2C2)

      IMPLICIT NONE
      
C      INCLUDE "../headers/h_tomas_arrays.f"
      INCLUDE 'sizecode.COM'
      INCLUDE 'modlspc.h'
C      INCLUDE 'common.inc'
      INCLUDE 'gaskin.h'

      DOUBLE PRECISION ofrac
C      DOUBLE PRECISION Temp            ! [K]  Temperature
C      DOUBLE PRECISION Pres            ! [Pa] Pressure
C      DOUBLE PRECISION RH              !      Relative humidity
      DOUBLE PRECISION ORG_O2C2(iORG)
      DOUBLE PRECISION timer
      
      DOUBLE PRECISION Mass_Org          ! [kg] Total mass of organics (monomers + dimers)
      DOUBLE PRECISION Frac_Orgs(iORG+1)!(iORG) !      Fraction of each organic species
      DOUBLE PRECISION Frac_Orgs2(iORG)
      
      DOUBLE PRECISION Tg_Orgs(iORG+1) !(iORG)   ! [K]  Glass-transition temperature of each organic species
      DOUBLE PRECISION Tg_Org           ! [K]  Ave. glass-transition temperature of total organics
      DOUBLE PRECISION Tg               ! [K]  Ave. glass-transition temperature of organics and water

      DOUBLE PRECISION Mass_W          ! [kg] Mass of water
      DOUBLE PRECISION Frac_W          !      Fraction of water

      DOUBLE PRECISION eta             ! [Pa s] Aerosol viscosity at current temperature
      DOUBLE PRECISION eta_0           ! [Pa s] Aerosol viscosity at infinite temperature
      DOUBLE PRECISION eta_c           ! [Pa s] Crossover viscosity (Evoy et al., 2019)
      PARAMETER(eta_0 = 1e-5)
      PARAMETER(eta_c = 1e-3)         

      DOUBLE PRECISION zeta            !        Correction factor (Evoy et al., 2019)
      PARAMETER(zeta = 0.93)

      DOUBLE PRECISION MW_ave          ! [g mol-1] Ave. MW of the condensing species weighted by mass
      DOUBLE PRECISION d_mo            ! [m]       Ave. diameter of condensing molecules
      DOUBLE PRECISION Cc              !           Slip-correction factor

      DOUBLE PRECISION MW_ave2
      
      DOUBLE PRECISION PI
      PARAMETER(PI = 3.1415926)

      DOUBLE PRECISION Na              ! [mol-1] Avogadro constant
      PARAMETER(Na = 6.022e23)
      
      DOUBLE PRECISION kB              ! [m2 kg s-2 K-1] Boltzmann constant
      PARAMETER(kB = 1.38e-23)    

      DOUBLE PRECISION k_GT            ! Gordon-Taylor constant (Shiraiwa, 2017)
      PARAMETER(k_GT = 2.5)

      DOUBLE PRECISION Tg_w            ! [K] Glass-transition temperature of water
      PARAMETER(Tg_w = 136.0)
      
      DOUBLE PRECISION D_frag          ! Fragility of aerosol liquid
      PARAMETER(D_frag = 10.0)

      DOUBLE PRECISION rho_org
      PARAMETER(rho_org = 1400.0)      ! [kg m-3] Density of organic aerosol

      DOUBLE PRECISION rho_w           ! [kg m-3] Density of water
      PARAMETER(rho_w = 1000.0)
      
      DOUBLE PRECISION beta            ! Ratio of Tg to To (Angell, 1995)
      PARAMETER(beta = 0.7966)

      DOUBLE PRECISION mfp             ! [m] Mean free path of air molecules
      PARAMETER(mfp = 66e-9)           

      DOUBLE PRECISION kappa           ! Kappa value of the organics
      PARAMETER(kappa = 0.1)
      
      DOUBLE PRECISION A,B,C,D,E       ! Parameterizations of glass-transition temperature model (Shiraiwa et al., 2017)
      PARAMETER(A = -21.57)
      PARAMETER(B = 1.51)
      PARAMETER(C = -1.7E-3)
      PARAMETER(D = 131.4)
      PARAMETER(E = -0.25)
      
      INTEGER i,j                      ! Loop counters

      DOUBLE PRECISION Mass_HOMS
      DOUBLE PRECISION Mass_LESS

      COMMON /TG_OUT/ Tg

      DOUBLE PRECISION MW_DIME
C      PARAMETER(MW_DIME=400.)

      DOUBLE PRECISION O2C_DIME
C      PARAMETER(O2C_DIME=0.4)
      
C     SKIPPING CRITERIA:
C     ==========================================================================      
      Mass_ORG = SUM(Mk(:,SRTORG1:SRTORGLAST))
C      print*,'ORG_O2C in f_calc =',ORG_O2C2
C      print*,'Mass_ORG =',Mass_ORG 
C      print*,'Temp =',Temp
C      print*,'Pres =',Pres
C      print*,'RH =',RH
C      print*,'iORG =',iORG
C      print*,'SRTORGLAST =',SRTORGLAST
C      print*,'MWORG(SRTORGLAST)=',MWORG(SRTORGLAST)
C      Mass_HOMS = SUM(Mk(:,xHOMS))
C      Mass_LESS = SUM(Mk(:,xORG_1ST:xHOMS-1))

C      IF (timer.EQ.0.) THEN !1600. !1800.
C         CALC_DB = 6e-24 !3.4e-19 !1e-19 !3.4e-19
C         GOTO 100
C      END IF

      
C      IF (MASS_ORG*1e9/(BoxVol*1e-6).LT.5.0) THEN !1.0
C         CALC_DB = 1e-17 !1e-19 !3.4e-19
C         GOTO 100
C      END IF
      
      IF (timer.LT.1800.) THEN !1600. !1800.
         CALC_DB = 1e-18 !3.4e-19 !1e-19 !3.4e-19
         GOTO 100
      END IF
      
C      IF (MASS_LESS.LT.MASS_HOMS) THEN
C         CALC_DB = 1e-20
C         GOTO 100
C      END IF
      
C     CALCULATE AVE. GLASS-TRANSITION TEMPERATURE OF THE ORGANICS:
C     ==========================================================================
C     GLASS-TRANSITION TEMPERATURE OF EACH SPECIES:
      DO i = 1,iORG !iORG
         !print*,ORG_O2C2(I)
         Tg_Orgs(i) = A + B*MWORG(i) + C*(MWORG(i)**2.) +D*ORG_O2C2(i)+ 
     &                E*MWORG(i)*ORG_O2C2(i)
         !print*,'Tg_Orgs(I)',Tg_Orgs(I)
C         print*,I,MWORG(I),ORG_O2C2(I),Tg_orgs(I)
      END DO
C      print*,'SUM(Tg_Orgs)=',SUM(Tg_Orgs)

C Sam Commented this 
C      MW_DIME = 0.0
C
C      DO i = 1,iORG
C         MW_DIME = MW_DIME + MWORG(i)*SUM(Mk(:,xDIME_1ST+i-1))/
C     &                                SUM(Mk(:,xDIME_1ST:xORG_LST))*2.
C      END DO


C      O2C_DIME = 0.0
C
C      DO i = 1,iORG
C         O2C_DIME = O2C_DIME + ORG_O2C(i)*SUM(Mk(:,xDIME_1ST+i-1))/
C     &                                SUM(Mk(:,xDIME_1ST:xORG_LST))
C      END DO

C      PRINT*, O2C_DIME
C Sam Commented this 
      
C      Tg_Orgs(SRTORGLAST) = A + B*300.0 + C*(300.0**2.) + D*1.5 + 
C     &                   E*300.0*1.5

C      PRINT*,'Tg_Orgs =', Tg_Orgs
C      STOP
      
C      PRINT*, ORG_MW(iORG-2)
C      STOP
      
C      PRINT*, Tg_Orgs
C      STOP
      
C     MASS FRACTION OF EACH MONOMER:
      DO i = 1,iORG !iORG
C         Frac_Orgs(i) = SUM(Mk(:,xORG_1ST+i-1))/(Mass_ORG-Mass_HOMS)
         Frac_Orgs(i) = SUM(Mk(:,SRTORG1+i-1))/(Mass_ORG)
      END DO

C      Frac_Orgs(SRTORGLAST) = SUM(Mk(:,SRTORGLAST))/Mass_ORG

C      PRINT*,'Frac_orgs =', Frac_Orgs
C      PRINT*, SUM(Frac_Orgs)
C      STOP
      
C     AVE. GLASS-TRANSITION TEMPERATURE:
      Tg_Org = 0.0
      
      DO i = 1,iORG!iORG
C         IF (i.EQ.iORG-2) THEN
C            CONTINUE
C            print*,Tg_Orgs(i),Frac_Orgs(i),I
            Tg_Org = Tg_Org + Tg_Orgs(i)*Frac_Orgs(i)
C         ELSE
C            Tg_Org = Tg_Org + Tg_Orgs(i)*Frac_Orgs(i)
C         END IF
      END DO

C      print*,'SUM(Frac_Orgs)=',SUM(Frac_Orgs)
C      PRINT*,'Tg_Org=', Tg_Org
C      STOP
      
C     NOW ACCOUNT FOR WATER CONTENT IN THE AEROSOL PHASE:
C     ==========================================================================      
C     MASS FRACTION OF WATER:      
      Mass_W = Mass_Org*(rho_w/rho_org)*(kappa/(1.0/RH - 1.0))
      Frac_W = Mass_W/(Mass_W + Mass_Org)
C      print*,'Frac_W=',Frac_W
      
C     OVERALL EFFECTIVE GLASS-TRANSITION TEMPERATURE:
      Tg = (Frac_W*Tg_W + (1./K_GT)*(1. - Frac_W)*Tg_Org) /
     &     (Frac_W + (1./K_GT)*(1. - Frac_W))
C      print*,'Tg =',Tg

C === CALCULATE BULK DIFFUSIVITY ===============================================
C     AVE. MOLECULAR WEIGHT OF THE CONDENSING SPECIES:
      MW_ave = 0.0
      MW_ave2 = 0.0
      
      DO i = 1,iORG !iORG-2
         MW_ave =MW_ave + MWORG(i)*Frac_Orgs(i)/
     &     (1.-Frac_Orgs(IORG))
      END DO

      DO i = 1,iORG !iORG
         MW_ave2 = MW_ave2 + MWORG(i)*Frac_Orgs(i)
      END DO

C     CALCULATE FRAGILITY
C     BASED ON DERIEUX ET AL., 2018:
C      D_frag = 10.3 + 602.6/MW_ave2

C      PRINT*, 'MW_ave =',MW_ave2,'D_frag = ',D_frag
       
C     CALCULATE AEROSOL VISCOSITY AT CURRENT TEMPERATURE:
      eta = eta_0*EXP(D_frag*beta/((Temp/Tg) - beta))
C      print*,'eta =',eta

      IF (eta.GT.1e12) eta = 1e12
      
C     AVE. DIAMETER OF THE CONDENSING MOLECULES:
      d_mo = ((6./PI)*(MW_ave2/1000.)/(rho_org*Na))**(1./3.)
C      print*,'d_mo =',d_mo

C     BULK DIFFUSIVITY:
      CALC_DB = kB*Temp/(6.*PI*d_mo*eta_c)*(eta_c/eta)**(zeta)

C      PRINT*, 'Db = ',CALC_DB
C      STOP
      
 100  RETURN
      END FUNCTION
