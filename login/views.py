from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
import bcrypt
from login import models
import json
from openai import OpenAI
import json
import easyocr
from PIL import Image
import os
import logging
import numpy as np

#api
current_dir = os.path.dirname(__file__)
config_path = os.path.abspath(os.path.join(current_dir, '../config.json'))
with open(config_path, 'r') as f:
    config = json.load(f)

client = OpenAI(
    api_key = config.get("apiKey"),
    base_url = config.get("baseUrl")
)

# Create your views here.

def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        if user and pwd:
            query = models.sora_UserInfo.objects.filter(name=user).first()
            if query is not None:
                dbpwd = bytes(query.password,encoding='utf-8')
                print(dbpwd)
            else:
                return render(request,'login.html',{"error":"username doesn't exist"})
            if bcrypt.checkpw(pwd.encode('utf-8'),dbpwd): #login sucessfully
                request.session["info"] = {"name":query.name}
                return redirect('chat')
            else:
                return render(request,'login.html',{"error":"invalid username or password"})
        else:
            return render(request,'login.html',{"error":"please input"})
        
def register(request):
    if request.method == "GET":
        return render(request,'register.html')
    else:
        user = request.POST.get('user')
        pwd = request.POST.get('pwd').encode('utf-8')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if user and pwd and phone and email:
            query = models.sora_UserInfo.objects.filter(name=user).first()
            if query is not None:
                return render(request,'register.html',{"error":"username has existed"})
            else:
                salt = bcrypt.gensalt()
                hashed_pwd = bcrypt.hashpw(pwd,salt).decode('utf-8')
                new_user = models.sora_UserInfo(
                    account = str(user),
                    password = hashed_pwd,
                    email = str(email),
                    name = str(user),
                    phone = int(phone),
                    salt = str(salt),
                )
                new_user.save()
                return redirect('login')
        else:
            return render(request,'register.html',{"error":"please input info"})
        
def index(request):
    infoDict = request.session.get('info')
    if not infoDict:
        return redirect('/login/')
    if request.method == "GET":
        return render(request,'index.html')
    else:
        data = json.loads(request.body)
        user_message = data.get("message")
        # kimiapi
        completion = client.chat.completions.create(
            model = "moonshot-v1-8k",
            messages = [
                {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
                {"role": "user", "content": user_message}
            ],
            temperature = 0.3,
        )
        bot_response = f"{completion.choices[0].message.content}"
        return JsonResponse({"response":bot_response})


def chat(request):
    infoDict = request.session.get('info')
    if not infoDict:
        return redirect('/login/')
    if request.method == "GET":
        return render(request,'chat.html')
    elif request.FILES.get('image'):
        image_file = request.FILES['image']
        image = Image.open(image_file)
        image_np = np.array(image)
        reader = easyocr.Reader(['ch_sim','en'])
        try:
            result = reader.readtext(image_np)
            text = '\n'.join([item[1] for item in result])
            # kimiapi
            completion = client.chat.completions.create(
            model = "moonshot-v1-8k",
            messages = [
                {"role": "system", "content": "你是 Kimi,由 Moonshot AI 提供的人工智能助手,你更擅长中文和英文的对话。你会为用户提供安全,有帮助,准确的回答。同时,你会拒绝一切涉及恐怖主义,种族歧视,黄色暴力等问题的回答。Moonshot AI 为专有名词,不可翻译成其他语言。你接收到的这条消息是图片识别而成,内容应该是一个问题,请你回答这个问题。如果这条消息不是一个问题,请你回复要求用户重新拍摄上传;如果这条消息语义不明,请你回复要求用户拍摄的更加清晰或完整。如果问题是选择题,请简单明了地回答,解析尽量短。"},
                {"role": "user", "content": text}
            ],
            temperature = 0.3,
            )
            bot_response = f"{completion.choices[0].message.content}"
            return JsonResponse({'response': bot_response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'response': '请上传图片~'})

# logger = logging.getLogger(__name__)

# def chat(request):
#     try:
#         if request.method == "POST":
#             pass
#         else:
#             return JsonResponse({"error": "GET not allowed"}, status=405)
#     except Exception as e:
#         logger.error(f"Error in chat view: {e}")
#         return JsonResponse({"error": "Server error"}, status=500)