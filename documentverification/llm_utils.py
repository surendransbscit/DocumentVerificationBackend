from transformers import pipeline
import traceback

HF_API_TOKEN = "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"  


llm = pipeline(
    task="text2text-generation",  # for T5/Flan-style models
    model="google/flan-t5-large",
    token=HF_API_TOKEN
)
def validate_passport_llm(data):
    print("data in llm_utils:", data)
    
    prompt = f"""
You are an AI expert in passport validation.

Below is the extracted data from an Indian passport using OCR:

Name: {data.get('name')}
Date of Birth: {data.get('dob')}
Passport Number: {data.get('doc_number')}
Expiry Date: {data.get('expiry_date')}

Full Raw OCR Text:
{data.get('raw_text')}

Based on the above data, check if this is a valid Indian passport.

Your response must be in the following format:
- Verdict: Indian passport Valid or Indian passport Invalid
- Reason: <Explain briefly why it is valid or not, e.g., missing or mismatched fields, incorrect format, etc.>
"""
    
    try:
        response = llm(prompt, max_new_tokens=300)
        print("LLM response:", response)
        return response[0]["generated_text"].strip()
    except Exception as e:
        print("LLM validation error:", e)
        traceback.print_exc()
        return "LLM validation failed"
    
    
# from transformers import pipeline
# import traceback

# HF_API_TOKEN = "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"

# llm = pipeline(
#     task="text2text-generation",
#     model="google/flan-t5-large",
#     token=HF_API_TOKEN
# )

# def validate_passport_llm(data):
#     raw_text = data.get("raw_text", "")
    
#     prompt = f"""
# You are a professional AI document analyst.

# Analyze the following raw OCR text and determine:
# 1. What type of document is this? (e.g., Indian Passport, Certificate, ID Card)
# 2. Is this document in the correct format for that type?
# 3. Extract the full name of the person mentioned in the document.
# 4. Is this document valid or invalid?

# Raw OCR Text:
# {raw_text}

# Please respond in this format:

# Document Type: <Passport / Certificate / ID Card / Unknown>
# Full Name: <Extracted Name or 'Not Found'> 
# Verdict: <Valid / Invalid>
# Reason: <Brief reason for the verdict>
# """

#     try:
#         response = llm(prompt, max_new_tokens=300)
#         return response[0]["generated_text"].strip()
#     except Exception as e:
#         print("LLM Error:", e)
#         traceback.print_exc()
#         return "LLM validation failed"
