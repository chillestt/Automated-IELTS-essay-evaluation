### This file is to clean, process, and save data

import pandas as pd 
import re


with open("human_feedback_final.txt", "r") as f:
    data = f.readlines()


rejected_eval = pd.read_csv("ielts_writing_evaluation.csv")
real_scores = pd.read_csv("real_scores.csv")


def convert_line(line, index):
    num = re.findall(r"[-+]?(?:\d*\.*\d+)", line)[0]    # get order
    line = line.split(", {")[1]     # get content
    idx = line.index("evalutation")     # get index
    prompt = line[:idx-2]       # get prompt
    evaluation = line[idx-2:]   # get evaluaton
    idp = prompt.index(":")
    prompt = prompt[idp + 3:] # remove the word "prompt" from the prompt

    # rejected = rejected_eval["evaluation"][rejected_eval["prompt"] == prompt]

    order = real_scores["order"][i]
    rejected = rejected_eval["evaluation"][rejected_eval["order"] == order].values[0]

    ide = evaluation.index(":")
    evaluation = evaluation[ide+1:][:-4]

    return {"order": num, "prompt": prompt, "chosen": evaluation, "rejected": rejected}

results = []
for i in range(len(data)):
    line = data[i]
    result = convert_line(line, i)
    results.append(result)

result = pd.DataFrame(results, columns=["order", "prompt", "chosen", "rejected"])
print(result.head())
print(len(result))
result.to_csv("human_feedback.csv")
