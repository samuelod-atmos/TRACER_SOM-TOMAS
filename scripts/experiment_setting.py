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


        "debug": {
            "endtime": 144.0,     # length of simulation 
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
            "fn_scale": 100.0,
            "T_switch": 1,
            "RH_switch": 1,
            "HOM_switch": 0,

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

        


        # no HOMs 
        "noHOM": {
            "endtime": 144.0,     # length of simulation 
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
            "fn_scale": 100.0,
            "T_switch": 1,
            "RH_switch": 1,
            "HOM_switch": 0,
            },


        # SOM species can't mix out
        "sommx": {
            "endtime": 144.0,     # length of simulation 
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
            "fn_scale": 100.0,
            "T_switch": 1,
            "RH_switch": 1,
            "HOM_switch": 1,
            },

        "kp1.5": {
            "endtime": 144.0,     # length of simulation 
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
            "fn_scale": 100.0,
            "T_switch": 1,
            "RH_switch": 1,
            "HOM_switch": 0,
            },

        "kp2.0": {
            "endtime": 144.0,     # length of simulation 
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
            "fn_scale": 100.0,
            "T_switch": 1,
            "RH_switch": 1,
            "HOM_switch": 0,
            },

        "kp2.5": {
            "endtime": 144.0,     # length of simulation 
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
            "fn_scale": 100.0,
            "T_switch": 1,
            "RH_switch": 1,
            "HOM_switch": 0,
            },
        
        # SOM grid gases can mix out of the chamber
        "y_mix": {
            "endtime": 144.0,     # length of simulation 
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
            "fn_scale": 100.0,
            "T_switch": 1,
            "RH_switch": 1,
            "HOM_switch": 0,
            },
        
        # SOM grid gases cannot mix out of the chamber
        "n_mix": {
            "endtime": 144.0,     # length of simulation 
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
            "fn_scale": 100.0,
            "T_switch": 1,
            "RH_switch": 1,
            "HOM_switch": 0,
            },
        
        
        
        # 
        "A1e-3": {
            "endtime": 144.0,     # length of simulation 
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
            "fn_scale": 1000.0,
            "T_switch": 1,
            "RH_switch": 1,
            "HOM_switch": 0,
            },

        # kflat = 1.3e-4 
        "kflat": {
            "endtime": 144.0,     # length of simulation 
            "aadt": 10,           # time step [s]
            "NOx": 5.0,           # NOx concentration [ppb]
            "nh3_ppt": [5000],    # Ammonia concentration for nucleation [ppt]
            "OH_scale": 0.8,      # pre-factor to multiply OH concentration by
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
            "fn_scale": 1000.0,
            "T_switch": 1,
            "RH_switch": 1,
            "HOM_switch": 0,
            },


        }
  
    exp_dict = experiments[experiment_name]
    exp_dict['exp_name'] = experiment_name

    return exp_dict
