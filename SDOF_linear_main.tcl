wipe;
model BasicBuilder -ndm 1 -ndf 1
node       1        0.00
fix    	   1  		1 




# Following two files are created from python script
source SDOF_linear_model.tcl;         # SDOF models
source SDOF_linear_gm.tcl;         # Earthquake motions


set scale_factor [expr $Factor*9.8]
#set accelSeries "Series -dt $dt -filePath $GMfile -factor $scale_factor"

set tsTag 1
set ptTag 1
#pattern UniformExcitation $ptTag 1 -accel $accelSeries;		# define where and how (pattern tag, dof) acceleration is applied

timeSeries Path $tsTag -dt $dt -filePath $GMfile -factor $scale_factor	
pattern UniformExcitation $ptTag 1 -accel $tsTag;		# define where and how (pattern tag, dof) 


# Output recorders
recorder Node    -file NodeDisp.txt -nodeRange $MinNodeNo $MaxNodeNo -dof 1 disp
recorder Node    -file NodeVelo.txt -nodeRange $MinNodeNo $MaxNodeNo -dof 1 vel
recorder Node    -file NodeAcce.txt -nodeRange $MinNodeNo $MaxNodeNo -dof 1 -timeSeries $tsTag accel


# Analysis parameters
set gamma 0.5;                      # Newmark integration parameter
set beta  0.25;                     # Newmark integration parameter
set Tol 1.0e-7;                     # convergence tolerance for test

constraints  Transformation
#constraints Penalty 1e10 1e10;     # how it handles boundary conditions
numberer 	Plain;                  # DOF numberer
system      UmfPack;                # how to store and solve the system of equations in the analysis (large model: try UmfPack)
#system      BandGeneral;           # how to store and solve the system of equations in the analysis (large model: try UmfPack)
test        NormDispIncr $Tol 100;  # determine if convergence has been achieved at the end of an iteration step
algorithm   Newton;                 # use Newton's solution algorithm: updates tangent stiffness at every iteration
integrator  Newmark $gamma $beta;    
#integrator  HHT 0.9;    
#integrator  GeneralizedAlpha 1.0 0.8;
analysis    Transient;


# Run dynamic analysis
set numSteps [expr int($Nsteps*$dt/$timeInc)]

puts "Running time history analysis..."
analyze $numSteps $timeInc;            

wipe;
puts "Time history analysis done."