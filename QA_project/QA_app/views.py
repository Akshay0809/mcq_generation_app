from django.shortcuts import render
from django.http import HttpResponse
from .models import MCQ
from .forms import UploadPDFForm
from langchain_groq import ChatGroq
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from langchain import LLMChain,PromptTemplate


#init groq llm 

llm = ChatGroq(
    temperature=0,
    groq_api_key='USE_YOUR_GROQ_API_KEY',
    model_name='llama-3.1-70b-versatile'
)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

#generating mcq with groq
def generate_mcq_with_groq(context):
    prompt = f"Generate multiple-choice questions based on the following context:\n\n{context}\n\n"
    response = llm.query(prompt)
    return response


#function to handle file handling and mcq generation 
def upload_pdf(request):
    if request.method=='POST':
        print(request.FILES)
        #form = UploadPDFForm(request.POST,request.FILES)
        form = UploadPDFForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            #uploaded_file = request.FILES.get('document')
            uploaded_file = request.FILES.get('context')
            print(uploaded_file)
            if uploaded_file is None:
                 print("No file uploaded!") 
                 return HttpResponse("No file uploaded.", status=400)
            
            if hasattr(uploaded_file, 'name'):
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                print(f"File saved: {filename}")  # Debugging: confirm file saving

            
            #fs=FileSystemStorage()
            #filename = fs.save(uploaded_file.name,uploaded_file)

        #extracting text from the uploaded file
        pdf_text=extract_text_from_pdf(uploaded_file)


        #generating mcq
        template=""" Generate maximum as possible as multiple-choice questions  based on the provided context and also should cover all concepts and major topics in pdf:
         Context:{context}
         Questions: """
        
        prompt_template= PromptTemplate(input_variable=["context"],template=template)
        llm_chain=LLMChain(prompt=prompt_template,llm=llm)
        mcq_ouput=llm_chain.run(context=pdf_text)

        # Mark existing MCQs as past
        MCQ.objects.filter(is_current=True).update(is_current=False)

        #save generated mcq in db

        mcqs=mcq_ouput.split("\n")
        for mcq in mcqs:
            if mcq.strip():
                MCQ.objects.create(question=mcq,is_current=True)

        #retrieve the generated mcqs to display
        #saved_mcqs=MCQ.objects.all()
        # Mark existing MCQs as past
        #current_mcqs =  MCQ.objects.filter(is_current=True)
                
        # Fetch current and past MCQs
        current_mcqs = MCQ.objects.filter(is_current=True)
        past_mcqs = MCQ.objects.filter(is_current=False)

        return render(request,'mcq_generated.html',{'current_mcqs':current_mcqs , 'past_mcqs': past_mcqs})
    else:
        form=UploadPDFForm()

    return render(request,'upload.html',{'form':form})

#view to download mcqs as pdf with watermark
def dowload_mcq_pdf(request):
    mcqs=MCQ.objects.all()

    #creating the pdf with mcq and watermark
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="mcqs.pdf"'

    buffer=BytesIO()
    p= canvas.Canvas(buffer,pagesize=letter)
    width,height=letter

    #adding watermark
    p.setFont("Helvetica",40)
    p.setFillColorRGB(0.9, 0.9, 0.9)
    p.drawCentredString(width / 2.0, height / 2.0, "Akshay")

    p.setFont("Helvetica", 12)
    p.setFillColorRGB(0, 0, 0)

    # Write the MCQs to the PDF
    p.drawString(100, height - 60, "Generated MCQs:")
    y = height - 100
    for mcq in mcqs:
        p.drawString(100, y, mcq.question)
        y -= 40
        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = height - 100
            
    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')








