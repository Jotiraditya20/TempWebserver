import re

def clean_summary(summary_text: str) -> str:
    # Remove AI intro phrases
    summary_text = re.sub(r"(?i)^of course\..*?analysis of the code changes\.\s*", "", summary_text)

    # Remove markdown headings (###) and bold (**)
    summary_text = re.sub(r"###\s*", "", summary_text)      # Remove headings
    summary_text = re.sub(r"\*\*(.*?)\*\*", r"\1", summary_text)  # Remove bold markers but keep text
    
    # Remove unnecessary leading/trailing whitespace
    summary_text = summary_text.strip()

    return summary_text