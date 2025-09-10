import cv2
import glob

# all possibilities to parse
net_types = ["provinces"]
diseases = ["DENV"]
timestep = 2000
models = ["MRI-ESM2-0", "CESM2", "ACCESS-CM2"]  # put your models here
years = [2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]  # put your years here
scenarios = ["SSP1-2.6", "SSP2-4.5","SSP5-8.5"]

# all analyzed epsilon at 8-9-2025
#epsilons = ["0.0001","0.0005","0.001","0.005","0.01","0.0208","0.0292","0.03","0.0312","0.0333","0.0375","0.04","0.0417","0.0437","0.05","0.0563","0.0583","0.0625","0.0667","0.075","0.0833","0.1","0.25","0.5","0.75","1.0","1.25","1.5","1.875","2.0","2.5","3.0","3.75","4.5","5.0","5.625","6.0","6.25","7.5","9.375","10.0","12.5","30.0"] #,"100.0","10000.0"]
epsilons = ["0.0001","0.0005","0.001","0.005","0.01","0.05","0.1","0.25","0.5","0.75","1.0","2.0","3.0","5.0","10.0","30.0"]

sel_disease = diseases[0]
sel_scenario = scenarios[0]
sel_model = models[0]
sel_epsilon = epsilons[0]
sel_year = years[0]

image_paths = []
for sel_epsilon in epsilons:
    for sel_model in models:
        for sel_scenario in scenarios:
            for sel_disease in diseases:
                image_paths  = []
                for sel_year in years:
                    image_path = f"/home/luca3/Desktop/PoD/stage/luca_plots/all_prov_results/{sel_disease}_{timestep}_{sel_scenario}_{sel_model}_{sel_year}_{sel_epsilon}_all_italy.png"
                    image_paths.append(image_path)

                # List of images sorted by filename
                img_files = image_paths

                # Read the first image to get size
                frame = cv2.imread(img_files[0])
                height, width, layers = frame.shape

                # Define video writer
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or 'XVID'
                video = cv2.VideoWriter(f'/home/luca3/Desktop/PoD/stage/{sel_disease}_{sel_scenario}_{sel_model}_{sel_epsilon}_epsilon_italy_slideshow_yearly.mp4', fourcc, 1.5, (width, height))  

                # Add frames
                for img_file in img_files:
                    img = cv2.imread(img_file)
                    video.write(img)

                video.release()
                cv2.destroyAllWindows()