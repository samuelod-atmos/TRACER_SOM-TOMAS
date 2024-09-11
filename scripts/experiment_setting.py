import numpy as np
ibins = 40


def get_settings(experiment_name):

    # Calculate a few things 
    xk = np.zeros(ibins+1) 
    xk[0]=1E-21*2**-10 
    for k in range(1,ibins+1):
       xk[k] = xk[k-1]*2.
    pdens=1400. # fixed density for simplicity
    xkm=np.sqrt(xk[:-1]*xk[1:])
    Dp=((6.*xkm/pdens/np.pi)**(1.0/3.0))*1E9 # [m] average particle diameter of bin

    k_par = ''
    #for i in range(len(Dp)):
    #  if i < 11:
    #    print('Dp[i]=',Dp[i])
    #    kpar = kpar + str(A/Dp[11])+' '
    #  else:
      #print(Dp[np.where(Dp>20.)[0][0]])
      #sys.exit()
      #kpar = kpar + str(float(0.00001440))+' '
      # Use this -----------------
      #if Dp[i] < 30:
      #  kpar = kpar + str(A/Dp[np.where(Dp>30)[0][0]])+' '
      #elif Dp[i]>1000:
      #  kpar = kpar + str(A/Dp[np.where(Dp>1000)[0][0]])+' '
      #else:
      #  kpar = kpar + str(A/Dp[i])+' '
      #---------------------------
      #kpar = kpar + str(9.108699918785293e-06)+' '

    experiments = {
        # ---------------------- MAIN SIMULATIONS ---------------------------
        # this simulation is run without trimethylbenzene 
        
        "0_tmb": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
            
            },

        # This is where 1% of HOMs contribute to nucleation - need to change this in source code and compile
        "01HOM": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 7.2e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            "kvap_on": 2.50000e-03, # vapor wall loss coefficient 
            
            },

        # doubling of ammonia to 10000 ppt
        "2xnh3": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [10000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 7.2e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            "kvap_on": 2.50000e-03, # vapor wall loss coefficient 
            
            },
        
        # kvap_on set to kpar for smallest particles
        "sulfW": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 7.2e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            "kvap_on": 7.2e-3/Dp[np.where(Dp>30)[0][0]], # vapor wall loss coefficient 
           
            },
        
        # 10% of HOMs to nuc, and trimethylbenzene included
        "oldbs": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 7.2e-4,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            "kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        # 10% of HOMs to nuc, and trimethylbenzene included
        "base?": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        
        # same as base? but with slower pwl
        "A7e-5": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 7.2e-5,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            "kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        # same as base? but with slower pwl
        "A7e-6": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 7.2e-6,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            "kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        
        # same as base? but with slower pwl
        "A7e-7": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 7.2e-7,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            "kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        # same as HOM.3 but OH smoohted
        "smtOH": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            "kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        # vapor wall losses off
        "vwl_0": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 0,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 7.2e-4,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        # kvap_on consistent with particles 
        "Fkpar": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 4.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        # kvap_on consistent with particles 
        "A1e-2": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-2,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
            },


        # kvap_on consistent with particles 
        "A8e-3": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 8.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        # kvap_on consistent with particles 
        "A6e-3": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 6.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        # kvap_on consistent with particles 
        "A4e-3": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 4.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        # Test for scaling injections
        "injec": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        # same as injec but number multiplied by 100x
        "inx10": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        
        # same as injec but number multiplied by 1000
        "x1000": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },


        # A=2e-3 but only 1% of HOMS to nucleation 
        "01HOM": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        
        # TMB going into XYLSOMG
        "tmbxy": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
    

        # Same as tmbxy but with styrene going to tolsomg
        "styre": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        
        # Styrene included but TMB going to bensomg
        "styon": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        
        # same as tmbto but SOM species can't mix out
        "sommx": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        

        # same as sommx but with slower wall losses
        "mxout": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        # Same as styre but a 0.1 scalar on SOM species mixing out
        "styr2": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        

        # Same as styre but a 0.8 scalar on SOM species mixing out
        "styr3": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        # styrene included and TMB going to TOLSOMG instead of XYLSOMG
        "tmbto": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        
   
        # No styrene and TMB still going to BNZSOMG, but TOL and XYL som grids have been expanded
        "nwgrd": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        
   
        # This is the same as tmbto except there is no styrene included
        "tmbt2": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        # same as tmbto but with no HOMs
        "noHOM": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        
        # HOM yields divided by 3. 
        "HOM.3": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },



        # same as tmbto but with PTR-MS NaNs replaced with 0.0
        "nan_0": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },


        # no instruments pulling and vwl and pwl off
        "nopul": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 0,             # vapor wall loss switch
            "pwl": 0,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        
        # same as tmbto but with new homcond and HOMs mixing out
        "HOMmx": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },


        # This simulation doesn't have constant pwl rates 
        # below 10 nm and kvapon = kpar for 1 nm particles
        # Dunne scaled by 1000 too
        "kvpon": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        # This is the same as kvpon but kvap_on = 
        # 3x kpar for 1 nm particles
        "kvp3x": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 2.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        
        
        # This simulation is currently the same as smtOH
        # but kpar is the summation of kflat and kturb
        "kflat": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        # Two PTR-MS datasets spliced together to cover data gaps
        "splic": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        "debug": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        "wiMDL": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        # This gets rid of the OH dips when the sun is near the horizon
        "minOH": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },
        # No injections 
        "noinj": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        # Just running for August 2nd
        "NPF_1": {
            "endtime": 23.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        # Just running for August 3rd
        "NPF_2": {
            "endtime": 23.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        # Just running for August 4th
        "NPF_3": {
            "endtime": 23.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        # Just running for August 5th
        "NPF_4": {
            "endtime": 23.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        # Just running for August 6th
        "NPF_5": {
            "endtime": 23.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
           
            },

        # This uses a scaled OH proxy and less smoothing
        "sclOH": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
            
            },

        # This is the same as sclOH, but OH is multiplied by 2x to better match GEOS-Chem
        "2x_OH": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
            
            },
        
        # this has the scaled OH (sclOH) but without the 1000x inorganic fn multiplier
        "sclfn": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
            
            },
        
        # OH from GEOS-Chem
        "GC_OH": {
            "endtime": 144.0,   # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 1.0,      # pre-factor to multiply OH concentration by
            "fion": 8.0,          # ion recombination coefficient 
            "org_nuc": 1,         # organic nucleation switch
            "inorg_nuc": 1,       # inorganic nucleation switch
            "COAG": 1,            # coagulation switch
            "vwl": 1,             # vapor wall loss switch
            "pwl": 1,             # particle wall loss switch
            "A": 1.0e-3,          # loss constant for particle wall losses
            "orgfrac_bg": 0.8,    # initial organic fraction of aerosols
            "boxvol": 2000000.0,  # box/bag volume [cm^3]
            "sfcpres": 101325.0,  # surface pressure 
            "kpar": ''.join([k_par + '0.00001440 ' for i in range(ibins)]), # size dependent wall loss coefficient 
            #"kvap_on": 2.50000e-03, # vapor wall loss coefficient 
            
            },


        }
  
    exp_dict = experiments[experiment_name]
    exp_dict['exp_name'] = experiment_name

    return exp_dict
