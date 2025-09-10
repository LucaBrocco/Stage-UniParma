import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from compute_metrics_Italy import load_results, italy_maps
import matplotlib as mpl

# decide if to run across all files to produce the csv or not
produce_csv = False

# choose type of data to parse (l_attack or l_peak)
data_types = ["l_attack","l_peak"]
chosen_type = data_types[0]
nprov = 107 # number of provinces in analysis

# all possibilities to parse
net_types = ["provinces"]
diseases = ["DENV"]
timestep = 2000
models = ["MRI-ESM2-0", "CESM2", "ACCESS-CM2"]  # put your models here
years = [2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]  # put your years here
scenarios = ["SSP1-2.6", "SSP2-4.5","SSP5-8.5"]

# all analyzed epsilon at 8-9-2025
#epsilons = ["0.0001","0.0005","0.001","0.005","0.01","0.0208","0.0292","0.03","0.0312","0.0333","0.0375","0.04","0.0417","0.0437","0.05","0.0563","0.0583","0.0625","0.0667","0.075","0.0833","0.1","0.25","0.5","0.75","1.0","1.25","1.5","1.875","2.0","2.5","3.0","3.75","4.5","5.0","5.625","6.0","6.25","7.5","9.375","10.0","12.5","30.0","100.0","10000.0"]
epsilons = ["0.0001","0.0005","0.001","0.005","0.01","0.05","0.1","0.25","0.5","0.75","1.0","2.0","3.0","5.0","10.0","30.0"]
# pick only "short range" epsilons
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

sel_disease = diseases[0]
sel_scenario = scenarios[0]
sel_model = models[0]
sel_epsilon = epsilons[0]
sel_year = years[0]

for sel_year in years:
    for sel_scenario in scenarios:
        for sel_model in models:
            # compute min and max attack rates for the colorbar
            mom_df = df[(df['model'] == sel_model) &
                        (df['scenario'] == sel_scenario) &
                        (df['year'] == sel_year)  &
                        (df['disease'] == sel_disease)]

            cmap_min = min(mom_df['l_attack'])
            cmap_max = max(mom_df['l_attack']) # max and min for colormaps

            for sel_epsilon in epsilons:
                sel_df = df[(df['model'] == sel_model) &
                            (df['scenario'] == sel_scenario) &
                            (df['year'] == sel_year)  &
                            (df['disease'] == sel_disease) &
                            (df['epsilon'] == sel_epsilon)]

                path_name = "/home/luca3/Desktop/PoD/stage/joint-model-parma-tobe-archived/joint-model-parma-tobe-archived/real_data/joint_mobility_provinces_IT.dat"
                d_load = load_results(path_name)
                savepath = f"/home/luca3/Desktop/PoD/stage/luca_plots/all_prov_results/{sel_disease}_{timestep}_{sel_scenario}_{sel_model}_{sel_year}_{sel_epsilon}_all_italy.png" # if False does not save. to save, put here the savepath
                doshow = False # if True shows the plot, else it does not
                title = f"{sel_disease} - Scenario {sel_scenario}\nModel {sel_model} - Year {sel_year} - $\epsilon$ = {sel_epsilon}"
                # plot italy map with the data
                italy_maps(100*sel_df['l_attack'],d_load,savepath,doshow,cmap_min,cmap_max,title,cmap="viridis")