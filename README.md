# Dive-into-LLM-Jailbreak-Scenario-with-Collective-intelligence

**[Website](https://ai.driseam.com/)**


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

- **analyze/**: Contains Python scripts for data analysis, raw game data, generated plots, and analysis results.
- **backend/**: Backend server implementation and its dependencies.
- **csv_converter/**: Utility for converting data to and from CSV format.
- **frontend/**: Web interface for visualizing and interacting with the analyzed data.