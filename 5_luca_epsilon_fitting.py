import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap
import os

# FITTING POWER LAW HYPOTESIS OVER RELATION BETWEEN l_attack (Y) and epsilon (X)
# choose type of data to parse (l_attack or l_peak)
data_types = ["l_attack","l_peak"]
chosen_type = data_types[0]
nprov = 107 # number of provinces in analysis

# if logscale on both axis
loglog = False

# all possibilities to parse
net_types = ["provinces"]
timestep = 2000

# Lists of parameters to test
# Lists of parameters to test
models = ["CESM2", "ACCESS-CM2", "MRI-ESM2-0"]  # put your models here
years = [2030, 2040, 2050] #, 2060, 2070, 2080, 2090, 2100]  # put your years here
scenarios = ["SSP1-2.6", "SSP2-4.5","SSP5-8.5"]

# times associated for the mobility: they should range in realistic intervals
# 0.5-1 day daily commute
# 2-3 days short trips
# 30-90 days seasonal migration
'''short time windows
Tmob = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
Tepi = [12.0, 16.0, 20.0, 24.0] # time (in days) that an infected host needs to completely range across all disease phases'''
Tmob = [30.0, 60.0, 90.0, 120.0, 150.0]
Tepi = [12.0, 16.0, 20.0, 24.0]

# epsilons is all possible combinations of Tmob / Tepi rounded to 4 decimal 
epsilons = [round(i/j,4) for i in Tepi for j in Tmob]
epsilons = epsilons[4:]

# Loop over combinations
diseases = ["DENV"]

color_epsilons = ['#FFCF99',
                  '#FFB056',
                  '#FF9013',
                  '#CF6E00',
                  "#965101",
                  "#582F00",
                  '#050300']

color_epsilons_dict = dict(zip(epsilons,color_epsilons))

# common path to all files
main_path = "/home/luca3/Desktop/PoD/stage/joint-model-parma-tobe-archived/joint-model-parma-tobe-archived/luca_runs"

list_df = []
for disease in diseases:
    for net_type in net_types:
        for year in years:
            for scenario in scenarios:
                for model in models:
                    for epsilon in epsilons:
                        subfolder_path = f"{disease}_{net_type}_{timestep}_{year}_{scenario}_{model}_{epsilon}"
                        data = np.load(f"{main_path}/{subfolder_path}/{chosen_type}.npy")
                        #print(np.shape(data))

                        datapoint_df = pd.DataFrame({
                            f"{chosen_type}": data * 100, # compute the percentage
                            #"disease": disease * len(data),
                            "year": np.full(len(data), year),
                            "scenario": np.full(len(data), scenario),
                            "model": np.full(len(data), model),
                            "disease":np.full(len(data), disease),
                            "epsilon":np.full(len(data), epsilon)
                        })
                        list_df.append(datapoint_df)


df = pd.concat(list_df, ignore_index=True)
#print(np.shape(df))
#print(df[:5])

sel_model = models[1]
sel_scenario = scenarios[0]
sel_year = years[0]
sel_disease = diseases[0]

# file for saving results
csv_file = f"/home/luca3/Desktop/PoD/stage/luca_plots/deep_epsilon_trends_fits/fit_results.csv"

def f_epsilon(epsilon):
    return(1.0/(1.0+1.0/epsilon))

for sel_model in models:
    for sel_scenario in scenarios:
        for sel_year in years:
            plt.figure(figsize = (8,6))
            sel_df = df[(df['model'] == sel_model) &
                                (df['scenario'] == sel_scenario) &
                                (df['year'] == sel_year)  &
                                (df['disease'] == sel_disease)]
            # average over provinces
            averages = sel_df.groupby('epsilon')['l_attack'].mean().reset_index()
            # get errors 
            errors = sel_df.groupby('epsilon')['l_attack'].std().reset_index()
            if loglog:
                # take logs (hp of power-law)
                yvalues = np.log(np.array(averages['l_attack'],dtype = float))
                # compute errors
                yerr = abs(np.log(np.array(errors['l_attack'], dtype = float)))/np.sqrt(nprov)
                xvalues = np.log(np.array(averages['epsilon'], dtype = float))
            else:
                # take logs (hp of power-law)
                yvalues = np.array(averages['l_attack'],dtype = float)
                # compute errors
                yerr = abs(np.array(errors['l_attack'], dtype = float))/np.sqrt(nprov)
                xvalues = np.array(averages['epsilon'], dtype = float)

            plt.scatter(xvalues,yvalues, label = f'{sel_year}') # plot immediately then remove undesired points for fit
            # plot errorbars
            plt.errorbar(xvalues,yvalues,yerr = yerr, fmt = 'o')

            # take only desired points for the fit
            idx = 0
            xvalues = xvalues[idx:]
            yvalues = yvalues[idx:]

            fit_res = np.polyfit(xvalues,yvalues,1)
            print(f'Fit results for {sel_disease} - Scenario {sel_scenario}\nModel {sel_model} - Years {years[0]} to {years[-1]}')
            print(fit_res,'\n')
            xfit = np.linspace(min(xvalues), max(xvalues),1000)
            yfit = fit_res[1] + fit_res[0] * xfit

            
            plt.plot(xfit, yfit, ls = '-', label = f'{sel_year} fit', c='orange')
            plt.title(f'{sel_disease} - Scenario {sel_scenario}\nModel {sel_model} - Year {sel_year}')
            # add fit info
            textstr = f"$y = {fit_res[1]:.2f} \\, + {{{fit_res[0]:.2f}}}x$"
            plt.text(0.05, 0.95, textstr,
                    transform=plt.gca().transAxes,  # relative coords (0–1)
                    fontsize=12, verticalalignment='top',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7))
            
            # add squared distance error (MSE)
            ypred = fit_res[1] + fit_res[0] * xvalues
            MSE = sum((ypred - yvalues)**2)
            textMSE = f"MSE = {round(MSE,3)}"
            plt.text(0.05, 0.85, textMSE,
                    transform=plt.gca().transAxes,  # relative coords (0–1)
                    fontsize=12, verticalalignment='top',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7))
            if loglog:
                plt.xlabel(f'log($\epsilon$)')
                plt.ylabel('log(Attack rate (%))')
            else:
                plt.xlabel(f'$\epsilon$')
                plt.ylabel('Attack rate (%)')
            plt.grid()
            plt.legend()
            # savefig
            if loglog:
                logloglab = 'loglog_'
            else:
                logloglab = ""
            plt.savefig(f'/home/luca3/Desktop/PoD/stage/luca_plots/deep_epsilon_trends_fits/{logloglab}{sel_disease}_{timestep}_{sel_scenario}_{sel_model}_{sel_year}_{xvalues[0]}_to_{xvalues[-1]}_fitting_epsilon.png')
            plt.show()
            
            # save fit info
            df_epsilon = pd.DataFrame([{
                "disease":sel_disease,
                "scenario":sel_scenario,
                "model":sel_model,
                "year":sel_year,
                "starting eps":epsilons[0],
                "ending eps":epsilons[-1],
                "fr0":fit_res[0],
                "fr1":fit_res[1],
                "MSE":MSE,
                "log":loglog
            }])

            # Append if file exists, else write with header
            if not os.path.isfile(csv_file):
                df_epsilon.to_csv(csv_file, index=False, mode='w')   # first time: write with header
            else:
                df_epsilon.to_csv(csv_file, index=False, mode='a', header=False)  # append without header
