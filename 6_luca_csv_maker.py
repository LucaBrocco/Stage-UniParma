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
years = [2030, 2040, 2050] #, 2060, 2070, 2080, 2090, 2100]  # put your years here
scenarios = ["SSP1-2.6", "SSP2-4.5","SSP5-8.5"]

# all analyzed epsilon at 8-9-2025
#epsilons = ["0.0001","0.0005","0.001","0.005","0.01","0.0208","0.0292","0.03","0.0312","0.0333","0.0375","0.04","0.0417","0.0437","0.05","0.0563","0.0583","0.0625","0.0667","0.075","0.0833","0.1","0.25","0.5","0.75","1.0"]#,"1.25","1.5","1.875","2.0","2.5","3.0","3.75","4.5","5.0","5.625","6.0","6.25","7.5","9.375","10.0","12.5","30.0","100.0","10000.0"]
# pick only "short range" epsilons
epsilons = ["0.0001","0.0005","0.001","0.005","0.01","0.05","0.1","0.25","0.5","0.75","1.0","2.0","3.0","5.0","10.0","30.0"]

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

# file for saving information from this code
csv_file = f"/home/luca3/Desktop/PoD/stage/luca_plots/max_attack_rates.csv"

# remember to flag the variable to re run the csv computation
if(produce_csv):
    for sel_disease in diseases:
        for sel_year in years:
            for sel_scenario in scenarios:
                for sel_model in models:
                    for sel_epsilon in epsilons:
                        sel_df = df[(df['year'] == sel_year) &
                                    (df['scenario'] == sel_scenario) &
                                    (df['model'] == sel_model) &
                                    (df['epsilon'] == sel_epsilon)]

                        plt.plot(sel_df.index % nprov, sel_df['l_attack'])
                        plt.title(f"{sel_disease} - Scenario {sel_scenario}\nModel {sel_model} - Year {sel_year}")
                        plt.xlabel("Provinces index")
                        plt.ylabel("Attack rate (%)")
                        plt.grid()
                        plt.savefig(f'/home/luca3/Desktop/PoD/stage/luca_plots/single_prov_results/{sel_disease}_{timestep}_{sel_scenario}_{sel_model}_{sel_year}_{sel_epsilon}_plot_l_attack_vs_provinces_idx.png')
                        #plt.show()
                        plt.close()
                        max_attack = max(sel_df['l_attack'])
                        avg_attack = np.mean(sel_df['l_attack'])
                        sum_attack = np.mean(sel_df['l_attack'])
                        std_attack = np.std(sel_df['l_attack'])
                        max_attack_idx = np.argmax(sel_df["l_attack"])
                        delta_max_mean = max_attack - avg_attack
                        #print(f"Max is {max_attack}, mean is {avg_attack}, std is {std_attack}, prov idx is {max_attack_idx}, max is {round(delta_max_mean/std_attack,3)} std far from mean")

                        df_max = pd.DataFrame([{
                                "disease":sel_disease,
                                "scenario":sel_scenario,
                                "model":sel_model,
                                "year":sel_year,
                                "epsilon":sel_epsilon,
                                "max_l_attack":max_attack,
                                "avg_attack":avg_attack,
                                "std_attack":std_attack,
                                "max_attack_idx":max_attack_idx,
                                "delta_std":delta_max_mean/std_attack,
                                "sum_attack":sum_attack
                            }])

                        # Append if file exists, else write with header
                        if not os.path.isfile(csv_file):
                            df_max.to_csv(csv_file, index=False, mode='w')   # first time: write with header
                        else:
                            df_max.to_csv(csv_file, index=False, mode='a', header=False)  # append without header


