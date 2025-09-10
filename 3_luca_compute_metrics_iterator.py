import subprocess
import time
from tqdm import tqdm

# Base command (without model and year, those will be added dynamically)
base_cmd = [
    "/home/luca3/Desktop/PoD/coding_env/bin/python",
    "/home/luca3/Desktop/PoD/stage/joint-model-parma-tobe-archived/joint-model-parma-tobe-archived/compute_metrics_main.py",
    "--disease", "DENV",
    "--netType", "provinces",
    "--timeStep", "2000",
    "--day_to_stamp=123"
]

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

# Loop over combinations

try:
    for year in years:
        for model in models:
            for scenario in scenarios:
                for epsilon in epsilons:
                    cmd = base_cmd + ["--model", model, "--year", str(year), "--scenario",str(scenario), "--epsilon",str(epsilon)]
                    print(f"\n>>> Running: {' '.join(cmd)}")  # just to track what’s happening
                    # Start process
                    start_process_time = time.time()
                    process = subprocess.Popen(cmd)

                    # Show tqdm until process finishes
                    with tqdm(total=0, bar_format="{l_bar}{bar} | Elapsed: {elapsed}") as pbar:
                        while process.poll() is None:  # still running
                            time.sleep(1)
                            pbar.update(0)  # refresh display

                    if process.returncode == 0:
                        print("✅ Finished successfully")
                    else:
                        print(f"❌ Run failed with code {process.returncode}")
                    print(f"Process elapsed time: {round(time.time()-start_process_time,3)}")

except KeyboardInterrupt:
    print("\n⏹️ Stopped by user.")
