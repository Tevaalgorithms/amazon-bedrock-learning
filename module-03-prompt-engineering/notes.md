# Module 03 — Prompt Engineering

## What is Prompt Engineering?

**Prompt engineering** is the practice of designing prompts that elicit better responses from language models.

Better prompts = better outputs = lower costs (fewer retries)

## Core Principles

### 1. Be Specific, Not Vague

**Bad:**
```
Explain AI
```

**Good:**
```
Explain machine learning in 2 sentences, focusing on how it differs from traditional programming.
```

### 2. Provide Context

**Bad:**
```
What should I do?
```

**Good:**
```
I'm building a web app and need to decide between React and Vue. The team has 2 React experts and 0 Vue experts. What should I do?
```

### 3. Give Examples (Few-Shot Learning)

```
Classify these sentences as positive or negative:

Example 1: "I love this product!" → Positive
Example 2: "This is terrible." → Negative

Now classify: "It's okay, nothing special."
```

### 4. State the Format

**Bad:**
```
Summarize this document
```

**Good:**
```
Summarize this document in JSON format with keys: title, key_points (list), recommendation
```

## System vs User Messages

### System Message
The "instruction set" for the model. Set once, affects all user messages.

```python
{
    'system': 'You are a Python expert. Answer all questions with code examples.',
    'messages': [
        {'role': 'user', 'content': 'How do I read a file?'}
    ]
}
```

### User Message
The actual question or task.

```python
{
    'messages': [
        {'role': 'user', 'content': 'How do I read a file?'}
    ]
}
```

## Techniques

### 1. Chain of Thought (CoT)

Ask the model to show its reasoning step-by-step.

**Without CoT:**
```
If Tom has 5 apples and gives 2 to Jane, how many does he have?
```
Answer: "3 apples"

**With CoT:**
```
If Tom has 5 apples and gives 2 to Jane, how many does he have?
Think step by step:
1. Tom starts with 5 apples
2. He gives 2 to Jane
3. So he has 5 - 2 = 3 apples

How many apples does Tom have?
```
Answer: "Tom starts with 5 apples. He gives 2 to Jane, so 5 - 2 = 3 apples. Tom has 3 apples remaining."

CoT improves accuracy on complex problems.

### 2. Role-Playing

```
You are a customer support agent for an e-commerce platform.
A customer is complaining that their order arrived damaged.
Respond professionally and offer a solution.

Customer: "My laptop arrived with a cracked screen!"
```

### 3. Structured Output

Tell the model the exact format you want:

```
Analyze this code and respond in JSON:
{
    "has_bugs": true/false,
    "bug_description": "string",
    "fix": "string",
    "severity": "low/medium/high"
}

Code:
def divide(a, b):
    return a / b
```

### 4. Few-Shot Learning

Provide examples before the actual task:

```
Translate English to French:

Example 1: "Hello" → "Bonjour"
Example 2: "Good morning" → "Bon matin"
Example 3: "How are you?" → "Comment allez-vous?"

Now translate: "Thank you very much"
```

### 5. Constraint-Based

```
Answer the question in exactly 50 words or less.
Use simple language, no technical jargon.
Include at least one example.

What is machine learning?
```

## Common Pitfalls

### 1. Being Too Wordy
Longer prompts = more tokens = higher cost. Be concise.

### 2. Negative Instructions
Instead of "Don't be rude", say "Be polite and professional"

### 3. Assuming Context
The model doesn't know your codebase. Provide snippets.

### 4. Ignoring Edge Cases
```
Bad: "Summarize this customer feedback"
Good: "Summarize this customer feedback. If the feedback is not constructive, note that. If it contains a bug report, extract the bug details."
```

## Anthropic Messages API (Claude)

Claude uses the Messages API format:

```python
{
    'anthropic_version': 'bedrock-2023-06-01',
    'max_tokens': 1024,
    'system': 'You are a helpful assistant.',
    'messages': [
        {
            'role': 'user',
            'content': 'What is 2+2?'
        }
    ]
}
```

### System Prompt Best Practices

**Be explicit about:**
- Your role: "You are a Python code reviewer"
- Your constraints: "Keep responses under 100 words"
- Your style: "Use casual, friendly tone"
- Your values: "Prioritize user privacy and security"

Example:
```python
{
    'system': '''You are a senior Python engineer reviewing code.
Your role:
- Check for bugs, security issues, and style problems
- Provide constructive feedback

Format your response as:
1. Issues found (if any)
2. Suggested fixes
3. Code quality score (1-10)
4. Learning resource (if relevant)

Keep feedback professional and encouraging.''',
    'messages': [...]
}
```

## Tool Use (XML Tags)

Claude understands XML tags for structured requests:

```python
{
    'messages': [
        {
            'role': 'user',
            'content': '''<customer_support_context>
Customer: "I can't log in"
Account status: Active
Last login: 3 days ago
</customer_support_context>

Suggest 3 troubleshooting steps. Be concise and professional.'''
        }
    ]
}
```

## Temperature and Randomness

**Temperature:** Controls randomness of responses

- `temperature: 0.0` — Deterministic (same answer every time)
- `temperature: 1.0` — Creative (varied answers)
- `temperature: 2.0` — Very creative (wild, sometimes nonsensical)

```python
{
    'system': 'You are a helpful assistant.',
    'max_tokens': 100,
    'temperature': 0.0,  # Deterministic for factual tasks
    'messages': [...]
}

# vs

{
    'system': 'You are a creative storyteller.',
    'max_tokens': 100,
    'temperature': 1.0,  # Creative for story generation
    'messages': [...]
}
```

## Prompt Optimization Workflow

1. **Write a baseline prompt** — clear but not perfect
2. **Test it** — run on 5-10 examples
3. **Measure** — accuracy, speed, cost
4. **Iterate** — refine based on failures
5. **A/B test** — try 2 variations, measure impact

## Example: Customer Complaint Classification

**V1 (Baseline):**
```
Classify this complaint as Product, Shipping, or Service.
Complaint: "Package arrived 2 days late"
```

Result: "Shipping" ✓ (works, but add guardrails)

**V2 (Better):**
```
Classify this customer complaint. Respond in JSON.

Categories:
- Product: About item quality, defects, or features
- Shipping: About delivery, delays, or packaging
- Service: About customer service, refunds, or returns

Complaint: "Package arrived 2 days late"

Response format:
{
    "category": "Shipping" or "Product" or "Service",
    "confidence": 0.0-1.0,
    "reason": "brief explanation"
}
```

Result:
```json
{
    "category": "Shipping",
    "confidence": 0.95,
    "reason": "Complaint explicitly mentions late delivery"
}
```

Better: structured output, confidence score, reasoning.

## Gotchas

### 1. Token Counting
Your prompt counts towards input tokens. Long system prompts = higher costs.

### 2. Language Drift
If you use Claude in French, subsequent mentions of English might be ignored. Be explicit.

### 3. Model Updates
Prompt quality can change when model versions update. Re-test after updates.

## Next Steps

Module 03 project: Build a prompt optimization framework that tests variations.

## Resources

- **Anthropic Prompt Guide:** https://docs.anthropic.com/en/docs/build-a-bot
- **Best Practices:** https://docs.anthropic.com/en/docs/build-a-bot
- **Bedrock Prompt Engineering:** https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-engineering.html
