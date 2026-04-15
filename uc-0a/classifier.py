"""
UC-0A — Complaint Classifier
Starter file. Build this using the RICE → agents.md → skills.md → CRAFT workflow.
"""
import argparse
import csv

def classify_complaint(row: dict) -> dict:
    """
    Classify a single complaint row.
    Returns: dict with keys: complaint_id, category, priority, reason, flag
    """
    description = row.get("description", "").lower()
    complaint_id = row.get("complaint_id", "N/A")
    category = "Other"
    priority = "Standard" # Default priority as per new AGENTS.md
    reason_parts = []
    flag = ""

    if not description:
        category = "Other"
        priority = "Standard"
        reason_parts.append("Description is empty")
        flag = "NEEDS_REVIEW"
        return {
            "complaint_id": complaint_id,
            "category": category,
            "priority": priority,
            "reason": ", ".join(reason_parts),
            "flag": flag,
        }

    # Categorization
    if any(keyword in description for keyword in ["pothole", "road surface cracked", "sinking"]):
        category = "Pothole"
        reason_parts.append("Category: Pothole (keywords: pothole/road surface cracked/sinking)")
    elif any(keyword in description for keyword in ["flooded", "water", "inaccessible"]):
        category = "Flooding"
        reason_parts.append("Category: Flooding (keywords: flooded/water/inaccessible)")
    elif any(keyword in description for keyword in ["streetlights out", "dark at night", "flickering", "sparking", "lights out"]):
        category = "Streetlight" # Changed from Streetlight Issue
        reason_parts.append("Category: Streetlight (keywords: streetlights out/dark at night/flickering/sparking/lights out)")
    elif any(keyword in description for keyword in ["overflowing garbage bins", "bulk waste", "dumped", "dead animal"]): # Added dead animal
        category = "Waste" # Changed from Garbage/Waste
        reason_parts.append("Category: Waste (keywords: overflowing garbage bins/bulk waste/dumped/dead animal)")
    elif "playing music past midnight" in description:
        category = "Noise" # Changed from Noise Complaint
        reason_parts.append("Category: Noise (keyword: playing music past midnight)")
    elif any(keyword in description for keyword in ["manhole cover missing", "footpath tiles broken", "upturned"]): # Combined Missing Manhole Cover and Footpath Issue
        category = "Road Damage"
        reason_parts.append("Category: Road Damage (keywords: manhole cover missing/footpath tiles broken/upturned)")
    else:
        category = "Other"
        reason_parts.append("Category: Other (no specific category keywords found)")

    # Prioritization
    urgent_keywords = ["injury", "child", "school", "hospital", "ambulance", "fire", "hazard", "fell", "collapse"]

    if any(keyword in description for keyword in urgent_keywords):
        priority = "Urgent"
        reason_parts.append("Priority: Urgent (due to immediate risk keywords)")
    else:
        priority = "Standard" # Changed from Medium/High
        reason_parts.append("Priority: Standard (no urgent risk keywords)")

    # Refusal condition check for vague descriptions (beyond just empty)
    # This is a simplified check; a more robust solution might involve NLP
    if category == "Other" and priority == "Standard" and len(description.split()) < 5: # Example of vague check
        flag = "NEEDS_REVIEW"
        if "Description is empty" not in reason_parts: # Avoid duplicate reason if already set
            reason_parts.append("Flag: NEEDS_REVIEW (description too vague)")


    return {
        "complaint_id": complaint_id,
        "category": category,
        "priority": priority,
        "reason": ", ".join(reason_parts), # Join reasons into a single sentence
        "flag": flag,
    }


def batch_classify(input_path: str, output_path: str):
    """
    Read input CSV, classify each row, write results CSV.
    """
    results = []
    with open(input_path, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            try:
                classified_row = classify_complaint(row)
                results.append(classified_row)
            except Exception as e:
                # Handle rows that might cause unexpected errors during classification
                results.append({
                    "complaint_id": row.get("complaint_id", "N/A"),
                    "category": "Other",
                    "priority": "Standard", # Updated default priority
                    "reason": f"Error during classification: {e}",
                    "flag": "PROCESSING_ERROR",
                })

    fieldnames = ["complaint_id", "category", "priority", "reason", "flag"]
    with open(output_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UC-0A Complaint Classifier")
    parser.add_argument("--input",  required=True, help="Path to test_[techm].csv")
    parser.add_argument("--output", required=True, help="Path to write results CSV")
    args = parser.parse_args()
    batch_classify(args.input, args.output)
    print(f"Done. Results written to {args.output}")
