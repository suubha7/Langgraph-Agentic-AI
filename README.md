## **LangGraph** 
---

### **Basic LangGraph**
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
