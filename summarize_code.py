import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import pandas as pd

def analyze_code(rfepo_path):
    analysis = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    snippet = f.read()
                    lines = snippet.split('\n')
                    analysis.append({
                        'file': os.path.join(root, file),
                        'snippet': snippet,
                        'line_count': len(lines),
                        'functions': [line for line in lines if 'def ' in line],
                        'comments': [line for line in lines if line.strip().startswith('#')],
                    })
    return analysis


def generate_narrative_document(analysis):
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B")
    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B")
    summarizer = pipeline("text-generation", model=model, tokenizer=tokenizer)

    narrative = []
    for item in analysis:
        snippet_summary = f"File: {item['file']}\n\n"
        snippet_summary += f"Code Snippet:\n{item['snippet']}\n\n"
        snippet_summary += f"Line Count: {item['line_count']}\n"
        snippet_summary += f"Functions: {', '.join(item['functions'])}\n"
        snippet_summary += f"Comments: {', '.join(item['comments'])}\n"

        result = summarizer(snippet_summary, max_length=500, num_return_sequences=1)
        narrative.append(result[0]['generated_text'].strip())

    full_narrative = "\n\n".join(narrative)
    return full_narrative


def main():
    repo_path = './'
    analysis = analyze_code(repo_path)
    narrative_document = generate_narrative_document(analysis)

    with open('narrative_document.md', 'w') as file:
        file.write(narrative_document)

    print("Narrative document generated successfully!")


if __name__ == "__main__":
    main()
