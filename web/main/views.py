from django.shortcuts import render, redirect
import os
from django.conf import settings
from django.http import HttpResponse

import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image
from torch.autograd import Variable
from .resnet import resnet101
# import matplotlib.image as mpimg
# from PIL import Image
# Create your views here.

def index(request):
    return render(request, 'main/main.html')

def upload(request):
    # print(request)
    if request.method == 'POST':
        if 'fileObj' in request.FILES:
            file = request.FILES['fileObj']
            filename = file._name

            fp = open('%s/%s' % (os.path.join(settings.BASE_DIR, 'media'), filename) , 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()
            
    return HttpResponse(filename)
    # return redirect('main:index')

def resultView(request):
    # if request.method == 'GET':
        # print(request.GET)
        # print(request.GET.get('name'))
        # pass
    fpath = os.path.join(settings.BASE_DIR, 'media')
    # preimage = mpimg.imread(os.path.join(fpath,request.GET.get('name')))
    preimage = os.path.join(fpath,request.GET.get('name'))

    # imagepath = os.path.join(fpath,request.GET.get('name'))
    def image_loader(loader, image_name):
        image = Image.open(image_name)
        image = loader(image).float()
        image = torch.tensor(image, requires_grad=True)
        image = image.unsqueeze(0)
        return image

    data_transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor()
    ])

    classes = ['Gun','Knife','Wrench','Pliers','Scissors']

    model = resnet101(len(classes), pretrained=True)
    checkpoint = torch.load('./main/models-/model_best_70.0000.pth.tar', map_location='cpu')
    model.load_state_dict(checkpoint['state_dict'])
    model.eval()

    res = classes[np.argmax(model(image_loader(data_transforms, preimage).cpu())[-1].detach().numpy())]

    imagepath = "../media/answer" + res + '.png'
    return HttpResponse(imagepath)