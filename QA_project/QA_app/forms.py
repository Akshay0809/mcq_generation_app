#from django import forms

#class UploadPDFForm(forms.Form):
   # context=forms.FileField(label="upload pdf")



from django import forms

class UploadPDFForm(forms.Form):
    context = forms.FileField(
        label='Select a PDF file', 
    )
