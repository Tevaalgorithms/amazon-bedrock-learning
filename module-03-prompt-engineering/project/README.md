# Module 03 Project — Prompt Optimization Framework

## Goal

Build a framework that tests multiple prompt variations against the same task and scores results. This teaches you how to iteratively improve prompts.

## Implementation

Create `prompt_optimizer.py`:

```python
import boto3
import json

client = boto3.client('bedrock-runtime', region_name='us-east-1')
model_id = 'anthropic.claude-3-5-haiku-20241022-v1:0'

# Define prompt variations
PROMPTS = {
    'baseline': {
        'system': 'You are a helpful assistant.',
        'user': 'Summarize quantum computing in 1 sentence.'
    },
    'detailed': {
        'system': 'You are a quantum physics expert. Explain concepts clearly.',
        'user': 'Summarize quantum computing in 1 sentence. Focus on how it differs from classical computing.'
    },
    'structured': {
        'system': 'You are an expert. Respond in JSON format.',
        'user': '''Summarize quantum computing. Respond in JSON:
{
    "summary": "1 sentence",
    "key_concepts": ["concept1", "concept2"],
    "applications": ["app1", "app2"]
}'''
    }
}

def invoke_with_prompt(system: str, user: str) -> str:
    # TODO: Create request for this prompt
    # TODO: Invoke model
    # TODO: Extract response text
    # TODO: Return response
    pass

def score_response(response: str, rubric: dict) -> float:
    """Score response based on rubric criteria."""
    # TODO: Implement scoring logic
    # Rubric might include: length, clarity, technical accuracy
    pass

def main():
    rubric = {
        'clarity': 0.4,
        'accuracy': 0.4,
        'conciseness': 0.2
    }

    results = {}
    for name, prompt in PROMPTS.items():
        response = invoke_with_prompt(prompt['system'], prompt['user'])
        score = score_response(response, rubric)
        results[name] = {
            'response': response,
            'score': score
        }

        print(f"\n{name.upper()}:")
        print(f"Response: {response}")
        print(f"Score: {score}/10")

    print("\nBEST PROMPT:", max(results, key=lambda k: results[k]['score']))

if __name__ == '__main__':
    main()
```

## Variations

1. **A/B Testing** — compare just 2 prompts, measure which works better
2. **Cost Analysis** — measure tokens used for each prompt
3. **Latency Testing** — measure response time
4. **User Feedback Loop** — collect human feedback on best prompts

## Key Learning

You'll discover:
- Specific prompts > vague prompts
- System messages matter
- Structured output helps
- Costs vary by prompt length
