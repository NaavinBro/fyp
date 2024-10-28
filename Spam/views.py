from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import joblib
import os
import PyPDF2
import re  # url extraction

# Load the models once (outside the function to prevent reloading on every request)
model1 = joblib.load(os.path.dirname(__file__) + "/myModel3.pkl")  # Model 1
model2 = joblib.load(os.path.dirname(__file__) + "/mySVCModel.pkl")  # Model 2

def Index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contactus(request):
    return render(request, 'contactus.html')

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        uploaded_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        file_path = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(file_path)

        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(file_path)

        # Pass the extracted text to both models to check for phishing
        result = check_spam(extracted_text)

        is_phishing = True
        # Optional: Delete the file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

        # Return the result and extracted text in JSON format
        return JsonResponse({
            'result': result,
            'extracted_text': extracted_text, 
            'is_phishing': is_phishing
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

def extract_text_from_pdf(pdf_path):
    """Extract text from the PDF file."""
    reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

def check_spam(extracted_text):
    """Check if the extracted text is phishing, not phishing, or suspicious."""
    # Use both models to predict phishing
    prediction1 = model1.predict([extracted_text])[0]  # Predict using model1
    prediction2 = model2.predict([extracted_text])[0]  # Predict using model2
    
    # If any model predicts "spam", it's phishing
    if prediction1 == "spam" or prediction2 == "spam":
        return "Phishing"
    else:
        return "Not Phishing"
 
    