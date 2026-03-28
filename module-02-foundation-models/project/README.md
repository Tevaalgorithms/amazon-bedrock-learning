# Module 02 Project — Multi-Model Comparison CLI

## Goal

Build a CLI tool that sends the same prompt to 3 different Bedrock models and compares:
- Response quality
- Speed (latency)
- Token counts
- Cost

This reinforces model selection decisions.

## Implementation

Create `model_comparison.py`:

```python
import boto3
import json
import time
from typing import Dict, List, Any

client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Model configurations with their request formats
MODELS = {
    'haiku': {
        'id': 'anthropic.claude-3-5-haiku-20241022-v1:0',
        'format': 'claude'
    },
    'llama': {
        'id': 'meta.llama3-1-70b-instruct-v1:0',
        'format': 'llama'
    },
    'mistral': {
        'id': 'mistral.mistral-large-2402-v1:0',
        'format': 'mistral'
    }
}

def format_request(model_name: str, prompt: str) -> Dict[str, Any]:
    """Format request based on model type."""
    # TODO: Implement request formatting for each model type
    # Claude, Llama, and Mistral have different JSON formats
    pass

def invoke_model(model_name: str, prompt: str) -> tuple:
    """Invoke a model and measure performance."""
    # TODO: Create formatted request
    # TODO: Invoke model via client.invoke_model()
    # TODO: Parse response
    # TODO: Calculate latency and costs
    # Return (response_text, latency_ms, input_tokens, output_tokens, cost_usd)
    pass

def main():
    prompt = "Explain quantum computing in 2 sentences."

    # TODO: Invoke all 3 models
    # TODO: Display results in a table
    # TODO: Calculate total cost and time

    for model_name in MODELS.keys():
        result = invoke_model(model_name, prompt)
        print(f"{model_name.upper()}: {result}")

if __name__ == '__main__':
    main()
```

## Expected Output

```
=== Model Comparison ===
Prompt: "Explain quantum computing in 2 sentences."

┌─────────────┬─────────────────────┬───────────────┬────────────┬──────────────┐
│ Model       │ Response Latency    │ Tokens Used   │ Cost       │ Quality      │
├─────────────┼─────────────────────┼───────────────┼────────────┼──────────────┤
│ Haiku       │ 0.45s               │ 18 in / 45 out│ $0.00018   │ Good         │
│ Llama 70B   │ 0.82s               │ 20 in / 48 out│ $0.00034   │ Excellent    │
│ Mistral     │ 0.61s               │ 21 in / 51 out│ $0.00027   │ Excellent    │
└─────────────┴─────────────────────┴───────────────┴────────────┴──────────────┘

Total Cost: $0.00079
Total Time: 1.88 seconds
Winner: Llama (best quality/cost ratio)
```

## Pricing Helper

Add this to calculate costs:

```python
PRICING = {
    'haiku': {'input': 0.00080 / 1000, 'output': 0.00400 / 1000},
    'llama': {'input': 0.00265 / 1000, 'output': 0.00265 / 1000},
    'mistral': {'input': 0.00270 / 1000, 'output': 0.00810 / 1000},
}

def calculate_cost(model_name: str, input_tokens: int, output_tokens: int) -> float:
    rates = PRICING[model_name]
    return (input_tokens * rates['input']) + (output_tokens * rates['output'])
```

## Variations

1. **Add more models** — try Titan, Cohere
2. **Vary the prompt** — test code vs creative vs analytical
3. **Add quality scoring** — use a rubric (accuracy, relevance, length)
4. **Multi-threaded** — invoke all models in parallel
5. **Cost calculator** — show which is most cost-effective

## Key Learnings

- Request format varies by model family
- Response structure varies
- Cost/performance trade-offs are real
- Haiku often good enough for simple tasks
- Llama/Mistral offer good balance
