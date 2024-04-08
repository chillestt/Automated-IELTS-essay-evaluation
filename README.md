# A STUDY OF REINFORCEMENT LEARNING AND ITS APPLICATION IN IELTS WRITING TASK 2 EVALUATION

## Project Overview
- **Project Name:** A STUDY OF REINFORCEMENT LEARNING AND ITS APPLICATION IN IELTS WRITING TASK 2 EVALUATION
- **Team Size:** 1 (Leader: Nguyen Minh Chi)
- **Time:** December 2023 - March 2024

## Description
This project focuses on leveraging the power of Large Language Models (LLMs) and reinforcement learning techniques for automated evaluation of IELTS Writing Task 2 essays. By fine-tuning LLMs and implementing reinforcement learning algorithms, we aim to develop a robust system capable of accurately assessing the quality of IELTS essays, providing valuable feedback to test takers and educators.

## Activities
- **Web Scraping:** Gathered IELTS essays from online sources for dataset creation.
- **Synthetic Data Generation:** Utilized Gemini APIs, GPT-3.5-Turbo, and Groq for generating synthetic data to augment the dataset.
- **Model Fine-tuning:** Fine-tuned Mistral-7b, Llama-2-7b, and Gemma-7b models using QLoRA technique. Training process conducted on a single GPU, leveraging Google Colab's free T4 Tesla GPU.
- **Model Selection:** Identified Mistral-7b as the model with the best performance and forwarded it to the Direct Preference Optimization (DPO) step.
- **Preference Dataset Acquisition:** Acquired preference dataset for DPO training.
- **Fine-tuning with DPO:** Further fine-tuned the model using the preference dataset and DPO technique.

## SFT Dataset
- **Content:** Includes essays, real band scores, and evaluation metrics.
- **Size:** Over 9,000 samples.
- **Source:** All essays are sourced from real IELTS tests conducted in 2022 and 2023.
- **Link**: https://huggingface.co/datasets/chillies/IELTS-writing-task-2-evaluation

## Preference Dataset
- **Content:** Includes essays, chosen samples, and rejected samples.
- **Size:** 768 samples.
- **Link**: https://huggingface.co/datasets/chillies/IELTS_essay_human_feedback

## SFT model
- **Link**: https://huggingface.co/chillies/IELTS-fighter

## DPO model
- **Link**: https://huggingface.co/chillies/DPO_ielts_fighter

## Additional Information
For more details on the project methodology, dataset preparation, and results, please refer to the project documentation and code repository.

---
*This project was developed by Nguyen Minh Chi as part of a research study. For inquiries or collaboration opportunities, please contact [Nguyen Minh Chi](mailto:minhchi1804@gmail.com).*
