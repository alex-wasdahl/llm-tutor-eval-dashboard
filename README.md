# llm-tutor-eval-dashboard
Interactive dashboard comparing LLM responses to student questions using different prompt strategies and evaluation metrics

# 🧠 Interactive Tutor Evaluation Dashboard

This project provides an interactive dashboard to evaluate how different large language models (LLMs) respond to middle school-level academic questions under different prompting strategies.

## ✨ Features

- Compare LLM responses to the same question using:
  - Zero-shot prompting
  - Few-shot prompting
  - Chain-of-thought prompting
- Evaluate responses using:
  - Readability metrics (Flesch, Coleman-Liau)
  - Step count / explanation depth
  - Word count
- Choose questions from a curated dataset of middle school algebra problems
- (Planned) Add scoring for accuracy and pedagogical helpfulness

## 🧰 Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [OpenAI API](https://platform.openai.com/)
- [pandas](https://pandas.pydata.org/)
- [textstat](https://pypi.org/project/textstat/)

## 🚀 Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/llm-tutor-eval-dashboard.git
   cd llm-tutor-eval-dashboard
