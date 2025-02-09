# LFPBench

This repository is for Legal Fact Prediction: The Missing Piece in Legal Judgment Prediction.

The code repository includes a complete benchmark dataset, execution scripts for all methods presented in the paper, and automatic evaluation scripts.

## Usage

### Preparation

**extraction_annoted.json**: formatted judgment paper and marked judgment; This document was obtained by applying regular expressions to extract information from court judgments and has undergone two rounds of manual annotation. In the first round, the list of court decisions was annotated. In the second round, the accuracy of the facts extracted from the "The court has found" section was verified. If the extracted facts were correct, the "Fact Verification" field was left blank; otherwise, the correct facts were manually entered into the "Fact Verification" field.

**extraction_evidence_washed2.json**: list of evidence extracted; This document was extracted from a court judgment using a large model and has undergone manual sampling inspection to verify the accuracy of the extracted evidence.

### Running

**LFP.py**: generation script for legal fact;

**LJP_with_evi.py**: evidence-based LJP;

**LJP_with_fact.py**: fact-based LJP;

**LJP_with_LFP_evi.py**: LFP/fact empowered;

**LJP_eval.py**: evaluation script for calculating the accuracy of results.
