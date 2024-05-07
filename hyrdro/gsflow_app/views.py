import urllib.parse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import os 
import io
import urllib, base64

import matplotlib.pyplot as plt
import numpy as np
import flopy
from gsflow.builder import GenerateFishnet
import gsflow

# Create your views here.

def handle_uploaded_file(f):
    with open("./dem.tif", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def index(request):
    dem = 'C:/Users/hp/Documents/GSFlow_app/gsflow/hyrdro/dem.tif'
    if os.path.exists(dem):
        raster = dem
        print(type(raster))
    else:
        print('method above did not work!')
        return render(request,'base.html')   
    return render(request,'base.html')


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        # print("Title is ", request.POST.get('title'))
        dem_title = str(request.POST.get('title'))
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            dem = 'C:/Users/hp/Documents/GSFlow_app/gsflow/hyrdro/dem.tif'
            if os.path.exists(dem):
                raster = dem
                print(type(raster))
                # set cell sizes in metres
                dx = 0.1
                dy = 0.1

                modelgrid = GenerateFishnet(raster,xcellsize =dx , ycellsize = dy )
                print(type(modelgrid))
                print(modelgrid.__class__.__bases__)
                print(modelgrid.extent)
                robj = flopy.utils.Raster.load(raster)
                print(robj)
                #plot the fishnet ontop of the raster imagery

                fig,ax = plt.subplots(figsize = (8,7))
                robj.plot(ax)
                modelgrid.plot(ax = ax)
                ax.set_title(dem_title + " DEM")
                fig.tight_layout()
                # Remove gridlines
                ax.grid(False)

                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                string = base64.b64encode(buf.read())
                uri = urllib.parse.quote(string)
                # Pass width and height to the template
                width, height = fig.get_size_inches() * fig.dpi
                return render(request,'base.html', {'data':uri,'width': width,'height':height})  
            else:
                print('method above did not work!')
                return render(request,'base.html')  
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})