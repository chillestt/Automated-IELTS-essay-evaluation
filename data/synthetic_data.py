from dotenv import load_dotenv
load_dotenv()
import time
import pandas as pd

import os 
import google.generativeai as genai


generation_config = {
    "temperature": 0.8,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 5000
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
]

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.0-pro-latest", 
                              generation_config=generation_config,
                              safety_settings=safety_settings
                              )

## prompt
prompt = """
The score of the essay below is **{}**. Evaluate this essay that aligns with the score provided.
----------------
In this task, you are required to evaluate an IELTS Writing Task 2 essay. Consider the following four criteria and provide a detailed assessment for each, along with a suggested band score:

## Task Achievement:
- Evaluate the extent to which the candidate has effectively addressed the given task.
- Assess the clarity, relevance, and coherence of ideas presented in response to the task.
- Identify whether all aspects of the task have been adequately covered and supported with appropriate arguments and evidence.
- Provide feedback on the candidate's ability to fulfill the requirements of the task.
- Suggested Band Score (Task Achievement): [Insert Score]

## Coherence and Cohesion:
- Analyze the clarity and fluidity of transitions between sentences and paragraphs.
- Assess the effectiveness of connecting words and phrases in maintaining a smooth progression of ideas.
- Evaluate the logical sequence and arrangement of information throughout the essay.
- Provide feedback on the overall organization and structural integrity of the text.
- Suggested Band Score (Coherence and Cohesion): [Insert Score]

## Lexical Resource (Vocabulary):
- Examine the range and accuracy of vocabulary used in the essay.
- Point out specific mistakes in vocabulary, such as inaccuracies or overuse of certain words and Suggest modified versions or alternatives for the identified mistakes. [list of mistakes and rectify]
- Assess the appropriateness of vocabulary for the given context.
- Suggested Band Score (Lexical Resource): [Insert Score]

## Grammatical Range and Accuracy:
- Evaluate the variety and complexity of sentence structures.
- Point out specific grammatical errors, such as incorrect verb forms or sentence construction and Suggest modified versions or corrections for the identified mistakes. [list of mistakes and rectify]
- Examine the use of punctuation and sentence formation.
- Suggested Band Score (Grammatical Range and Accuracy): [Insert Score]

## Overall Band Score:
- Provide an overall band score for the essay, considering the holistic performance across all criteria.
- Consider the synergy of the essay in meeting the task requirements cohesively.
- Suggested Overall Band Score: [Insert Score]

## Feedback and Additional Comments:
- Provide constructive feedback highlighting specific strengths and areas for improvement.
- Suggest strategies for enhancement in weaker areas.


## Prompt:
{}

## Essay:
{}

## Evaluation:"""


## get data
ielts_essays = pd.read_csv("ielts_writing.csv", lineterminator='\n')
ielts_essays.drop(columns=["Unnamed: 0"], inplace=True)

###########################################
# CSV file name
csv_file = 'fffffffffffffffffffffffffffffffffffffffffff.csv'

# Read the existing CSV file or create a new one if it doesn't exist
try:
    df = pd.read_csv(csv_file, lineterminator='\n')
except FileNotFoundError:
    df = pd.DataFrame(columns=["prompt", "essay", "evaluation", "band"])

headers = list(df.columns)
# ############################################
count = 0
essay_idx = 3387
l = len(ielts_essays) + 1

while essay_idx < 5000:
    try:
        sample = ielts_essays.iloc[essay_idx]
        sample_prompt = prompt.format(sample.band, sample.question, sample.essay)
        response = model.generate_content(sample_prompt)

        print(f"Essay id: {essay_idx}")
        print(response.text)
        print("\n=====================\n")

        data_row = [sample.question, sample.essay, response.text, sample.band]
        sample_df = pd.DataFrame(data_row)

        idx = len(df)
        df.loc[idx] = data_row
        df.to_csv(csv_file, index=False)
        essay_idx += 1
    except:
        print("Something wrong happened")
        count += 1
        essay_idx += 1
        if count == 5:
            break

        