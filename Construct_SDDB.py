"""
This is a code to develop a seismic deamnd database.
To run this code, you need to download ground motions from NGA-WEST database.

Developed by Taeyong Kim, University of Toronto
November 12, 2022
"""

# Import libraries
import numpy as np
import scipy.io as sio
import sqlite3
import os

#%%
# Function to handle AT2 format
def processNGAfile(filepath, scalefactor=None):
    '''
    This function process acceleration history for NGA data file (.AT2 format)
    to a single column value and return the total number of data points and 
    time iterval of the recording.
    Parameters:
    ------------
    filepath : string (location and name of the file)
    scalefactor : float (Optional) - multiplier factor that is applied to each
                  component in acceleration array.
    
    Output:
    ------------
    desc: Description of the earthquake (e.g., name, year, etc)
    npts: total number of recorded points (acceleration data)
    dt: time interval of recorded points
    time: array (n x 1) - time array, same length with npts
    inp_acc: array (n x 1) - acceleration array, same length with time
             unit usually in (g) unless stated as other.
    
    Example: (plot time vs acceleration)
    filepath = os.path.join(os.getcwd(),'motion_1')
    desc, npts, dt, time, inp_acc = processNGAfile (filepath)
    plt.plot(time,inp_acc)
        
    '''    
    try:
        if not scalefactor:
            scalefactor = 1.0
        with open(filepath,'r') as f:
            content = f.readlines()
        counter = 0
        desc, row4Val, acc_data = "","",[]
        for x in content:
            if counter == 1:
                desc = x
            elif counter == 3:
                row4Val = x
                if row4Val[0][0] == 'N':
                    val = row4Val.split()
                    npts = float(val[(val.index('NPTS='))+1].rstrip(','))
                    dt = float(val[(val.index('DT='))+1])
                else:
                    val = row4Val.split()
                    npts = float(val[0])
                    dt = float(val[1])
            elif counter > 3:
                data = str(x).split()
                for value in data:
                    a = float(value) * scalefactor
                    acc_data.append(a)
                inp_acc = np.asarray(acc_data)
                time = []
                for i in range (0,len(acc_data)):
                    t = i * dt
                    time.append(t)
            counter = counter + 1
        return desc, npts, dt, time, inp_acc
    except IOError:
        print("processMotion FAILED!: File is not in the directory")

        
#%% The target structural systems
Stiffness = np.load('stiffness.npy')

# Change stiffness to period (0,05~10 sec, 90 steps)
g = 9.8; # ground acceleration (m/s2)
Period = 2*np.pi*np.sqrt(1/g/Stiffness);

# Damping
Damping = [0.00, 0.001, 0.005, 0.010, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04,
           0.05, 0.07, 0.10, 0.12, 0.15,0.20, 0.25, 0.30, 0.35, 0.40]; 
#%% Ground motion information
# Please change accordingly based on the dataset you downloaded from NGA-WEST
###############################################################################
num_ground_motion = 1 # number of ground motions

GM_path_folder = "./GM_Data/"; # The path that ground motions are stored
temp_gm_location = "A-HMC180.AT2"; # THe number of ground motions
###############################################################################

#%% Construct database, Create a database to save the structural responses 
Name_db = 'SDDB_Linear_ver2.0.db'; # Name of the DB

# Make a database --> SQLite3
conn = sqlite3.connect(Name_db)

# Create cursur instance --> it tells the database what you want to do
db = conn.cursor()

# Generate table (3 tables)
table1_sql = """create table Ground_motion (ID integer PRIMARY KEY,  
                                            RSN INTEGER )"""
db.execute(table1_sql)

table2_sql = """create table Damping (ID integer PRIMARY KEY, 
                                      Damping_coeff REAL)"""
db.execute(table2_sql)
                                
table3_sql = """create table Structural_system (ID integer PRIMARY KEY, 
                                                "Period(s)" REAL,
                                                Stiffness REAL)"""
db.execute(table3_sql)

                                
table4_sql = """create table Analysis_result ("Displacement(m)" REAL,
                                            "Velocity(m/s)" REAL, 
                                            "Acceleration(m/s^2)" REAL, 
                                            Ground_motion_id INTEGER, 
                                            Damping_id INTEGER,
                                            Structural_id INTEGER, 
                                            FOREIGN KEY (Ground_motion_id) REFERENCES Ground_motion (ID), 
                                            FOREIGN KEY (Damping_id) REFERENCES Damping (ID), 
                                            FOREIGN KEY (Structural_id) REFERENCES Structural_system (ID))"""

db.execute(table4_sql)

conn.commit()

# SQL for storing the datasets to the database
# Please note that the ID starts from 0 not 1
# Insert one record into tables
Query1 = """ INSERT INTO Ground_motion VALUES (?, ?)"""
Query2 = """ INSERT INTO Damping VALUES (?, ?)"""
Query3 = """ INSERT INTO Structural_system VALUES (?, ?, ?)"""
Query4 = """ INSERT INTO Analysis_result VALUES (?, ?, ?, ?, ?, ?)"""

# Save the data into database
for ii in range(len(Damping)):
    temp_damp = Damping[ii]# % temporal damping
    db.execute(Query2, (ii+1,temp_damp) )
    
for ii in range(len(Period)):
    temp_period = Period[ii] 
    temp_stiff = Stiffness[ii]
    db.execute(Query3, (ii+1,float(temp_period),float(temp_stiff)) )
    
    
#%% Run dynamic analysis
DB_results = [];
# First loop for each ground motions
for ii in range(num_ground_motion):
    
    gm_info = processNGAfile(GM_path_folder+temp_gm_location)        
    
    db.execute(Query1, (ii+1,ii+1) )
    
    tmp_name1 = 'temp_ground_motion.txt'
    np.savetxt(tmp_name1, gm_info[4])
    
    # Write OpenSees file for the selected ground motion
    f = open('SDOF_linear_gm.tcl', 'w');
    f.write('set  Factor  1 \n');
    f.write('set GMfile     temp_ground_motion.txt \n');
    f.write('set dt        %f \n' %(gm_info[2]));
    f.write('set Nsteps    %f \n' %(gm_info[1]));
    f.write('set timeInc   %f \n' %(np.max([gm_info[2]/20, 0.00005])));
    f.close();

    # Second loop for each structural system (damping)
    for jj in range(2):#len(Damping)):
        temp_damp = Damping[jj]# % temporal damping

        # Write OpenSees file for the selected structural system
        f = open('SDOF_linear_model.tcl', 'w');        
        
        # Third loop for each structural system (period)
        for kk in range(3):#len(Stiffness)):
            temp_stiff = Stiffness[kk]#; % Temporal stiffness
            kk = kk+1
            f.write('node  %d  0.0  -mass 1.00 \n' %(kk*10));
            f.write('uniaxialMaterial  Elastic  %d  %f \n' %(kk*10, temp_stiff*g));
            f.write('uniaxialMaterial  Viscous  %d  %f  1.0 \n'
                    %(kk*10+1, 2*temp_damp*np.sqrt(temp_stiff*g/1)));
            f.write('element zeroLength  %d  1  %d   -mat %d -dir 1\n' %(kk*10, kk*10, kk*10));
            f.write('element zeroLength  %d  1  %d   -mat %d -dir 1\n' %(kk*10+1, kk*10, kk*10+1));
            f.write('\n');
        
        
        f.write('set  MaxNodeNo  %d \n' %(10*kk));
        f.write('set  MinNodeNo  %d \n' %(10*1));
        f.close();

        # Run OpenSees
        os.system("./OpenSees SDOF_linear_main.tcl")

        # Perform Post process
        Large_Res_disp = np.loadtxt('NodeDisp.txt');
        Large_Res_velo = np.loadtxt('NodeVelo.txt');
        Large_Res_acce = np.loadtxt('NodeAcce.txt');
        
        for kk in range(3): #len(Stiffness)):
            Res_disp = Large_Res_disp[:,kk];# % m
            Res_velo = Large_Res_velo[:,kk];# % m/s
            Res_acce = Large_Res_acce[:,kk];# % m/s^2

            tmp_DB = np.array([np.max(np.abs(Res_disp)), np.max(np.abs(Res_velo)), 
                               np.max(np.abs(Res_acce)), ii, jj, kk]); 
                  
            # Save the structural responses to the new database
            DB_results.append(tmp_DB)                
       
        os.remove('NodeDisp.txt')
        os.remove('NodeVelo.txt')
        os.remove('NodeAcce.txt')
        os.remove('SDOF_linear_model.tcl')
        
    os.remove('SDOF_linear_gm.tcl')

#% Save the results to the database
db.executemany(Query4, DB_results)
conn.commit()
conn.close()
    
