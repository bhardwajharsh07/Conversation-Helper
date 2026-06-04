# Conversation Helper

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![TextBlob](https://img.shields.io/badge/TextBlob-Sentiment%20Analysis-2E86C1)](https://textblob.readthedocs.io/)
[![UI](https://img.shields.io/badge/UI-Interactive%20Prototype-1F2937)]()

A Streamlit application for simulating customer support conversations, evaluating agent replies in real time, and generating quality feedback with coaching suggestions.

## Live Demo

[Open the deployed app](https://conversation-assistant.streamlit.app/)

## Overview

Conversation Helper is a rule-based conversation monitoring tool designed to help support teams review interactions, track customer sentiment, and receive actionable coaching. Users can add customer and agent messages, see per-message sentiment analysis, inspect detailed quality breakdowns, and choose from multiple suggested reply styles.

## Key Features

- **Real-time conversation simulation** with customer and agent message roles
- **Per-message sentiment analysis** — inline badges (Positive / Neutral / Negative) on every message
- **Emotion keyword detection** — tags like "frustrated", "angry", "urgent", "confused" shown on customer messages
- **8-rule agent quality scoring** — greeting, empathy, action words, personalization, clarifying questions, response length, polite closing, and profanity check
- **Detailed rule breakdown** — see exactly which quality checks passed or failed
- **3 categorized suggested replies** — Empathetic, Action-oriented, and Concise alternatives
- **Customer sentiment trend chart** — polarity plotted over conversation history
- **Agent score history chart** — quality scores tracked across replies
- **Emotion tag cloud** — aggregated customer emotions with counts
- **Conversation export** — download chat as a `.txt` file
- **Polished dashboard UI** — glassmorphic cards, gradient header, micro hover animations

## Tech Stack

- Python
- Streamlit
- TextBlob
- HTML/CSS for custom dashboard styling

## Tags

`python` `streamlit` `textblob` `sentiment-analysis` `customer-support` `conversation-analysis` `quality-monitoring` `dashboard` `coaching` `emotion-detection`

## How It Works

1. Add a customer message to start the conversation.
2. Add an agent reply — the app evaluates it across 8 quality rules and calculates a score out of 10.
3. If the response needs improvement, specific nudges are shown alongside a detailed breakdown.
4. Three suggested alternative replies are provided, categorized by style: Empathetic, Action-oriented, and Concise.
5. Charts track customer sentiment and agent score trends over the conversation.

## Installation

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

Start the Streamlit app with:

```bash
streamlit run app.py
```

## Project Structure

```text
.
├── app.py              # Main application
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

## What You Can Use It For

- Support agent coaching and training demos
- Conversation quality walkthroughs
- Sentiment-aware response prototyping
- Internal tooling prototypes for customer support operations

## Notes

This project uses lightweight, rule-based scoring. It is useful for demonstrations and internal experimentation, but it is not a production-grade QA or moderation system.
