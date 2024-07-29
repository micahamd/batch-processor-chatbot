
# Chapter writing pipeline
# Chapter summary by individual page:

Please process this page from a chapter on [], which part of a textbook on []. Your task is to summarize this content in a manner comprehensible and digestible to undergraduate students. Your content should comprise of the following:

- A header that briefly encapsulates the page
- A 500-600 word summary of the page. This should not exceed 3 paragraphs.
- 2-3 key concepts that were provided in the page, with a brief exposition of each.

Please ensure that your summary is formal, direct, informative and engaging. Your output should be structured as follows:

***
Header:
Summary: (500-600 words)
Key Concepts: (2-3)
References: (1-2)
***
# Generate lectures from slides

**Prompt for GPT:**

---

**Task Overview:**

You will be processing a PDF file containing a lecture on [insert specific topic area, e.g., "Cognitive Development in Adolescence"]. Your goal is to create a [insert intended duration, e.g., "30-minute"] lecture transcript that complements the PDF content.

**Instructions:**

1. **PDF Processing:**
   - Carefully analyze each slide in the provided PDF. Pay attention to the key talking points and any additional information presented.

2. **Transcript Creation:**
   - Based on your analysis, generate a transcript that is structured around the individual slides.
   - Each section of the transcript should correspond to a slide from the PDF, and you should include timestamps indicating where each segment falls within the overall lecture duration.

3. **Audience Consideration:**
   - The intended audience is undergraduate psychology students, some of whom may have limited English proficiency. Ensure that your language is clear and accessible.
   - Avoid overly complex terms and keep your language formal yet engaging, using minimal adjectives and without superfluous terminology.

4. **Formatting Requirements:**
   - Divide the transcript into clearly defined sections, each with a subheader that identifies the slide topic.
   - Maintain a neat structure with coherent paragraphs for easy readability.

**Output Example Format:**

- **[Timestamp: HH:MM] Slide Title 1**
  
  [Content related to slide 1...]
  
- **[Timestamp: HH:MM] Slide Title 2**
  
  [Content related to slide 2...]
  
- **[Timestamp: HH:MM] Slide Title 3**
  
  [Content related to slide 3...]

**Final Note:**
Please ensure your transcript not only reflects the information from the slides but also conveys it in a manner that is engaging and easy to understand for the target audience. 
# Generate Forum Discussions and 16 Quiz questions (for PS205)

[Place transcript in context window, and produce the following prompt]

This is the week's lecture transcript. Please process this carefully, and output the following:

1. A short (<50 words) forum discussion point based on the provided transcript. This should be a simple instruction, directly addressed to the students, that asks them to explore a particular topic/relation from the previous week's lecture. This should be related to the transcript, and encourage self-reflection. It should also be structured in a way that the instructor need not necessarily respond to the discussion. Note that each forum discussion is only worth 1% of the student's grade, so the expected response will be quite brief (<100 words). Please ensure your forum discussion point meets these criteria.

2. Generate 12 multiple choice quizzes (4 options each) and 4 true/false items, so a total of 16 test items. Please markthe correct answer for each test item, and justify why that answer was correct relative to the remaining options under each test item. Please ensure that the questions are well-constructed, and pertain directly to the provided transcript.

# QOT assessment from Lecture transcript

[Use gemini flash. Place QOT document in context, and lecture transcript in batch directory]

---

You are a Learning Observer tasked with evaluating a lecture based on the criteria listed. Your output should respond to each of the items in the Quality of Teaching Classroom Observation Checklist based on the transcript you assess. 

Specifically, your output should provide good scores for each of the components described. Elaborate the final remarks appropriately, being concise and favorable. The final remark should conclude with a recommendation for promotion based on teaching quality.

--

[Unselect Context and Batch Directory, then select Chat History and include the following prompt]

--

You have been provided a Classroom Observation Checklist, completed for the evaluation of Mr. Orban.

I would like you to re-organize this content, without omitting anything. 

You'll note the separate headings marked out in MD format, using '###'. Under each header, there are individual queries, and single sentence responses to those queries. I want you to parse all the responses to all individual queries under each header into a single, brief and comprehensive paragraph that addresses all the points. You can leave the score for each section as is. Your output should therefore be structured as:

---

`### Header

{Paragraph summarizing remarls}

Point score (X out of X)

---



 