##############################################################
README LUCA REPOSITORY FOR STAGE @ UniParma (update 10/9/2025)
##############################################################

This readme contains important information about the code you can find in the repository @ https://github.com/LucaBrocco/Stage-UniParma
The code was developed to study the influence of an epsilon parameter (from now on ε) on the study subject system. The system is the ensemble of a SEIR model for the spread of vector-borne diseases across Italy and a dynamics model that predict migration across the provinces.

For reference on the overall project you can refer to my presentation: https://docs.google.com/presentation/d/1utg1bDcg_0hMJfotu1VzGe9IWVtjOMtOhUyP-is22ZU/edit?usp=sharing or contact me at lucabrocco31@gmail.com

############################
EPSILON (ε) PARAMETER'S ROLE
############################

ε is a parameter that determines the difference in terms of timescale between mobility-related events and disease-related events. In my interpretation, it can be seen as:

ε = Tdisease / Tmobility

where for Tdisease I refer to a typical time range of a complete disease outbreak in a host (from being exposed to being recovered, typical range is between 10-20 days for DENV) and Tmobility refers to the typical time range of mobility events there considered (0.5-1 day for daily commute events, 60-120 days for migration events). This leads ε to have a wide range of possible values. We are interested in seeing if the system behaves significantly differently when ε varies. 

To achieve this, I set up a pipeline for the study.


#############
PREREQUISITES
#############

We need to work inside joint-model-parma-tobe-archived folder from Charles. The folder was already edited by Paolo to have comprehensive scripts that merge the workflow together, so that we don't need to run manually all the files. To run my scripts, just get them inside /home/user/.../joint-model-parma-tobe-archived/joint-model-parma-tobe-archived 

!!!!!!!!!!!!
### NOTE ###
All paths contained in my files are absolute, relative to my local PC. You will need to adjust these accordingly.

!!!!!!!!!!!!
### NOTE ###
File notation: all output files should be named according to the following order, if they are relative to a specific run 
DISEASE_NETTYPE_TIMESTEP_YEAR_SCENARIO_MODEL_ε

e.g. : DENV_provinces_2000_2030_SSP1-2.6_ACCESS-CM2_0.1 (this is the name of a folder containing the run)

I have always kept, up to today (10/9/2025) the following constants:
disease: DENV
nettype: provinces
timestep: 2000


################
1: boxplot maker
################

This code snippet produces a boxplot. This code assumes that you already took at least a complete run of the epidemics (complete meaning you iterated across all years and all possible combinations of scenario-model for at least one value of epsilon). If you don't have a complete run, refer to code 2 and 3 to do so. 
Even if the code gives the option to pick between l_attack and l_peak, this plot makes sense only with the first one. 
The plot it produces contains all 9 combinations of model-scenario, showing the trend of attack rate (in % from 0 to 100) across the years. 

@@@@@@@@@
VARIABLES:
logscale: if True sets logscale on y axis (useful for visualization)
triple: if True shows all scenarios in the same plot. Otherwise produces 3 smaller plots, one each
(net_types, timestep, scenarios, models, years, diseases, epsilons): these are lists that contain all the information about the runs. Put here the parameters you are interested in seeing boxplotted. Remember the boxplot wants ALL the years and ALL the models. The parameters in (...) above will be referred as "standard parameters" from now on


#########################
2: run epidemics iterator
#########################

This code performs the run of epidemics across all permutation of the standard parameters. Here you have the option to manually select desired ε values or instead compute them as Tdisease/Tmobility. If you do so remember that the results will be saved in a folder whose name contains ε value in its name. Use this code in conjunction with 3 to produce the desired data.
If a folder with the specified standard parameter combination already exists, the code skips the permutation to save time. Note this can produce errors later if the folder exists, but it does not contain results.dat for some reason.

###########################
3: compute metrics iterator
###########################

Does the same as 2, but it takes its output and computes the metrics relative to the desired combination of standard parameters. This code should halt if results are missing for a combination of standard parameters (check 2 above here).
After this completed, you should have l_attack.npy files in all folders of your run


!!!!!!!!!!!!
### NOTE ###

You need to run 2 and 3 before going to next codes, or to have gotten their output elsewhere. Be mindful of filepaths!


#####################
4: epsilon comparison
#####################

This code takes different epsilon runs and compares them. Files are saved with different nomenclature based on the True/False value of the following variables:

@@@@@@@@@
VARIABLES:
xlogscale: if True sets logscale on x axis (useful for visualization)
ylogscale: if True sets logscale on y axis (useful for visualization)
fit: leave it False, as the next code snippet does the fit better
mobility: if True computes f(ε) = 1 / (1 + 1/ε) and plots f(ε) instead of ε on xaxis. This is due to the fact that f(ε) should be the fraction of hosts that contribute to their own patch. 

##################
5: epsilon fitting
##################

Fits the plots seen in 4 (pick a combination of standard parameters except ε and fits log(atk_rate) vs log(ε), or atk_rate vs ε, depending on loglog value). We want a linear fit on loglog because the base hp I came up with was the one of a power law (for specific ranges of ε, given the other parameters fixed). You can adjust the range of the fit (excluding some ε values by adjusting idx value

@@@@@@@@@@
VARIABLES: 
loglog: activates logscale on both axis. 
idx: determines from which point to start fitting. The plot still shows all of them


############
6: csv maker
############

This code snippet explores all runs singularly and:
- produces a plots for each, showing on x the index of the provinces and on y the attack rate
- merges all data of these plots in a single csv file. Information there will include:
-- highest attack rate
-- average attack rate
-- std of attack rate
-- index of province with highest attack rate
Don't be scared of re running this code, since we'll take care of duplicates in later codes

@@@@@@@@@@
VARIABLES:
you can uncomment the #plt.show() line to check the plots while  the code runs, but it is very slow to do so. 


#######################################
7: study attack vs epsilon distribution
#######################################

This code takes the .csv file from 6 and explores the distribution of attack values and statistical relevant quantities vs ε

@@@@@@@@@@
VARIABLES: to edit variables here you have to edit 3 places: 
- plt.scatter
- plt.ylabel
- plt.savefig
the code is set to plot std/mean on y axis, but you can be easily use it to plot just mean or std or max values. remember to edit all 3 places to avoid confusion later


#################################################
8.1: slideshow image maker and 8: slideshow maker
#################################################

These codes are used to produce pretty slideshows making a specific quantity out of standard parameters vary while keeping the other fixed. First off, use 8.1:

8.1 produces the single images you want to use for the slideshow. Put in the lists all combinations of standard parameters you desire and let cook
I edited the italy_maps function to not show the plots and save them in a specified path. Here is the function:


def italy_maps(l_measure,d_load,savepath,doshow,cmap_min,cmap_max,title,cmap="viridis"):
    unit = list(d_load["name"].values())
    for i in range(len(unit)):
        if unit[i] == "Lombardy":
            unit[i] = "Lombardia"
        if unit[i] == "Tuscany":
            unit[i] = "Toscana"
        if unit[i] == "Piedmont":
            unit[i] = "Piemonte"
        if unit[i] == 'Valle d’Aosta':
            unit[i] = "Valle d'Aosta/Vallée d'Aoste"
        if unit[i] == 'Trentino-Alto Adige':
            unit[i] = "Trentino-Alto Adige/Südtirol"
        if unit[i] == 'Friuli Venezia Giulia':
            unit[i] = "Friuli-Venezia Giulia"
    df = pd.DataFrame([unit, list(l_measure)]).transpose()
    df.columns = ['region','quantity']
    #Download a geojson of the region geometries
    gdf = gpd.read_file(filename="/home/luca3/Desktop/PoD/stage/joint-model-parma-tobe-archived/joint-model-parma-tobe-archived/real_data/limits_IT_municipalities.geojson")
    gdf = gdf.dissolve(by='prov_acr') #The geojson is to detailed, dissolve boundaries by reg_name attribute
    #gdf = gdf.dissolve(by='reg_name')
    gdf = gdf.reset_index()
    gdf = pd.merge(left=gdf, right=df, how='left', left_on='prov_acr', right_on='region')
    gdf["quantity"] = pd.to_numeric(gdf["quantity"], errors="coerce")
    vmin,vmax = np.min(l_measure),np.max(l_measure)
    ax = gdf.plot(
        column="quantity",
        #scheme="EqualInterval",
        legend=True,
        #k=5,
        figsize=(12, 14),
        cmap=cmap,
        vmin = cmap_min, # min and max values for the colormap
        vmax = cmap_max,
        legend_kwds={
        "label": "Attack rate (%)",
        "orientation": "horizontal",
        "shrink":0.3
        },
        missing_kwds={'color': 'lightgrey'});
    ax.set_axis_off()

    ax.set_title(title, fontsize=14, pad=10)
    if (savepath != False):
        plt.savefig(savepath)
    if (doshow == True):
        plt.show()
    plt.close()
    
    
When you have your plots produced is time for 8
THere is a nested structure of for loops. The most inner one defines the quantity that will range, while the others are fixed. Right now is set to keep ε fixed and range over the years, but you may be interested in doing the opposite. 

@@@@@@@@@@
VARIABLES:
fps: defines how many frames per second. Increasing it leads the video to be faster



##########################
9: scenario model analysis
##########################

This code computes for each combination of model and scenario some statistically relevant quantities. I decided to limit my analysis on a small range of ε values. The code takes all ε values for a combination of scenario-model, computes the maximum variation of the average attack rate across the years. I used it to also compute the number of provinces that have at a specific year an attack rate higher than a fixed threshold and higher than the average atk rate, but it can be achieved easily by editing the latter for loop
