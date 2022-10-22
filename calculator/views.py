from django.shortcuts import render

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