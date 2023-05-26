from django.shortcuts import render
import openai,os
from dotenv import load_dotenv
load_dotenv()

api_key=os.getenv("OPENAI_KEY",None)


# Create your views here.
def gpt(request):
    chat_response=None
    print(api_key)
    
    if api_key is not None and request.method == "POST":
        openai.api_key=api_key
        user_input=request.POST["input"]
        prompt=user_input
        response=openai.Completion.create(engine='text-davinci-003',
        prompt=prompt,
    max_tokens=256,
    temperature=0.5
    )
        print(response)
        chat_response = response.choices[0].text.strip()
        chat_response_lines = chat_response.split('\n')
        
        context = {'response_lines': chat_response_lines}
        return render(request,'./query2.html',context)
    else:
        return render(request,'./query2.html')
