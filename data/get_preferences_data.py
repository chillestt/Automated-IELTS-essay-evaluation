### This file is to get preferences data

import os
import time
import pandas as pd
import openai
import json
import numpy as np


"""
### First, find data that didnt align with real score
scores = pd.read_csv("scores.csv")

# |real_score - estimated_score| >= 1
real_score = scores.real_score
estimated_score = scores.estimated_score
diffs = np.abs(real_score - estimated_score)

hf = {"order": [0], "real_score": [0]}
for i in range(1, len(scores)):
    if diffs[i] >= 1:
        order = scores.order[i]
        rs = real_score[i]
        hf["order"].append(order)
        hf['real_score'].append(rs)

pd.DataFrame(hf, columns=["order", "real_score"]).to_csv("real_scores.csv")
"""


### read data from dataset
data = pd.read_csv("writing_task2_prompts.csv", encoding="unicode_escape")
real_scores = pd.read_csv("real_scores.csv")
API_KEY = ["Your api key"]


def append_data_to_json(filename, new_data):
    # Đọc dữ liệu hiện có từ tệp
    with open(filename, 'r') as json_file:
        data = json.load(json_file)

    # Thêm dữ liệu mới vào dữ liệu hiện có
    data.append(new_data)

    # Ghi lại dữ liệu đã cập nhật vào tệp
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def generate(input_content,real_score):
    prompt = f"re-evaluate this writing essay according to 4 criteria of IELTS writing, this one deserve a band {real_score}: {input_content}"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", temperature=0.8, messages=[{"role": "user", "content": prompt}]
    )
    return { "prompt": input_content, "evalutation": response.choices[0].message.content }


# ham xu ly loi
def send_request_with_retry(data, real_score, max_retries=5, delay=60):
    retries = 0
    while retries < max_retries:
        try:
            response = generate(data, real_score=real_score)
            return response # Trả về kết quả nếu không có lỗi
        except Exception as err:
            print(err)
            # print(f"Request rate limit exceeded, retrying in {delay} seconds...")
            time.sleep(delay)  
            retries += 1
    return None  


count = 0
key = 0
os.environ["OPENAI_API_KEY"] = API_KEY[key]

"""
- loop through each line of scores
- get real_score, order -> 
- get prompt with specific order -> 
- put that prompt into function to get data
"""


# This time, get preferences data from wrong generated data
for i in range(len(data)):
    rs = real_scores.real_score[i]
    order = real_scores.order[i]
    prompt = data["prompt"][order]
    res = send_request_with_retry(prompt, rs)
    print(res)
    with open("human_feedback_final.txt", "a", encoding="utf-8") as f:
        f.write(f"[{i}, {res}]\n")
