from transformers import pipeline

# Load summarization pipeline once
summarizer = pipeline('summarization', model='facebook/bart-large-cnn')

def chunk_text(text, chunk_size=400):
    # Split text into chunks of chunk_size words (safer for BART)
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i+chunk_size])

import re

def filter_sentences(text):
    # Keep lines that look like sentences (contain a period, question mark, or exclamation)
    lines = text.splitlines()
    sentence_lines = [line for line in lines if re.search(r'[.!?]', line) and len(line.split()) > 4]
    return '\n'.join(sentence_lines)

def summarize_text(text):
    if not text.strip() or len(text.strip().split()) < 10:
        return "Please upload a file with at least 10 words of meaningful text to summarize."
    # Clean up text: remove extra spaces, replace tabs/newlines with single space
    clean_text = ' '.join(text.replace('\t', ' ').replace('\n', ' ').split())
    try:
        chunks = list(chunk_text(clean_text, chunk_size=250))
        summaries = []
        for chunk in chunks:
            try:
                input_length = len(chunk.split())
                max_len = min(400, max(30, int(input_length * 0.7)))
                min_len = min(80, max(10, int(input_length * 0.3)))
                summary_list = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)
                if summary_list and isinstance(summary_list, list) and len(summary_list) > 0 and 'summary_text' in summary_list[0]:
                    # Format summary: bullet points, new lines after periods
                    summary_text = summary_list[0]['summary_text'].replace('\n', ' ')
                    points = [f"• {line.strip()}" for line in summary_text.split('. ') if line.strip()]
                    summaries.extend(points)
                else:
                    summaries.append("• [Chunk could not be summarized]")
            except Exception as e:
                summaries.append(f"• [Chunk error: {str(e)}]")
        # Limit to first 20 bullet points for readability
        return '\n'.join(summaries[:20])
    except Exception as e:
        return f"Error: {str(e)}"

# Test function for local debugging
if __name__ == "__main__":
    test_text = "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of intelligent agents: any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals."
    print(summarize_text(test_text))