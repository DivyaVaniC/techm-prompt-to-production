# skills.md
# INSTRUCTIONS: Generate a draft by prompting AI, then manually refine this file.
# Delete these comments before committing.

skills:
  - name: classify_complaint
    description: Classifies a single citizen complaint by category and priority.
    input:
      type: dict
      format: "{'complaint_id': 'str', 'description': 'str'}"
    output:
      type: dict
      format: "{'complaint_id': 'str', 'category': 'str', 'priority': 'str', 'reason': 'str', 'flag': 'str'}"
    error_handling: Returns 'Other' category, 'Standard' priority, and 'PROCESSING_ERROR' flag if an unexpected error occurs during classification. If description is empty or too vague, returns 'Other' category, 'Standard' priority, and 'NEEDS_REVIEW' flag.

  - name: batch_classify
    description: Reads a CSV file of complaints, classifies each row using classify_complaint, and writes the results to a new CSV file.
    input:
      type: dict
      format: "{'input_path': 'str', 'output_path': 'str'}"
    output:
      type: str
      format: "Path to the output CSV file (e.g., 'results_pune.csv')"
      nomenclature has to be like results_pune.csv
    error_handling: Flags individual rows with 'PROCESSING_ERROR' if classification fails for that row, but continues processing and produces an output CSV. Does not crash on bad rows.
