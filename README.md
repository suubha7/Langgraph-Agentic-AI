## **LangGraph** 
---

## **Basic LangGraph**
**Scenario: Text Processor**

**Task:**

1. Takes user text input
2. Counts the number of words
3. Converts text to uppercase
4. Adds a timestamp
5. Returns the processed result

**Requirements:**

- Use StateGraph
- Create 3 nodes (count_words, uppercase, add_timestamp)
- Linear flow: entry → count → uppercase → timestamp → END
- No conditions, no loops, just straight flow
---

**Scenario: AI Content Summarizer**

Build a graph that takes long articles and creates smart summaries.

**Task:**

1. Extract key sentences using LLM
2. Analyze sentiment (positive/negative/neutral) using LLM
3. Generate 3-sentence summary using LLM

**Requirements:**

- Use OpenAI/Anthropic LLM in nodes
- Linear flow: extract → sentiment → summarize → END
- State: article_text, key_points, sentiment, summary
---

## AI Recruiter Screener

### Overview
This project implements an **AI-powered job application screener**. It processes resumes step-by-step, evaluates candidates against job requirements, and generates interview questions, emails, and summaries.

### Workflow
The pipeline runs through the following nodes:

1. **Extract Candidate Info**  
   - Input: `resume_text`  
   - Output: `candidate_info` (name, current_role, years_of_experience, skills, education)

2. **Match Skills Against Job Requirements**  
   - Compares candidate skills with `job_requirements`  
   - Output: `skill_match_score` (0–10) + `missing_skills`

3. **Evaluate Experience Relevance**  
   - Scores candidate’s experience vs. job description  
   - Output: `experience_score` (0–10)

4. **Generate Interview Questions**  
   - Based on missing skills and weak experience areas  
   - Output: `questions`

5. **Write Personalized Email**  
   - Invitation if scores ≥ 7, otherwise rejection with encouragement  
   - Output: `email`

6. **Create Evaluation Summary**  
   - Consolidates all results into a structured summary  
   - Output: `summary`

### State Variables
The pipeline maintains the following state:
- `resume_text`  
- `candidate_info`  
- `skill_match_score`  
- `experience_score`  
- `questions`  
- `email`  
- `summary`

### Example
**Resume (demo):**
- Priya Sharma, 4 years experience, Python, SQL, AWS, FastAPI, Flask, B.Tech CS

**Job Requirement (demo):**
- Backend Engineer, 3–5 years, Python, SQL, AWS, Docker, Git, FastAPI/Flask

### Usage
- Feed `resume_text` and `requirements` into the pipeline.  
- Each node prompt depends on the previous node’s output.  
- Final output: structured evaluation summary + personalized email.
---

## AI News Aggregator

This project is a lightweight news‑summarization workflow built with **LangGraph**, **LangChain tools**, and a custom **AWS LLM**.

**It fetches news from:**
- DuckDuckGo Search  
- Google News RSS  
- Reddit public posts  

All sources run in parallel, and the final node uses an LLM to generate a clean, unified summary.

**How It Works**
1. User provides a query  
2. Workflow fetches news from all sources  
3. Text is cleaned and normalized  
4. LLM produces a concise final summary  

**Run Example**
```python
query = {"query": "ai trends today"}
response = workflow.invoke(query)
print(response["final_response"])
```
**Purpose:**

A simple, modular pipeline for aggregating and summarizing news using multiple sources and an LLM.
---