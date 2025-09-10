import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from compute_metrics_Italy import load_results, italy_maps

# decide if to run across all files to produce the csv or not
produce_csv = False

# choose type of data to parse (l_attack or l_peak)
data_types = ["l_attack","l_peak"]
chosen_type = data_types[0]
nprov = 107 # number of provinces in analysis

# all possibilities to parse
diseases = ["DENV"]
net_types = ["provinces"]
timestep = 2000
models = ["MRI-ESM2-0", "CESM2", "ACCESS-CM2"]  # put your models here
years = [2030, 2040, 2050] #, 2060, 2070, 2080, 2090, 2100]  # put your years here
scenarios = ["SSP1-2.6", "SSP2-4.5","SSP5-8.5"]

# all analyzed epsilon at 8-9-2025
epsilons = ["0.0001","0.0005","0.001","0.005","0.01","0.0208","0.0292","0.03","0.0312","0.0333","0.0375","0.04","0.0417","0.0437","0.05","0.0563","0.0583","0.0625","0.0667","0.075","0.0833","0.1","0.25","0.5","0.75","1.0"]#,"1.25","1.5","1.875","2.0","2.5","3.0","3.75","4.5","5.0","5.625","6.0","6.25","7.5","9.375","10.0","12.5","30.0","100.0","10000.0"]
# pick only "short range" epsilons

# import the csv just created
df = pd.read_csv(f"/home/luca3/Desktop/PoD/stage/luca_plots/max_attack_rates.csv")
df = df.drop_duplicates() # remove duplicates

print(df.columns)
sel_year = years[1]
sel_scenario = scenarios[1]
sel_model = models[0]
sel_disease = diseases[0]
max_epsilon = 20.0

for sel_scenario in scenarios:
    for sel_model in models:
        
        plt.figure(figsize=(10,8))
        for sel_year in years:
            sel_df = df[(df['year'] == sel_year) &
                        (df['scenario'] == sel_scenario) &
                        (df['model'] == sel_model) &
                        (df['epsilon'] <= max_epsilon)
                    ]
            # plot the trend of epsilon vs the distance between max and mean (in std units)
            
            plt.scatter(sel_df['epsilon'],sel_df['std_attack']/sel_df['avg_attack'], label = f"{sel_year}")
        plt.grid(which = 'both', ls = '--')
        plt.xscale('log')
        #plt.yscale('log')
        #plt.ylim([0,12])
        #plt.minorticks_on()  # ensure minor ticks are enabled
        fs = 18
        plt.xlabel(f'$\epsilon$', fontsize = fs)
        plt.ylabel(r'$\frac{\sigma}{\mu}$', fontsize = fs)
        #plt.ylabel(r"$\frac{max - \mu}{\sigma}$")
        plt.title(f"{sel_disease} - Scenario {sel_scenario}\nModel {sel_model}", fontsize = fs+2)
        plt.legend()
        plt.xticks(fontsize = fs-4)
        plt.yticks(fontsize = fs-4)
        plt.savefig(f"/home/luca3/Desktop/PoD/stage/luca_plots/std_over_max/{sel_disease}_{sel_scenario}_{sel_model}_{sel_year}_{epsilons[0]}_to_{epsilons[-1]}_stdovermu_vs_epsilon_noylog.png")
        

        plt.show()

