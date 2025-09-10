# this notebook takes all possible combinations of scenario and model, and for 3 selected epsilon values (1 high, 1 low, 1 = 1) computes the outcomes of the simulations in terms of attack rates

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap
import os

# decide if to run across all files to produce the csv or not
produce_csv = True

# choose type of data to parse (l_attack or l_peak)
data_types = ["l_attack","l_peak"]
chosen_type = data_types[0]
nprov = 107 # number of provinces in analysis

# all possibilities to parse
net_types = ["provinces"]
timestep = 2000
models = ["MRI-ESM2-0", "CESM2", "ACCESS-CM2"]  # put your models here
years = [2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]  # put your years here
scenarios = ["SSP1-2.6", "SSP2-4.5","SSP5-8.5"]

# all analyzed epsilon at 8-9-2025
#epsilons = ["0.0001","0.0005","0.001","0.005","0.01","0.0208","0.0292","0.03","0.0312","0.0333","0.0375","0.04","0.0417","0.0437","0.05","0.0563","0.0583","0.0625","0.0667","0.075","0.0833","0.1","0.25","0.5","0.75","1.0"]#,"1.25","1.5","1.875","2.0","2.5","3.0","3.75","4.5","5.0","5.625","6.0","6.25","7.5","9.375","10.0","12.5","30.0","100.0","10000.0"]
# short range, 1, long range (for epsilon)
epsilons = ["0.1","0.5","1.0","5.0","10.0"]

diseases = ["DENV"]

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
sel_model = models[0]
sel_scenario = scenarios[2]
sel_epsilon = epsilons[1]
# select data for a specific (scenario, model) combination, then take an epsilon
# I want to study the influence of this epsilon value on the model

results = []
for sel_model in models:
    for sel_scenario in scenarios:
        for sel_epsilon in epsilons:
            sel_df = df[(df['model'] == sel_model) &
                        (df['scenario'] == sel_scenario) &
                        (df['epsilon'] == sel_epsilon)]

            means = []
            for sel_year in years:
                data = sel_df[sel_df['year'] == sel_year]
                means.append(np.mean(data['l_attack']))
            delta_means = max(means)-min(means)
            res_dict = {
                "scenario":sel_scenario,
                "model":sel_model,
                "epsilon":sel_epsilon,
                "delta_mean":delta_means
            }
            results.append(res_dict)

df_res = pd.DataFrame(results)
df_mean = df_res.groupby(['scenario','model'])['delta_mean'].mean()
df_std = df_res.groupby(['scenario','model'])['delta_mean'].std()
print(df_mean)
print(df_std)