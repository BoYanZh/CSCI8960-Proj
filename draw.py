# draw a acc and loss graph from log

import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import glob


def draw(log_file):
    name = log_file.split("/")[-2]
    print("drawing " + name)
    lines = open(log_file).readlines()
    index = 0
    for i, line in enumerate(lines):
        if "============ Initialized logger ============" in line:
            index = i
    lines = lines[index:]
    logs = [
        json.loads(line.split("__log:")[1].strip())
        for line in lines
        if "test_acc_ema" in line and "final_train_acc_ema" not in line
    ]

    test_acc = [log["test_acc_ema"] for log in logs]
    train_acc = [log["train_acc_ema"] for log in logs]

    df = pd.DataFrame(
        {
            "nb_steps": np.arange(0, len(test_acc) * 100, 100).tolist() * 2,
            "accuracy": test_acc + train_acc,
            "type": ["test"] * len(test_acc) + ["train"] * len(train_acc),
        }
    )
    sns.set_style("whitegrid")
    sns.lineplot(x="nb_steps", y="accuracy", hue="type", data=df)

    plt.savefig("draw/" + name + ".png")
    plt.clf()


if __name__ == "__main__":
    for file in glob.glob("dump-*"):
        draw(file + "/train.log")
