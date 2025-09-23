This code --
wave_power_model generates ---. Format
wave_occurrence_model generates ---
GloPW run both models, combine the results, and generates ---

Format of the input files
1) Threshold.txt

     0.298000	<-- H+-band threhold
     0.213000	<-- He+-band threhold

2) RF_model_input.txt
		Col1				Col2				Col3				Col4				Col5				Col6				Col7				Col8				Col9				Col10
       20.948938	       71.435536	       1.3329999	       2.0000000	       2.2300000	       5.2363290	       1.7779541	      -3.9603143	     -0.95053719	       4.2857918
       20.989233	       71.434269	       1.3329999	       2.0000000	       2.2300000	       5.2482190	       1.7919230	      -3.9724672	     -0.96296224	       4.2852568
       21.029564	       71.433002	       1.3329999	       2.0000000	       2.2200000	       5.2599753	       1.8058308	      -3.9845619	     -0.97525432	       4.2847209
       21.069935	       71.431736	       1.0000000	       2.0000000	       2.2200000	       5.2716002	       1.8196797	      -3.9966094	     -0.98741613	       4.2841841
       21.110340	       71.430469	       1.0000000	       2.0000000	       2.2300000	       5.2830947	       1.8334737	      -4.0086102	     -0.99944850	       4.2836462
       21.150784	       71.429202	       1.0000000	       2.0000000	       2.2600000	       5.2944580	       1.8472106	      -4.0205631	      -1.0113506	       4.2831074
       21.191261	       71.427936	       1.0000000	       2.0000000	       2.2600000	       5.3056903	       1.8608928	      -4.0324650	      -1.0231227	       4.2825676
...

Col1: Dipole tilt angle in degree
Col2: F10.7
Col3: HP30
Col4: HP30* (maximum HP30 in 3 hours)
Col5: Solar wind dynamic pressure in nPa
Col6: L
Col7: MLT in hour
Col8: MLAT in degree
Col9: Distance to the LPP
Col10: Lpp


HOW TO RUN THE MODEL?

1) Ensure that your python version should be later than 3.3.

2) Install XGBoost in your python environment. See details of XGBoost https://xgboost.readthedocs.io/en/stable/.

pip install xgboost
or
conda install -c conda-forge xgboost

3) Run GloPW.py in the src folder.

