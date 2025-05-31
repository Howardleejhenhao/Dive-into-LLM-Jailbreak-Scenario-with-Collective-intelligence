# Dive-into-LLM-Jailbreak-Scenario-with-Collective-intelligence


# Project Introduction

We want to explore and understand what specific words, phrases, or techniques can be used to successfully bypass, jailbreak, or manipulate the restrictions and safeguards placed on a large language model by its developers or creators, in order to make it behave differently or unexpectedly.

## Project Structure

```
.
├── README.md
├── analyze
│   ├── analyze-code
│   │   ├── EP_analyze_Speech_Act.py
│   │   ├── EP_analyze_triggers.py
│   │   ├── EP_emotion_analysis.py
│   │   ├── EP_modality_analysis.py
│   │   ├── EP_politeness_analysis_extended.py
│   │   ├── Sentence-Transformers-method.py
│   │   ├── analyze_Speech_Act.py
│   │   ├── analyze_eazy_hard_version_successful_proportion.py
│   │   ├── analyze_topic_modeling.py
│   │   ├── analyze_triggers.py
│   │   ├── analyze_triggers_ratio.py
│   │   ├── emotion_analysis.py
│   │   ├── merge_challenges_records.py
│   │   ├── modality_analysis.py
│   │   ├── politeness_analysis.py
│   │   ├── politeness_analysis_extended.py
│   │   ├── readability_complexity_analysis.py
│   │   ├── sentiment_analysis.py
│   │   ├── structural_template_analysis.py
│   │   └── toxicity_analysis.py
│   ├── game-data
│   │   ├── challenges.json
│   │   └── game_records.json
│   ├── plot
│   │   ├── Attack success rate by difficulty.png
│   │   ├── Categories (Successful Attacks).png
│   │   ├── Emotion Analysis by Phase (Successful Attacks).png
│   │   ├── Emotion Distribution in Successful Prompts.png
│   │   ├── Modality Distribution Successful vs Failed Attacks.png
│   │   ├── Modality Distribution by Phase.png
│   │   ├── Politeness Distribution by Phase.png
│   │   ├── Sentence Type Distribution (Successful Attacks).png
│   │   ├── Sentence Type Distribution Across Phases.png
│   │   ├── analyze_eazy_hard_version_successful_proportion.py
│   │   ├── plot_EP_analyze_Speech_Act.py
│   │   ├── plot_EP_emotion_analysis.py
│   │   ├── plot_EP_modality_analysis.py
│   │   ├── plot_EP_politeness_analysis.py
│   │   ├── plot_analyze_Speech_Act.py
│   │   ├── plot_emotion_analysis.py
│   │   ├── plot_modality_analysis.py
│   │   └── plot_politeness_analysis.py
│   ├── requirements.txt
│   └── result
│       ├── EP_analyze_Speech_Act.txt
│       ├── EP_analyze_triggers.txt
│       ├── EP_emotion_analysis.txt
│       ├── EP_modality_analysis.txt
│       ├── EP_politeness_analysis.txt
│       ├── analyze_Speech_Act.txt
│       ├── analyze_triggers.txt
│       ├── analyze_triggers_del.txt
│       ├── emotion_analysis.txt
│       ├── modality_analysis.txt
│       └── politeness_analysis.txt
├── backend
│   ├── main.py
│   └── requirements.txt
├── csv_converter
│   └── converter.py
└── frontend
    ├── index.html
    ├── script.js
    └── styles.css
```

## Dataset
The dataset can be found in the `analyze/game-data` folder:

1. `challenges.json` contains information about all challenges.
2. `game_records.json` stores every message we collected from both users and GPT.

## How to Run the Analysis Code

1. Navigate to the `analyze` directory.
2. Install all required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run any analysis script from the `analyze-code` folder. For example:
   ```
   python analyze_triggers.py
   ```

## **[Website](https://ai.driseam.com/)**
The `backend` and `frontend` folders contain the code that powers the site.

## csv converter
Run `csv_conerter/converter.py` to merge all data into a single CSV file.
