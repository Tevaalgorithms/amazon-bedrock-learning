# Module 09 Project — Model Evaluation Dashboard

## Goal

Build a dashboard that:
- Runs evaluation on test dataset
- Compares 2 models (Claude vs Llama)
- Shows metrics (accuracy, latency, cost)
- Generates HTML report

## Implementation

```python
import boto3
import json
import time
from datetime import datetime

bedrock_runtime = boto3.client('bedrock-runtime')

# Test dataset
test_cases = [
    {'question': 'What is 2+2?', 'expected': '4'},
    {'question': 'What is the capital of France?', 'expected': 'Paris'},
    # ... more test cases
]

models = [
    'anthropic.claude-3-5-sonnet-20241022-v1:0',
    'meta.llama3-1-70b-instruct-v1:0'
]

results = {}

for model in models:
    print(f"Evaluating {model}...")
    correct = 0
    total_latency = 0

    for test_case in test_cases:
        start = time.time()
        response = bedrock_runtime.converse(
            modelId=model,
            messages=[{'role': 'user', 'content': test_case['question']}]
        )
        latency = (time.time() - start) * 1000

        answer = response['output']['message']['content'][0]['text']

        if test_case['expected'].lower() in answer.lower():
            correct += 1

        total_latency += latency

    accuracy = correct / len(test_cases)
    avg_latency = total_latency / len(test_cases)

    results[model] = {
        'accuracy': accuracy,
        'avg_latency_ms': avg_latency
    }

# Generate HTML report
html = f'''
<html>
<head><title>Model Evaluation Report</title></head>
<body>
<h1>Model Evaluation Report</h1>
<p>Generated: {datetime.now()}</p>

<table border="1">
<tr><th>Model</th><th>Accuracy</th><th>Avg Latency (ms)</th></tr>
{''.join([f"<tr><td>{model}</td><td>{results[model]['accuracy']:.1%}</td><td>{results[model]['avg_latency_ms']:.1f}</td></tr>" for model in results])}
</table>

<h2>Winner: {max(results, key=lambda k: results[k]['accuracy'])}</h2>
</body>
</html>
'''

with open('evaluation_report.html', 'w') as f:
    f.write(html)

print("Report saved to evaluation_report.html")
```

## Expected Output

- HTML report with model comparison
- Accuracy percentages
- Latency metrics
- "Winner" recommendation
