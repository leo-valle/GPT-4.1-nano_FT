# Fine-Tuning gpt-4.1-nano for Classification

## 1. Overview
This project demonstrates the process of fine-tuning the **gpt-4.1-nano** model to improve its accuracy in classifying requirements into **"functional"** and **"non-functional"** categories.  

The initial tests showed that the base model struggled with this specific task, and fine-tuning was employed as a strategy to enhance its performance on this specialized domain.  

The repository includes scripts for data preparation and for evaluating the model's accuracy both before and after the fine-tuning process.

---

## 2. The Results: A Significant Improvement
The primary goal of this project was to increase the model's accuracy. The results clearly show the success of the fine-tuning process.

| Model Version      | Correct Classifications | Total Requirements | Accuracy |
|--------------------|-------------------------|--------------------|----------|
| Base gpt-4.1-nano | 62                      | 107                | 57.94%   |
| Fine-Tuned Model   | 58                      | 71                | 81.69%   |

The fine-tuned model:  
`ft:gpt-4.1-nano-2025-04-14:ita:leonardo-valle-102087-ga-ita-br:CBiDAYf5`  
achieved an accuracy of **81.69%**, a dramatic improvement over the base model's **57.94%**.

To confirm that the fine-tuned model learned genuine semantic patterns and not just superficial correlations, an additional experiment was conducted. A new test was run using the same test dataset, but with the labels intentionally inverted (i.e., every 'functional' requirement was labeled as 'non-functional', and vice versa).

The goal was to see if the model's performance would collapse, proving it had learned the correct underlying logic.
| Model Version      | Test Condition | Accuracy |
|--------------------|----------------|----------|
| Fine-Tuned Model   |Inverted Labels | 53.52%   |

---

## 3. Repository Contents
This repository contains the following Python scripts:

- **gpt-4_1-nano_pre_FT.py**:
  The main script for evaluating the performance of the model pre fine tunning.
  It reads a test dataset, sends each requirement to the specified model via the OpenAI API, and calculate the final accuracy.

- **datasettest2_to_jsonl.py**:  
  A utility script to convert datasets from an Excel file (.xlsx) into the JSON Lines (.jsonl) format required for OpenAI's fine-tuning process.  
  It handles mapping categorical values (like `1` and `0`) to string labels ("non-functional" and "functional").

- **gpt-4_1-nano_Tunado.py**:  
  The main script for evaluating the performance of a fine-tuned model.  
  It reads a test dataset, sends each requirement to the specified model via the OpenAI API, and compares the model's prediction with the correct answer to calculate the final accuracy.

---

## 4. How to Replicate This Project

### Step 1: Prerequisites
- Python 3.7 or higher  
- An Excel file with your dataset (e.g., `dataset-test2.xlsx`) containing **Requisito** (Requirement) and **Categoria** (NF) columns.

### Step 2:  Install Dependencies
Install the necessary Python libraries using pip:

```bash
pip install pandas openpyxl openai
````
---
### Step 3: Prepare Your Data
If your training/testing data is in an Excel file, use the conversion script to create the `.jsonl` file.

1. Place your `.xlsx` file in the project directory.  
2. Make sure the column names in the script match your Excel file (or update the script).  
3. Run the converter:

```bash
datasettest2_to_jsonl.py
```
This will generate a `dataset-convertido.jsonl` file, which you can use for fine-tuning or testing.

Obs: the file `dataset_unido.jsonl` was created manually.

---

### Step 4: Configure the Accuracy Checker
Open the `gpt-4_1-nano_Tunado.py` script and update the following configuration variables at the top of the file:

```python
# 1. Paste your OpenAI API key.
API_KEY = "xj-..."

# 2. Paste the full ID of your fine-tuned model.
FINE_TUNED_MODEL_ID = "ft:gpt-4.1-nano-..."

# 3. Set the name of your test dataset file.
TEST_DATASET_FILE = 'dataset-convertido.jsonl'

```

### Step 5: Run the Evaluation
Execute the script from your terminal to start the evaluation process.


