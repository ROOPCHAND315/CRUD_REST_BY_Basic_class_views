from django.shortcuts import render
from .models import StudentModel
from .serializers import StudentSerializer
import io
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(csrf_exempt,name='dispatch')
class StudentView(View):
    def get(self,request,*args,**kwargs):
        json_data=request.body
        print(json_data)
        stream=io.BytesIO(json_data)
        python_data=JSONParser().parse(stream)
        print(python_data)
        id=python_data.get('id',None)
        if id is not None:
            stu=StudentModel.objects.get(id=id)
            serializer=StudentSerializer(stu)
            json_data=JSONRenderer().render(serializer.data)
            return HttpResponse(json_data,content_type='application/json')
        stu=StudentModel.objects.all()
        serializer= StudentSerializer(stu,many=True)
        json_data=JSONRenderer().render(serializer.data)
        return HttpResponse(json_data,content_type='application/json')
    

    def post(self, request, *args, **kwargs):
        json_data=request.body
        stream=io.BytesIO(json_data)
        python_data=JSONParser().parse(stream)
        serializer= StudentSerializer(data=python_data)
        if serializer.is_valid():
            serializer.save()
            res={'msg':'Data Added!'}
            json_data=JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type='application/json')
    
    def put(self,request,*args,**kwargs):
        json_data=request.body
        stream= io.BytesIO(json_data)
        python_data=JSONParser().parse(stream)
        id=python_data.get('id')
        stu= StudentModel.objects.get(id=id)
        serializer=StudentSerializer(stu,data=python_data)
        if serializer.is_valid():
            serializer.save()
            res={'msg':'Data upadate!'}
            json_data=JSONRenderer().render(res)
            return HttpResponse(json_data,content_type='application/json')
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type='application/json')

    def delete(self ,request, *args , **kwargs):
        json_data=request.body
        stream=io.BytesIO(json_data)
        python_data=JSONParser().parse(stream)
        id=python_data.get('id')
        stu= StudentModel.objects.get(id=id)
        stu.delete()
        res={'msg':'Data Deleted!'}
        json_data=JSONRenderer().render(res)
        return HttpResponse(json_data,content_type='application/json')