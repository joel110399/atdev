from django.shortcuts import render

import pandas as pd


def home(request):
    if request.method == 'POST':

        salary = int(request.POST['salary'] if request.POST['salary'] != '' else 0)
        anual_salary = salary * 12

        # Calcular porcentaje de impuesto sobre la renta
        if anual_salary >= 416220 and anual_salary <= 624329:
            surplus = anual_salary - 416220
            anual_salary = anual_salary - (surplus * 0.15)
            salary = anual_salary / 12

        elif anual_salary >= 624329 and anual_salary <= 867123:
            surplus = anual_salary - 624329
            anual_salary = anual_salary - 31216 - (surplus * 0.20)
            salary = anual_salary / 12

        elif anual_salary >= 867123:
            surplus = anual_salary - 867123
            anual_salary = anual_salary - 79776 - (surplus * 0.25)
            salary = anual_salary / 12
            
        # Decuento AFP 2.87
        salary = salary - (salary * 2.87/100)

        # Descuento Health Insurance 3.04
        salary = salary - (salary * 3.04/100)
        
        salary = round(salary, 2)
        salary = 'RD$ {:,.2f}'.format(float(salary))

        context = {
            "result": salary,
        }

        return render(request, 'index.html', context=context)

    return render(request, 'index.html')


def dashboard(request):

    if request.method == 'POST' and request.FILES['file_excel']:
          
        attachment = request.FILES['file_excel']
        df = pd.read_excel(attachment)

        quality = []
        customer_experience = []
        call_time = []
        hours_completed = []

        for inx, dic in df.iterrows():
            quality.append(dic['Quality'])
            customer_experience.append(dic['Customer Experience'])
            call_time.append(dic['Time of the call'])
            hours_completed.append(dic['Hours completed'])

        context = {
            'quality': {
                'high': len(list(filter(lambda x: x == 'high', quality))),
                'medium': len(list(filter(lambda x: x == 'medium', quality))),
                'low': len(list(filter(lambda x: x == 'low', quality))),
                'total': len(quality),
            },
            'customer_experience': {
                'good': len(list(filter(lambda x: x == 'good', customer_experience))),
                'bad': len(list(filter(lambda x: x == 'bad', customer_experience))),
                'total': len(customer_experience),
            },
            'call_time': {
                'min': min(call_time),
                'max': max(call_time),
                'avg': sum(call_time) / len(call_time),
                'total': sum(call_time),
            },
            'hours_completed': {
                'min': min(hours_completed),
                'max': max(hours_completed),
                'avg': sum(hours_completed) / len(hours_completed),
                'total': sum(hours_completed),
            },
        }

        return render(request, 'dashboard.html', context=context)
    return render(request, 'dashboard.html')
