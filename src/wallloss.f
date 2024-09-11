!     =========================================================================================
!                   THIS SUBROUTINE STEPS FORWARD FOR PARTICLE AND VAPOR WALL LOSS
!     =========================================================================================

      SUBROUTINE STEP_WALLLOSS(kvap_on,kpar,VWL,PWL,Gci,Nki,Mki,
     & mWSORB,Tempi,time,dt,Csat_Ref2)

      IMPLICIT NONE
C      USE hTOMAS; IMPLICIT NONE
      include 'sizecode.COM'

!     DECLARATIONS:
!     =========================================================================================
      DOUBLE PRECISION Nki(ibins), Mki(ibins, icomp), Gci(icomp-1)
C      REAL(8) :: Gc_WALL(iCOMP-1)
C      REAL(8) :: Nk_WALL(iBINS)
C      REAL(8) :: Mk_WALL(iBINS,iCOMP)
      DOUBLE PRECISION kvap_on             ! [s-1]         Gas-phase wall loss rate
      INTEGER VWL                            !               Switch for vapor wall loss
      INTEGER PWL                            !               Switch for particle wall loss
      INTEGER mWSORB
C      DOUBLE PRECISION Temp                  ! [K]           Chamber temperature
C      DOUBLE PRECISION BoxVol                ! [cm3]         Chamber volume
      DOUBLE PRECISION time
      DOUBLE PRECISION dt                    ! [s]           Total timestep
      
C      REAL(8) :: kpar(iBINS)
      DOUBLE PRECISION :: kpar(iBINS)
      
      INTEGER nsteps                         !               Number of microphysical timesteps
      PARAMETER(nsteps = 10)
      
      DOUBLE PRECISION R
      PARAMETER(R = 8.314)

      DOUBLE PRECISION PI
      PARAMETER(PI = 3.1415926)

      DOUBLE PRECISION rho_org
      DOUBLE PRECISION rho_ams
      PARAMETER(rho_org = 1400.0)            ! [kg m-3]      Density of the aerosols
      PARAMETER(rho_ams = 1770.0)            ! [kg m-3]      Density of the seeds
      
      INTEGER i,j,k
      
      DOUBLE PRECISION mdt                   ! [s]           Microphysical timestep for vapor wall loss
      DOUBLE PRECISION Dl,Dh,Dp              ! [nm]          Bins bounds and center size

      DOUBLE PRECISION kw_par(IBINS)         ! [s-1]         Particle wall loss rate
      DOUBLE PRECISION kw_gas(iorg)          ! [s-1]         Vapor wall loss rate
      DOUBLE PRECISION kw_gas_off(iorg)      ! [s-1]         Vapor evaporating rate
      DOUBLE PRECISION wlc(iorg)             ! [ug m-3]      Saturation vapor concentration of species on the wall
      
      DOUBLE PRECISION Gas_temp(iorg,nsteps) !               Temporary array
      DOUBLE PRECISION Wal_temp(iorg,nsteps) !               Temporary array
      DOUBLE PRECISION h2so4_temp(nsteps)    ! SamO added for non-reversible wall loss of h2so4
      
C      DOUBLE PRECISION cstar(IORG)           ! [ug m-3]      Saturation vapor pressure

      DOUBLE PRECISION dn,dm

      DOUBLE PRECISION Csat_Ref2(iorg)
      DOUBLE PRECISION TEMPi

!     PARTICLE WALL LOSS FOR NUMBER CONCENTRATION:
!     =========================================================================================
      
      DO 500 i = 1,iBINS
         IF (Nki(i).LT.1.0) GOTO 500
         
         IF (PWL.EQ.1) THEN
            dn = Nki(i)*(1.0 - EXP(-dt*kpar(i)))
         ELSE
            dn = 0.0
         END IF

         Nki(i) = Nki(i) - dn
         
         Nk_WALL(i) = Nk_WALL(i) + dn
 500  CONTINUE
      
!     PARTICLE WALL LOSS FOR MASS CONCENTRATION:
!     =========================================================================================
      DO 501 i = 1,iBINS
         IF (Nki(i).LT.1.0) GOTO 501
         DO j = 1,iCOMP
            
            IF (PWL.EQ.1) THEN
               dm = Mki(i,j)*(1.0 - EXP(-dt*kpar(i)))
            ELSE
               dm = 0.0
            END IF

            Mki(i,j) = Mki(i,j) - dm
            
            Mk_WALL(i,j) = Mk_WALL(i,j) + dm
         END DO
 501  CONTINUE
      
!     VAPOR WALL LOSS FOR GAS-PHASE SPECIES:
!     =========================================================================================      
!     WALL EQUIVALENT OA (Krechmer et al., 2016):
      DO i = 1,iORG
         
         cstar(i) = Csat_Ref2(i) * (298.0/TEMPi) * 
     &              EXP(Hvap(i)*1.0D3*(1.0D0/298.0-1.0D0/TEMPi)/R)
         
         IF (cstar(i).GT.1.0e4) THEN
            wlc(i) = 10.0e3            
         ELSE IF ((cstar(i).LT.1.0e4).AND.(cstar(i).GT.1.0)) THEN
            wlc(i) = 16.0*(cstar(i)**0.6)
         ELSE
            wlc(i) = 16.0
         END IF
         
      END DO


      IF (mWSORB.EQ.0) THEN
         WLC(:) = SUM(Gc_wall)*1e9/BoxVol*1e6
      
         DO i = 1,iORG
            IF (WLC(i).LT.1e-6) WLC(i) = 1e-6
         END DO
      END IF

!     VAPOR WALL LOSS AND REVERSE RATES:
      DO i = 1,iorg

         IF (VWL.EQ.1) THEN
            kw_gas(i) = kvap_on
         ELSE
            kw_gas(i) = 0.0
         END IF

         kw_gas_off(i) = kw_gas(i) * cstar(i) / wlc(i)!

      END DO

      ! Vapor wall loss for gas-phase species and the wall:
      mdt = dt/DBLE(nsteps)

      ! Create temporary arrays:
      DO i = 1,iorg
         Gas_temp(i,1) = Gci(i+1)
         Wal_temp(i,1) = Gc_wall(i+1) !SamO
      END DO

      ! Integrate:
      DO i = 2,nsteps
         DO j = 1,iorg
            
            Gas_temp(j,i) = Gas_temp(j,i-1)*exp(-kw_gas(j)*mdt) + 
     & Wal_temp(j,i-1)*(1-exp(-kw_gas_off(j)*mdt))
            
            Wal_temp(j,i) = Wal_temp(j,i-1)*exp(-kw_gas_off(j)*mdt) + 
     &  Gas_temp(j,i-1)*(1-exp(-kw_gas(j)*mdt))
            
         END DO
      END DO

! H2SO4 wall loss - SamO
!---------------------------------------
      IF (VWL.EQ.1) THEN
        h2so4_temp(1) = Gci(1) ! SamO initialize sulfuric acid 
        DO i = 2,nsteps
          h2so4_temp(i) = h2so4_temp(i-1)*exp(-kvap_on*mdt)
        END DO
        GC_wall(1) = GC_wall(1) + Gci(1) - h2so4_temp(nsteps)
        Gci(1) = h2so4_temp(nsteps)  ! SamO - update Gci array
      ENDIF
!---------------------------------------

      ! Update gas concentration and wall mass concentration:
      DO i = 1,iorg
         Gci(i+1) = Gas_temp(i,nsteps)
         
         IF (Wal_temp(i,nsteps).LT.1e-30) THEN
            Gc_wall(i+1) = 0.0
         ELSE
           Gc_wall(i+1) = Wal_temp(i,nsteps)
         END IF
         
      END DO

      RETURN

      END SUBROUTINE STEP_WALLLOSS
