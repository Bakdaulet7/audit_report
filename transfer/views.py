from django.shortcuts import render
from django.db import connections
from .models import Brand,Merchant
from django.http import JsonResponse
from django.core import serializers

import pandas as pd
import numpy as np
import json

from django.views.decorators.csrf import csrf_exempt


def TransferData(request):
    Merchant.objects.all().delete()
    print('\n_______All data deleted from sqllite\n')
    merch = []
    with connections['mssql'].cursor() as cursor:
        q = """
            DECLARE @Date_From date, @Date_To datetime
            SET @Date_From = '2019-02-01'
            SET @Date_To = dbo.dayEnd(GETDATE())

            SELECT 
                cp.Name,
                sector.Name AS SectorName,
                skuP.Name AS PlanName,
                brand.Name as BrandName,
                Period,
                IIF(mt.InventoryStatus=1,1,0) as InventoryStatus
                FROM MarketTourREF
            JOIN MTMerchandasingREF AS mt ON MarketTourREF.ID=mt.MarketTourID
            LEFT JOIN SKUMainREF AS sku ON mt.SKUMainID=sku.ID
            LEFT JOIN SKUPlanREF AS skuP ON skuP.ID = sku.SKUPlanID
            LEFT JOIN CounterpartiesREF AS cp ON MarketTourREF.CounterpartyID = cp.ID 
            LEFT JOIN CounterpartySectorsREF AS sector ON cp.SectorID = sector.ID
            LEFT JOIN BrandsREF AS brand ON sku.BrandID = brand.ID

            WHERE Period BETWEEN @Date_From AND @Date_To
            --GROUP BY cp.Name,sector.Name,skuP.Name,brand.Name,Period,InventoryStatus 
                    """
        cursor.execute(q)
        merch = cursor.fetchall()
    for m in merch:
        i = Merchant(counterparty=m[0],sector=m[1],sku=m[2],brand=m[3],date=m[4],status=m[5])
        i.save()
    print('\n____New data saved in DB\n')
    return render(request,'index.html')

def IndexView(request):
    return render(request,'index.html')

def InventoryView(request):
    brands_list = Merchant.objects.values('brand').order_by('brand').distinct()
    sectors_list = Merchant.objects.values('sector').order_by('sector').distinct()
    context = {
        'brands':brands_list,
        'sectors':sectors_list}
    return render(request,'inventory.html',context)

def InventoryPerView(request):
    brands_list = Merchant.objects.values('brand').order_by('brand').distinct()
    sectors_list = Merchant.objects.values('sector').order_by('sector').distinct()
    context = {
        'brands':brands_list,
        'sectors':sectors_list}
    return render(request,'inventory_per.html',context)

@csrf_exempt
def InventoryAjax(request):
    brand_name = request.POST.get('brand')#get brand name from user selection
    sector_name = request.POST.get('sector')
    date_after = request.POST.get('date_after')
    print('date_after:',date_after)
    
    date_bef = request.POST.get('date_bef')
    print('date_bef:',date_bef)
    data = dict() # create empty dictionary

    # set up the data
    #merch = Merchant.objects.filter(brand__startswith=brand_name,sector__startswith=sector_name,date__range=[date_after,date_bef]).only('counterparty','sku','status').order_by('counterparty')
    merch = Merchant.objects.filter(date__range=[date_after,date_bef]).only('counterparty','sku','status').order_by('counterparty')
    
    if(brand_name):
        merch = merch.filter(brand__startswith=brand_name).only('counterparty','sku','status').order_by('counterparty')
    if(sector_name):
        merch = merch.filter(sector__startswith=sector_name).only('counterparty','sku','status').order_by('counterparty')
    
    print(len(merch))
    data_from_db = [ (m.counterparty,m.sku,m.status) for m in merch ]
    
    df = pd.DataFrame(data_from_db,columns=['counterparty','sku','status'])
    
    df_pivot = df.pivot_table(values=['counterparty','status'],index=['counterparty'],columns=['sku'],aggfunc={'status':max})
    df_values = df_pivot.values.tolist()
    df_index = df_pivot.index.values.tolist()
    data["data"] = []
    for i in range(len(df_index)):
        data["data"].append([df_index[i]] + df_values[i])
    print('data size is:',len(data['data']))
    col_names = df_pivot.columns.values
    data['columns'] = [{ "name": "Counterparty", "title":"Торговая точка" , "targets": 0 }]
    for i,n in enumerate(col_names):
        data['columns'].append({"name":n[1],"title":n[1],"targets":i+1})
    print('columns size:',len(data['columns']))
    data['tt_len'] = len(data['data'])
    data['col_len'] = len(data['columns'])

    
    return JsonResponse(data,safe=False)

@csrf_exempt
def InventoryPerAjax(request): #Ajax ,for 2nd page with percents
    brand_name = request.POST.get('brand')#get brand name from user selection
    sector_name = request.POST.get('sector')
    date_after = request.POST.get('date_after')
    print('date_after:',date_after)
    date_bef = request.POST.get('date_bef')
    print('date_bef:',date_bef)
    
    data = dict() # create empty dictionary

    # set up the data
    if(brand_name):
        print('brand name is set')
    merch = Merchant.objects.filter(brand__startswith=brand_name,sector__startswith=sector_name,date__range=[date_after,date_bef]).only('counterparty','sku','status').order_by('counterparty')#[:100]
    print(len(merch))
    
    data_from_db = [ (m.counterparty,m.sku,m.status) for m in merch ]
    
    df = pd.DataFrame(data_from_db,columns=['counterparty','sku','status'])
    
    df_pivot = df.pivot_table(values=['counterparty','status'],index=['counterparty'],columns=['sku'],aggfunc='mean')
    df_pivot = df_pivot.select_dtypes(include=['number'])*100
    df_values = df_pivot.values.tolist()
    df_index = df_pivot.index.values.tolist()
    
    data["data"] = []
    for i in range(len(df_index)):
        data["data"].append([df_index[i]] + df_values[i])
    print('data size is:',len(data['data']))
    
    col_names = df_pivot.columns.values
    data['columns'] = [{ "name": "Counterparty", "title":"Торговая точка" , "targets": 0 }]
    for i,n in enumerate(col_names):
        data['columns'].append({"name":n[1],"title":n[1],"targets":i+1})
    print('columns size:',len(data['columns']))

    
    return JsonResponse(data,safe=False)

