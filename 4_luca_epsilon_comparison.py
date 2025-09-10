import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap

# choose type of data to parse (l_attack or l_peak)
data_types = ["l_attack","l_peak"]
chosen_type = data_types[0]

# choose logscale or not
ylogscale = True
xlogscale = True

# choose fit or not
fit = False
# choose if 1/(1+1/epsilon) or not
mobility = False

# all possibilities to parse
net_types = ["provinces"]
timestep = 2000
models = ["MRI-ESM2-0", "CESM2", "ACCESS-CM2"]  # put your models here
years = [2030, 2040, 2050] #, 2060, 2070, 2080, 2090, 2100]  # put your years here
scenarios = ["SSP1-2.6", "SSP2-4.5","SSP5-8.5"]
epsilons = ["0.0001","0.0005","0.001","0.005","0.01","0.0208","0.0292","0.03","0.0312","0.0333","0.0375","0.04","0.0417","0.0437","0.05","0.0563","0.0583","0.0625","0.0667","0.075","0.0833","0.1","0.25","0.5","0.75","1.0","1.25","1.5","1.875","2.0","2.5","3.0","3.75","4.5","5.0","5.625","6.0","6.25","7.5","9.375","10.0","12.5","30.0","100.0","10000.0"]
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

sel_model = models[0]
sel_scenario = scenarios[0]
#sel_year = years[0]
sel_disease = diseases[0]


#years = [2080]
for sel_scenario in scenarios:
    for sel_model in models:
        plt.figure(figsize = (10,8))
        for sel_year in years:
            # data selection
            sel_df = df[(df['model'] == sel_model) &
                    (df['scenario'] == sel_scenario) &
                    (df['year'] == sel_year)  &
                    (df['disease'] == sel_disease)]
            # get the average
            averages = sel_df.groupby('epsilon')['l_attack'].mean().reset_index()
            # get the values
            yvalues = np.array(averages['l_attack'],dtype = float)
            xvalues = np.array(averages['epsilon'], dtype = float)
            
            if (mobility):
                xvalues = 1/(1.0+1.0/xvalues)
            
            
            if(fit and not ylogscale):
                print('Cannot fit outside logscale!')
                exit

            if (fit and ylogscale):
                save_path = '/home/luca3/Desktop/PoD/stage/luca_plots/epsilon_trends_fits'
                fit_results = np.polyfit(xvalues,yvalues,1)
                x_fittizzie = np.linspace(xvalues[0], # start of x range
                                        xvalues[-1], # end of x range
                                        2000 # numbers to make
                                        )
                y_fittizzie = x_fittizzie * fit_results[0] + fit_results[1] # produce fit
                plt.scatter(xvalues, # x axis content
                            yvalues, # y axis content (attack)scatter
                            label = f"{sel_year}"
                            )
                #plt.plot(x_fittizzie, y_fittizzie, ls = '-') # plot of the fit
                print('Fit results')
                print(fit_results)
                
                plt.ylabel("Attack rate (%)")
                plt.title(f"{sel_disease} - Scenario: {sel_scenario}\nModel {sel_model} - Years from {years[0]} to {years[-1]}")
                plt.grid()
                plt.show()
                exit
            else:
                save_path = '/home/luca3/Desktop/PoD/stage/luca_plots/epsilon_trends_nofits'
                plt.plot(xvalues, # x axis content
                        yvalues, # y axis content (attack)scatter
                        'o', #pointtype
                        label = f"{sel_year}",
                        ls = '--',
                        )
        if (mobility):
            plt.xlabel(f"1/(1+1/$\epsilon$)")
            mob = 'mobility_'
        else:
            plt.xlabel(f"$\epsilon$")
            mob = ''
        plt.ylabel("Attack rate (%)")
        plt.title(f"{sel_disease} - Scenario: {sel_scenario}\nModel {sel_model} - Years from {years[0]} to {years[-1]}")
        plt.grid()
        if(xlogscale):
            plt.xscale('log')
            llsx = 'logscalex_'
        else:
            llsx = ''
        if (ylogscale):
            plt.yscale('log')
            llsy = 'logscaley_'
        else:
            llsy = ''
            
        plt.legend()
        plt.savefig(f"{save_path}/{mob}{llsx}{llsy}{sel_disease}_{timestep}_{sel_scenario}_{sel_model}_{years[0]}_to_{years[-1]}_eps_{epsilons[0]}_to_{epsilons[-1]}.png")
        plt.show()



'''code AUGUST PLOTS
alpha_step = 1.0 / len(epsilons)

plt.figure(figsize = (9,6))
sel_model = models[0]
sel_scenario = scenarios[0]
alphavalue = 1.0 - alpha_step * len(epsilons) 
years_str = [str(y) for y in years] # years in string
for epsilon in epsilons:
    sel_df = df[(df['disease'] == sel_disease)&
            (df['epsilon'] == epsilon)&
            (df['scenario'] == sel_scenario) &
            (df['model'] == sel_model)] # take desired data
    averages = sel_df.groupby('year')['l_attack'].mean()
    plt.plot(years, # x axis content
            averages, # y axis content
            'o-', # format
            c=colors[0], # color
            alpha = alphavalue, # sfumature
            label = fr'Model {sel_model} $\epsilon$ = {epsilon}'
            )
            
    alphavalue += alpha_step
        
plt.legend(bbox_to_anchor=(1.0, 1.0))
plt.xlabel('Year')
plt.ylabel('Attack rate (%)')
title_str = f'Attack rate vs year vs $\\epsilon$ - {sel_disease} - Timestep {timestep}\nScenario {sel_scenario} - Model {sel_model}'

plt.title("\n".join(textwrap.wrap(title_str, 60)))
plt.grid(ls = '--')
if (logscale):
    plt.yscale('log')
    lls = 'logscale_'
else:
    lls = ''
    
plt.savefig(f'/home/luca3/Desktop/PoD/stage/luca_plots/epsilon_comparisons/{lls}{sel_disease}_{timestep}_{sel_scenario}_{sel_model}_{epsilons[0]}_to_{epsilons[-1]}.jpg',bbox_inches = 'tight')

plt.show()
#print(sel_scenario, sel_model)
'''
