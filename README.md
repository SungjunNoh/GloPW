# GloPW

This model produces global EMIC wave activities (occurrence and wave power) in the Earth's magneosphere. The wave activity is modeled globally on the magnetic equator, and as functions of L-MLT.

The wave occurrence model (wave_occurrence_model.py) is designed to determine presence or absence, which is a binary classification problem, of EMIC wave activity at a given time segment and position. To address this binary classification problem, we utilize the Extreme Gradient Boosting (XGBoost) library (available at https://xgboost.readthedocs.io/en/stable/). The XGBoost is a decision tree-based gradient boosting technique that is widely used as a machine learning algorithm for binary classification problems. It captures nonlinear relationships and is also robust to overfitting issues (Chen et al. 2016).

Once the occurrence model identifies the presence of an EMIC wave, the power model (wave_power_model.py) estimates its frequency-integrated power (in nT²). To model the wave power, we construct a probability distribution function (PDF) of wave power in each spatial and Hp30 bin. In the first method, we choose 50% percentile of the PDF as the representing wave power. 16% and 84% quantiles, which fall into 68% confidence interval, are the lower and upper bounds of the wave power, respectively. However, one cannot fully reconstruct the PDF only with the three values. Thus, the model also provides Monte Carlo samples of wave power from the PDF, allowing the user to generate any number of samples from the PDF. This sampling method randomly chooses a value in the cumulative distribution function (CDF)—a random position in the y axis of Figure 5—and maps the selected position to the equivalent wave power; thus there is a higher probability to choose values near the peak of the PDF. If the number of samples is statistically large, this approach approximates the true distribution function and provides flexible uncertainty estimates which is useful for global simulations.

GloPW run both models, combine the results, and generates final outputs. Detailed descriptions are available in Noh et al. (2025).

# Format of the input files
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

