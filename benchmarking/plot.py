import matplotlib.pyplot as plt
import csv

def plot(async_results_file, sync_results_file, partially_sync_results_file, save_to="./benchmarking/results.png"):
    sync_results = []
    partially_sync_results = []
    async_results = []
    with open(sync_results_file, "r") as file:
        reader = csv.reader(file)
        next(reader)
        sync_results.extend(reader)
    with open(partially_sync_results_file, "r") as file:
        reader = csv.reader(file)
        next(reader)
        partially_sync_results.extend(reader)

    with open(async_results_file, "r") as file:
        reader = csv.reader(file)
        next(reader)
        async_results.extend(reader)

    plt.plot([res[0] for res in sync_results], [round(float(res[2]), 2) for res in sync_results], label="sync", color="red")
    plt.plot([res[0] for res in partially_sync_results], [round(float(res[2]), 2) for res in partially_sync_results], label="partially sync", color="green")
    plt.plot([res[0] for res in partially_sync_results], [round(float(res[2]), 2) for res in async_results], label="async", color="blue")

    plt.title(f"Tested on {sync_results[0][1]} files")
    plt.legend()
    plt.xlabel("Experiment numbers")
    plt.ylabel("Time in seconds")
    plt.savefig(save_to)

if __name__ == "__main__":
    plot("./benchmarking/async_results.csv", "./benchmarking/fully_sync_results.csv", "./benchmarking/partially_sync_results.csv")
