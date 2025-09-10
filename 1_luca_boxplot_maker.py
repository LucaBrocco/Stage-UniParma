import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# choose type of data to parse (l_attack or l_peak)
data_types = ["l_attack","l_peak"]
chosen_type = data_types[0]

# choose logscale or not
logscale = True
# choose modality (all scenarios in one plot or not)
triple = True

# all possibilities to parse
net_types = ["provinces"]
timestep = 2000
scenarios = ["SSP1-2.6","SSP2-4.5","SSP5-8.5"]
models = ["ACCESS-CM2", "CESM2","MRI-ESM2-0"]
years = [2030,2040,2050,2060,2070,2080,2090,2100]
diseases = ["DENV"]
epsilons = [0.0001,0.5,1.0,10.0,100.0]

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
print(np.shape(df))
print(df[:5])

# plot color setup
palette = {
    "ACCESS-CM2": "blue",
    "CESM2": "red", 
    "MRI-ESM2-0": "green"
}

# outliers
flierprops = dict(marker='o', markerfacecolor='white', markersize=8, markeredgecolor='black')
bbwidth = 0.5

# mean points - we'll customize these manually after plotting
meanlineprops = dict(linestyle='-', linewidth=2.5, color='purple')

# boxes - white fill with black edges
boxprops = dict(facecolor='white', edgecolor='black', linewidth=1)

# boxplot maker
sel_disease = diseases[0]
sel_scenario = scenarios[1] 
sel_epsilon = epsilons[0]

# ALL CODE FOR SINGLE PLOTS
if (not triple):
    for sel_epsilon in epsilons:
        for sel_scenario in scenarios:
            sel_df = df[(df['disease'] == sel_disease) & (df['scenario'] == sel_scenario) & (df['epsilon'] == sel_epsilon)]

            plt.figure(figsize=(10,8))

            # Create boxplot with dodge=True for separation
            bplot = sns.boxplot(
                x='year',
                y='l_attack', 
                hue='model',
                data=sel_df,
                palette=palette,
                showmeans=False,  # We'll add custom means
                flierprops=flierprops,
                boxprops=boxprops,
                dodge=True,  # This separates the boxes by hue
                width= 0.5
            )

            # Custom mean markers with different shapes and colors
            models = sel_df['model'].unique()
            marker_dict = {
                models[0]: 's',  # square
                models[1]: 'o',  # circle  
                models[2]: '^'   # triangle
            }  
            for i, year in enumerate(sel_df['year'].unique()):
                year_data = sel_df[sel_df['year'] == year]
                
                # Calculate positions to match seaborn's dodge spacing
                n_models = len(models)
                width = (bbwidth * 1.28 ) / n_models
                base_positions = [i + (j - (n_models-1)/2) * width * 0.8 for j in range(n_models)]
                
                for j, model in enumerate(models):
                    model_data = year_data[year_data['model'] == model]['l_attack']
                    if not model_data.empty:
                        mean_val = model_data.mean()
                        plt.scatter(base_positions[j], mean_val, 
                                marker=marker_dict[model], 
                                color=palette[model], 
                                s=100, 
                                edgecolor='black',
                                linewidth=1,
                                zorder=10,
                                label=f'{model} mean' if i == 0 else "")

            if logscale:
                plt.yscale('log')

            # Create custom legend combining box colors and mean markers
            handles, labels = plt.gca().get_legend_handles_labels()

            # Filter out duplicate mean labels (only keep first occurrence)
            unique_handles = []
            unique_labels = []
            seen_labels = set()

            for handle, label in zip(handles, labels):
                if 'mean' in label:
                    model_name = label.replace(' mean', '')
                    if model_name not in seen_labels:
                        unique_handles.append(handle)
                        unique_labels.append(model_name)
                        seen_labels.add(model_name)
                elif label not in seen_labels:
                    unique_handles.append(handle)
                    unique_labels.append(label)
                    seen_labels.add(label)
            plt.legend(unique_handles, unique_labels)
            plt.title(f'{sel_disease} - Timestep {timestep} - Scenario {sel_scenario} $\epsilon$ = {sel_epsilon}')
            plt.grid(ls='--')
            plt.ylabel('Attack rate (%)')
            plt.xlabel('Year')
            plt.savefig(f'/home/luca3/Desktop/PoD/stage/luca_plots/boxplots/single_boxplot_{sel_disease}_{timestep}_{years[0]}_to_{years[-1]}_{sel_scenario}_all_models_{sel_epsilon}.png', dpi = 300)
            plt.show()

# so we want triple plots
else: 
    
    for sel_epsilon in epsilons:
        # Create figure with subplots = one per scenario
        n_scenarios = len(scenarios)
        fig, axes = plt.subplots(
            n_scenarios, 1, 
            figsize=(8, 6 * n_scenarios), 
            sharey=True,
            gridspec_kw={"wspace": 0.3, "hspace": 0.4}
        )

        if n_scenarios == 1:
            axes = [axes]  # make iterable if single subplot

        for ax, sel_scenario in zip(axes, scenarios):
            sel_df = df[
                (df['disease'] == sel_disease) &
                (df['scenario'] == sel_scenario) &
                (df['epsilon'] == sel_epsilon)
            ]

            # Boxplot
            bplot = sns.boxplot(
                x='year',
                y='l_attack',
                hue='model',
                data=sel_df,
                palette=palette,
                showmeans=False,
                flierprops=flierprops,
                boxprops=boxprops,
                dodge=True,
                width=0.5,
                ax=ax,
                legend = True
            )
            
            # Custom mean markers
            models = sel_df['model'].unique()
            marker_dict = {
                models[0]: 's',
                models[1]: 'o',
                models[2]: '^'
            }
            for i, year in enumerate(sel_df['year'].unique()):
                year_data = sel_df[sel_df['year'] == year]
                n_models = len(models)
                width = (bbwidth * 1.28) / n_models
                base_positions = [i + (j - (n_models-1)/2) * width * 0.8 for j in range(n_models)]

                for j, model in enumerate(models):
                    model_data = year_data[year_data['model'] == model]['l_attack']
                    if not model_data.empty:
                        mean_val = model_data.mean()
                        ax.scatter(
                            base_positions[j], mean_val,
                            marker=marker_dict[model],
                            color=palette[model],
                            s=100,
                            edgecolor='black',
                            linewidth=1,
                            zorder=10,
                            label=f'{model} mean' if i == 0 else ""
                        )

            if logscale:
                ax.set_yscale('log')

            # Title per subplot
            ax.set_title(f'Scenario {sel_scenario}')
            ax.set_ylabel('Attack rate (%)')
            ax.set_xlabel('Year')
            ax.grid(ls='--')

        fig.suptitle(f'{sel_disease} - Timestep {timestep} - $\epsilon$={sel_epsilon}', fontsize=14)

        plt.tight_layout(rect=[0,0,1,0.95])
 
        plt.savefig(f'/home/luca3/Desktop/PoD/stage/luca_plots/boxplots/multiplot_{sel_disease}_{timestep}_{years[0]}_to_{years[-1]}_{sel_epsilon}.png', dpi=300)
        plt.show()
