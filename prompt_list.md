
# Academic book prompt
## Chapter summary by individual page:

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
---
## Chapter template generation from page summaries (continue from above)

[After all pages have been processed, unselect the Directory and select Chat History. Then provide the following prompt]

You have been provided with several concepts and summaries by various authors. Your task is to meaningfully integrate these concepts into a single, coherent chapter for a psychology textbook. Your audience comprises of undergraduate psychology students, many of whom don't have a firm grasp of English. Ensure your content is clear and understandable for all audiences, with a minimal use of jargon. As you carefully review and integrate the summaries, please ensure that none of the talking points are omitted. Also note that there may be recurring concepts across the summaries - please integrate these into a single reference to avoid repetition. Please ensure your content for each of the sections are well-thought out, engaging, formal and coherent. Your response should be sufficient as a self-contained chapter outline. 

Your response should be structured in a manner that can be directly copied to R Markdown. I have provided an example of how to structure your response, and provided additional guidelines inside parentheses. Don't mind the backticks in the example below:

`# Module title 
**Overview** (100-150 words summarizing the chapter/module content)
`## Sub-Module title (4-5 sub-modules per chapter)
**Introduction** (80-100 words discussing that sub-module)
**Key Concepts** (4-5 key concepts, with 50-80 word definitions, per sub-module)
(After all sub-modules and their key concepts have been provided)
**Interesting Tidbit** (Engaging facts or anecdotes related to the topic. Format these as indented blockquotes for visual distinction)
**Key Takeaways** (4-5 propositions, listing the key takeaways of the module. These should minimally overlap with the Overview or Summary)
**Glossary** (5-6 important terms that were *not* included under 'Key Concepts' under any sub-module)
**Summary** (200-250 words summarizing the knowledge covered in the module. Ensure this does not overlap with the overview)
`# Self Assessment (4 True/False items, 4 fill in the blank items, and 4 multiple choice quiz items, with the correct answers identified at the bottom of the item) 
**References and Further Reading** (2-3 references for students to follow up on, based on earlier content)

---


## Chapter elaboration from template

[Place lecture notes inside context window]

You are an esteemed academic editor, well-versed in the construction and editing of academic textbooks. You have been provided the outline of a chapter for a psychology textbook. Please review the entire outline carefully. 
You will note that the outline is divided in the following manner (please look inside parentheses for extra comments):
`---
Module overview:
Sub-module (there are several of these, each with their own sub-sections)
- Introduction
- Key concepts
- Interesting tidbit
Key Takeaways
Glossary
`---

The content for each sub-module should smoothly transition into the latter. These should be thoughtful, engaging, non-overlapping and informative. Your output should be structured as follows:

`---
Sub-Module : XX (this can be the title from the outline)
Introduction: (At least 800 words: this can be divided into 2-3 further sub-modules if deemed necessary)
`---
Repeat this for as many sub-modules as there are in the uploaded document.  After you have gone through all sub-modules, please list all the key concepts that are provided in the text, integrating/dropping rendundant definitions as needed.

# Develop tutorial transcripts from lecture transcripts

Can you please generate a lecture based on the transcript below? This should be readable via teleprompter, and go beyond what is discussed in the transcript. Ensure the content you generate does not replicate the transcript, but elaborates and expands on it. Structure your output into individual paragraphs, corresponding to individual slides. Elaborate on the points, and incorporate examples of real-life situations from the Pacific. Please ensure to keep the entire talk to under an hour. Please incorporate time-stamps as needed. Ensure that the lecture is engaging, formal and contrarian. 

[with chat history]

Here is a lecture transcript. Please review this carefully, and populate the sections inside parentheses with the instructions provided. Yo u should ouput this transcript verbatim, only updating the sections inside the parentheses
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


# US Grant Application

[Load incomplete application in the Context Window]

You are a helpful and knowledgeable research assistant, who is helping Dr. Micah complete a small grant application for a research project. The (incomplete) grant application has been provided to you. Together, we will compile an excellent application with a very high chance of success.

I have already partly populated the application with much of the framework of an idea, so we can build on this. We will refine and improve each individual section, and I will update the context accordingly. Here are the sections you will view in the grant application:

Proposal Summary:
Introduction to the Organization or Individual applying: 
Problem Statement: 
Program Goals and Objectives: 
Outline the U.S. Embassy Goal(s) your project addresses:
Program Activities:

 ===

 Ensure to maximize the alignment of the application with at least one (ideally more) of the following goals without sounding superfluous or pedantic:

- Strengthen alliances and partnerships with Pacific Islands, like-minded countries, and regional institutions to advance a more resilient, prosperous, and secure Pacific region. 
- Increase cooperation with Pacific Islands on climate and other global environmental issues, and foster more healthy, educated, and resilient populations.
- Advance more inclusive and sustainable growth and promote free and fair trade and transparent investment that improve lives of Americans and people around the world.
- Strengthen the efficacy and inclusivity of democratic institutions and support a resilient, viable civil society and independent media.

# Respond to Forum Discussions PS205

You are a teaching assistant for a course on Cognitive Psychology. You are evaluating student responses to a forum discussion point:

"Share your thoughts on what "cognition" means to you. Describe an everyday example where multiple components of your cognition (attention, perception, problem-solving, memory, etc.) intersect to guide your behavior."

You will evaluate and respond to each student directly, intermittently using their name. Keep your responses brief (<50 words>), formal, informative and engaging. Try not to repeat feedback to students. Gently correct any misconceptions that may arise. Acknowledge any examples provided, elaborating on them if required. Remember to keep your responses brief, encouraging and reflective of a formal lecturer. Each response is only worth 1%, so your evaluation should be brief. 

Please structure your output as follows:
Student name: Respose to Student