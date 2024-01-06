import os
import time
import pandas as pd
import openai
import json

data = pd.read_csv("writing_task2_prompts.csv", encoding="unicode_escape")
API_KEY = ["YOUR OPENAI API KEY"]

def append_data_to_json(filename, new_data):
    # Đọc dữ liệu hiện có từ tệp
    with open(filename, 'r') as json_file:
        data = json.load(json_file)

    # Thêm dữ liệu mới vào dữ liệu hiện có
    data.append(new_data)

    # Ghi lại dữ liệu đã cập nhật vào tệp
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def generate(input_content):
    prompt = f"Evaluate this writing essay according to 4 criteria of IELTS writing, and suggest band score: {input_content}"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", temperature=0.8, messages=[{"role": "user", "content": prompt}]
    )
    return { "prompt": input_content, "evalutation": response.choices[0].message.content }


# ham xu ly loi
def send_request_with_retry(data, max_retries=5, delay=60):
    retries = 0
    while retries < max_retries:
        try:
            response = generate(data)
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
for i in range(125, 200):
    count += 1
    # os.environ["OPENAI_API_KEY"] = API_KEY[key]
    prompt = data["prompt"][i]
    res = send_request_with_retry(prompt)
    print(res)
    if count == 3:
        count = 0
        # key = (key + 1) % len(API_KEY)
        # os.environ["OPENAI_API_KEY"] = API_KEY[key]
    with open("results.txt", "a", encoding="utf-8") as f:
        f.write(f"[{i}, {res}]\n")