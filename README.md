# Amazon Bedrock Complete Learning Curriculum

A comprehensive, hands-on guide to becoming an **Amazon Bedrock expert**. Each module combines concept notes with a practical project that reinforces real-world usage.

## 📚 12-Module Curriculum

| # | Module | Duration | Project |
|---|--------|----------|---------|
| **01** | [Introduction & Setup](#module-01--introduction--setup) | 1-2h | Hello Bedrock — first API call |
| **02** | [Foundation Models Deep Dive](#module-02--foundation-models-deep-dive) | 2-3h | Multi-model comparison CLI |
| **03** | [Prompt Engineering](#module-03--prompt-engineering) | 2-3h | Prompt optimization test harness |
| **04** | [Converse API & Streaming](#module-04--converse-api--streaming) | 1-2h | Terminal chatbot with streaming |
| **05** | [Knowledge Bases & RAG](#module-05--knowledge-bases--rag) | 3-4h | Document Q&A with citations |
| **06** | [Bedrock Agents](#module-06--bedrock-agents) | 3-4h | Customer service agent |
| **07** | [Guardrails](#module-07--guardrails) | 2-3h | Safe content pipeline |
| **08** | [Bedrock Flows](#module-08--bedrock-flows) | 2-3h | Automated content workflow |
| **09** | [Model Evaluation](#module-09--model-evaluation) | 2-3h | Evaluation comparison report |
| **10** | [Fine-Tuning & Custom Models](#module-10--fine-tuning--custom-models) | 3-4h | Custom model training & deployment |
| **11** | [Production & Observability](#module-11--production--observability) | 3-4h | Production observability stack |
| **12** | [Multi-Agent Orchestration](#module-12--multi-agent-orchestration) | 3-4h | Supervisor + subagent system |

**Total:** ~30-40 hours of learning + hands-on projects

## Progress Tracker

Track your completion:

```
Amazon Bedrock Core
- [ ] Module 01 — Introduction & Setup
- [ ] Module 02 — Foundation Models Deep Dive
- [ ] Module 03 — Prompt Engineering
- [ ] Module 04 — Converse API & Streaming
- [ ] Module 05 — Knowledge Bases & RAG
- [ ] Module 06 — Bedrock Agents
- [ ] Module 07 — Guardrails
- [ ] Module 08 — Bedrock Flows
- [ ] Module 09 — Model Evaluation
- [ ] Module 10 — Fine-Tuning & Custom Models
- [ ] Module 11 — Production & Observability
- [ ] Module 12 — Multi-Agent Orchestration

Status: 0/12 complete
```

## Prerequisites

- **AWS Account** — free tier eligible, but some modules incur charges (fine-tuning, provisioned throughput)
- **Python 3.9+** — boto3, standard library only for most projects
- **AWS CLI** configured with credentials
- **IAM Permissions** — Bedrock API access, Lambda, S3, OpenSearch (varies by module)
- **Cost awareness** — estimate ~$50-100 if you complete all projects (most costs from fine-tuning + provisioned throughput)

## Getting Started

1. **Clone this repo**
   ```bash
   git clone https://github.com/Tevaalgorithms/amazon-bedrock-learning.git
   cd amazon-bedrock-learning
   ```

2. **Start with Module 01** — sets up your environment
   ```bash
   cd module-01-intro-and-setup
   cat notes.md
   ```

3. **Work through sequentially** — each module builds on prior concepts
4. **Do the projects** — implementation is where learning happens

## Directory Structure

```
amazon-bedrock-learning/
├── module-01-intro-and-setup/
│   ├── notes.md              # Concept notes
│   └── project/
│       ├── README.md         # Project guide
│       └── hello_bedrock.py  # Starter code
├── module-02-foundation-models/
│   ├── notes.md
│   └── project/
│       ├── README.md
│       └── model_comparison.py
├── ... (10 more modules)
└── README.md                 # You are here
```

---

## Module Details

### Module 01 — Introduction & Setup
Learn what Bedrock is, how to set up your AWS environment, and invoke your first model.

**Key Topics:** Bedrock fundamentals, pricing, IAM setup, boto3, model IDs, InvokeModel API
**Project:** `hello_bedrock.py` — call Claude, print response
**Time:** 1-2 hours

→ [Go to Module 01](module-01-intro-and-setup/)

---

### Module 02 — Foundation Models Deep Dive
Explore all available models and understand their capabilities, strengths, and use cases.

**Key Topics:** Claude, Titan, Llama, Mistral, Cohere, Stable Diffusion, capability matrix, pricing
**Project:** Compare 3 models side-by-side with the same prompt
**Time:** 2-3 hours

→ [Go to Module 02](module-02-foundation-models/)

---

### Module 03 — Prompt Engineering
Master prompt design for Bedrock — system prompts, few-shot learning, chain-of-thought, structured outputs.

**Key Topics:** Anthropic Messages API, prompt templates, few-shot, CoT, XML tags, tool-use format
**Project:** Prompt optimization framework that tests variations
**Time:** 2-3 hours

→ [Go to Module 03](module-03-prompt-engineering/)

---

### Module 04 — Converse API & Streaming
Learn the model-agnostic Converse API and how to stream responses for better UX.

**Key Topics:** Converse API vs InvokeModel, multi-turn conversations, streaming, token counting
**Project:** Terminal chatbot with streaming and conversation history
**Time:** 1-2 hours

→ [Go to Module 04](module-04-converse-api/)

---

### Module 05 — Knowledge Bases & RAG
Build retrieval-augmented generation systems with Bedrock Knowledge Bases.

**Key Topics:** Embeddings, OpenSearch Serverless, chunking, sync jobs, RetrieveAndGenerate, citations
**Project:** Document Q&A system that ingests PDFs and answers with citations
**Time:** 3-4 hours

→ [Go to Module 05](module-05-knowledge-bases-rag/)

---

### Module 06 — Bedrock Agents
Create agents that act on tools — define action groups, integrate Lambda functions, handle stateful conversations.

**Key Topics:** Agent anatomy, action groups, Lambda integration, session state, return of control, code interpreter
**Project:** Customer service agent with order lookup and FAQ action groups
**Time:** 3-4 hours

→ [Go to Module 06](module-06-bedrock-agents/)

---

### Module 07 — Guardrails
Implement safety guardrails for responsible AI — content filtering, PII detection, denied topics.

**Key Topics:** Content filters, word filters, PII masking, topic denial, grounding checks
**Project:** Safe content pipeline with blocked content logging
**Time:** 2-3 hours

→ [Go to Module 07](module-07-guardrails/)

---

### Module 08 — Bedrock Flows
Define complex workflows visually or via code using Bedrock Flows.

**Key Topics:** Flow nodes, prompt nodes, conditionals, iterators, KB integration, agent invocation
**Project:** Content workflow — topic → KB retrieval → draft → quality check → publish
**Time:** 2-3 hours

→ [Go to Module 08](module-08-bedrock-flows/)

---

### Module 09 — Model Evaluation
Evaluate and compare model outputs systematically using Bedrock Evaluation Jobs.

**Key Topics:** Human vs model-based evaluation, BLEU/ROUGE/RAGAS, Bedrock Evaluations, comparison reports
**Project:** Evaluation dashboard that compares 2 models on a benchmark
**Time:** 2-3 hours

→ [Go to Module 09](module-09-model-evaluation/)

---

### Module 10 — Fine-Tuning & Custom Models
Fine-tune foundation models on your own data for domain-specific performance.

**Key Topics:** Fine-tuning vs continued pre-training, JSONL format, hyperparameters, provisioned throughput
**Project:** Prepare data, launch fine-tune job, deploy with provisioned throughput
**Time:** 3-4 hours

→ [Go to Module 10](module-10-fine-tuning/)

---

### Module 11 — Production & Observability
Deploy Bedrock applications to production with monitoring, cost tracking, and resilience.

**Key Topics:** CloudWatch metrics, logging, cost optimization, error handling, multi-region failover
**Project:** CDK-based production stack with observability dashboard and cost alarms
**Time:** 3-4 hours

→ [Go to Module 11](module-11-production/)

---

### Module 12 — Multi-Agent Orchestration
Build enterprise-scale systems with multiple coordinated agents.

**Key Topics:** Supervisor/subagent pattern, inline agents, cross-agent delegation, action group routing
**Project:** Supervisor agent orchestrates research, writer, and reviewer subagents
**Time:** 3-4 hours

→ [Go to Module 12](module-12-multi-agent/)

---

## How to Use This Curriculum

### For Self-Paced Learning
- Read each module's `notes.md` to understand concepts
- Follow the `project/README.md` step-by-step implementation guide
- Complete the starter code with the TODOs
- Experiment beyond the scope — modify, extend, break things

### For Teaching
- Adapt module content for your audience
- Use projects as assignments
- Projects are designed to take 1-2 hours each

### For Reference
- Jump to any module by directory
- Each module is independent (except sequential dependencies noted)
- Project code is production-adjacent (not production-grade)

---

## Learning Outcomes

By completing this curriculum, you will:

✅ Understand Bedrock architecture and APIs
✅ Choose the right model for your use case
✅ Master prompt engineering for better outputs
✅ Build RAG systems with knowledge bases
✅ Create agents with custom tools and integrations
✅ Implement safety and guardrails
✅ Deploy to production with observability
✅ Fine-tune models for specialized domains
✅ Orchestrate multi-agent systems

You'll be equipped to architect and build **production-grade AI applications** on AWS.

---

## Tech Stack

- **Python 3.9+** — all projects
- **boto3** — AWS SDK
- **Amazon Bedrock** — models, knowledge bases, agents
- **AWS Lambda** — for agent action groups
- **AWS CDK / Terraform** — infrastructure as code
- **OpenSearch Serverless** — vector database
- **CloudWatch** — observability

---

## Cost Estimates

| Module | Est. Cost |
|--------|-----------|
| 01-05 (API + KB) | $5-10 |
| 06-08 (Agents + Flows) | $10-20 |
| 09 (Evaluation) | $5-15 |
| 10 (Fine-tuning) | $20-50 |
| 11 (Production setup) | Free-$5 |
| 12 (Multi-agent) | $5-10 |
| **Total** | **~$50-100** |

⚠️ Provisioned throughput (Module 10-12) is expensive — clean up after projects!

---

## Contributing

These notes are my learning journey. If you find errors, have suggestions, or want to contribute:

1. Open an issue with feedback
2. Submit a PR with improvements
3. Share your implementation variations

---

## Resources

- **Official Docs:** https://docs.aws.amazon.com/bedrock/
- **Models:** https://docs.aws.amazon.com/bedrock/latest/userguide/models-support.html
- **Pricing:** https://aws.amazon.com/bedrock/pricing/
- **SDK Samples:** https://github.com/aws/amazon-bedrock-samples

---

## License

These notes are provided as-is for learning purposes.

---

**Happy learning! 🚀**

> "The expert in anything was once a beginner." — Helen Hayes
