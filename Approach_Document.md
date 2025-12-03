# AI Agent Assignment — Approach Document

## SECTION 1: BASIC DETAILS
**Name:** Anusha Rallabandi (placeholder — replace if needed)  
**AI Agent Title / Use Case:** ExamBuddy — AI Agent to help college students revise for exams

---

## SECTION 2: PROBLEM FRAMING

**1.1 What problem does your AI Agent solve?**  
ExamBuddy helps students quickly create concise revision plans, generate targeted practice questions, and produce short summaries of topics to speed up last-minute study sessions.

**1.2 Why is this agent useful?**  
It reduces time spent deciding what to study, turns vague requests ("I need to revise calculus") into structured revision steps, and provides active recall prompts (practice questions).

**1.3 Who is the target user?**  
Undergraduate engineering students preparing for midterms or finals who need focused, topic-level revision materials and quick practice questions.

**1.4 What not to include?**  
- No deep tutoring or step-by-step solutions for complex proof derivations.  
- No access to student's private files or LMS.  
- No long-form lecture generation (> 1000 words).

---

## SECTION 3: 4-LAYER PROMPT DESIGN

### 3.1 INPUT UNDERSTANDING
**Prompt (final):**

```
SYSTEM: You are Input-Interpreter. Your job: read the user's message and extract:
- intent (one of: revise_topic, generate_quiz, summarize_notes, schedule_plan, unclear)
- subject (e.g., "Calculus", "Data Structures")
- topic_scope (short phrase or list, e.g., "integration techniques", "binary trees")
- desired_output_type (summary, 5q_quiz, flashcards, study_plan)
- urgency (now/today/this week)
- user_level (high-school / undergraduate / postgraduate) if provided
Return a strict JSON object with keys: intent, subject, topic_scope, desired_output_type, urgency, user_level, confidence (0-1), clarifying_question (null if none).
EXAMPLE USER: "Help me revise integration by parts for tomorrow exam" 
-> produce JSON.
```

**Responsibility:** Converts free-form user text into a structured intent + parameters JSON that the agent can act on.

**Example Input + Output:** (see `prompts_and_examples/input_understanding_example.json`)

---

### 3.2 STATE TRACKER
**Prompt (final):**

```
SYSTEM: You are State-Tracker. Maintain a small session memory for the user in JSON with fields:
- recent_subject (last subject requested)
- recent_topics (list of up to 6 recent topic scopes)
- last_quiz (metadata: subject, topic_scope, num_questions)
- preferences (study_duration_minutes, preferred_formats e.g., ["flashcards","quizzes"])
Given a new action JSON from Input-Interpreter, update the state and return the updated JSON. If nothing to update, return the unchanged state.
```
**How it remembers:** Simulated memory via a JSON object stored across agent turns (in our demo this is saved to `state.json`).

---

### 3.3 TASK PLANNER
**Prompt (final):**

```
SYSTEM: You are Planner. Input: interpretation JSON and current state JSON.
Output: a step-by-step plan (array) of internal subtasks. Each step object: {step_id, action_type, description, required_params}.
Planner should:
1) Validate interpretation (if confidence < 0.6, add clarifying_question step).
2) Map desired_output_type to generator actions.
3) If urgency == "now" or "tomorrow", include time-limited plan (e.g., 30-60 minute revision plan).
4) Return planner JSON with fields: plan_steps (array), estimated_time_minutes, needs_clarification (bool), clarification_text (if any).
```
**How it helps:** Breaks down the request into deterministic tasks the Output Generator will fulfill.

---

### 3.4 OUTPUT GENERATOR
**Prompt (final):**

```
SYSTEM: You are Output-Generator. Input: planner JSON + interpretation JSON + state JSON.
Produce the final user-facing message. Requirements:
- Start with a 1-line summary of what you'll deliver.
- If providing study plan: give bullet list with timings (e.g., 0-30m: Topic A review; 30-50m: Practice questions).
- If providing quiz: present questions numbered, and include an "Answer key" collapsed (labelled and separated clearly).
- Tone: supportive, concise, motivating.
- Limit: final message <= 300 words for summaries, <= 10 questions for quizzes.
- End by asking one clear follow-up question to continue the session.
Return plain text output only.
```
**Formatting/Tone:** Concise, actionable, friendly; use markdown for bullets and code blocks where needed.

---

## SECTION 4: CHATGPT EXPLORATION LOG

| Attempt | Prompt Variant | What Happened | What You Changed | Why |
|---|---:|---|---|---|
| 1 | Simple "Generate quiz" | Output generic, not topic-aware | Added Input-Understanding layer | To extract topic and urgency |
| 2 | Added planner layering | Planner produced steps but no time mapping | Added urgency handling in Planner | To support "tomorrow" flows |
| 3 | Final prompts above | Produced structured outputs in testing | N/A | Stabilized behavior |

(More detailed logs + transcripts are in `chat_logs.txt` file.)

---

## SECTION 5: OUTPUT TESTS (SAMPLES)

**Test 1: Normal input**  
Input: "Help me revise integration by parts for tomorrow's exam, 45 minutes."  
Output (sample):
```
Summary: 45-minute revision plan for Integration by Parts (Calculus).

0-10m: Quick concept review — formula, when to use.
10-25m: Walk through one example (set up integrals + substitution).
25-40m: 5 short practice questions (no solutions shown).
40-45m: Quick summary + 3 memory-check flashcards.

Would you like the practice questions now (answers after you attempt)?
```

**Test 2: Vague input**  
Input: "Give me something to practice for data structures"  
Output (sample):
```
I can help — do you want a quick summary, a 30-minute plan, or a 5-question quiz? Which subject and topic (e.g., 'binary trees', 'hash tables')?
```

**Test 3: Empty input**  
Input: ""  
Output (sample):
```
I didn't get any topic. What subject or topic would you like to revise? Example: "Calculus — integration techniques"
```

---

## SECTION 6: REFLECTION

**6.1 Hardest part:** Designing prompts that separate responsibilities cleanly — avoiding duplicate behavior between planner and generator.  
**6.2 Enjoyed:** Thinking about the step-wise planner and creating short, practical study plans.  
**6.3 If more time:** Implement multi-turn state persistence, web scraping of syllabus outlines, and small web UI.  
**6.4 Learned about ChatGPT/prompt design:** Clear role separation (Input->Planner->Output) reduces hallucination and makes outputs testable. Small, strict JSON outputs from the Input layer improve reliability.  
**6.5 Stuck?** Yes — tuning confidence thresholds. Resolved by adding clarifying question steps in Planner.

---

## SECTION 7: HACK VALUE
- Included a simulated `state.json` memory.  
- Provided a minimal example Python file showing how the 4 prompts can be combined locally.

---