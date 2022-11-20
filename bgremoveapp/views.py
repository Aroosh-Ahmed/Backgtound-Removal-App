from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image
import base64
import json
import io

from django.http import JsonResponse

from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from bgremoveapp.modnet_module.src.inference import make_matte,display
# Create your views here.

image = Image.open("D:\MODNet-master\Input\Me2.jpeg")
ckpt_path = "D:\MODNet-master\pretrained\modnet_photographic_portrait_matting.ckpt"

# @csrf_exempt
def removebgview(request):
    if request.method == "POST":
        img = request.POST["image"]
        # print("Image is : ", request.POST)
        # body_unicode = request.body.decode('utf-8')
        # body = json.loads(body_unicode)
        # img = body['image']
        pre_img = img.split(",")[0]
        bytes_image = base64.b64decode(img.split(",")[1])
        img = Image.open(io.BytesIO(bytes_image))
        matted_image = make_matte(img,ckpt_path)
        bgremoved_image = display(img,matted_image)
        print("TT : ", type(bgremoved_image))
        buffered = io.BytesIO()
        bgremoved_image.save(buffered, format='PNG')
        img_str = base64.b64encode(buffered.getvalue())
        img_str = str(img_str)
        print("D is : ", pre_img)
        print("Image is : ", img_str)
        final_img = pre_img+","+img_str.split("'")[1]
        return render(request, "index.html", {"Image":final_img})
        # bgremoved_image.show()
        # return JsonResponse({"result_base64":img_str.split("'")[1]})
    elif request.method == "GET":
        return render(request,"index.html")
        # im = image
        # matte = make_matte(im, ckpt_path)
        # result = display(im, matte)
        # image_data = base64.b64encode(result).decode('utf-8')
        # print(type(result))
        # print("Base 64 image is : ",image_data)
        # return render(request, "index.html", {"image": image, "name": "Arsh"})
        # return JsonResponse({"message":"Get Request Not supported for API yet"})
