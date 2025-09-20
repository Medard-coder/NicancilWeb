from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cita
from .forms import CitaForm

@login_required
def lista_citas(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita creada exitosamente.')
            return redirect('lista_citas')
        else:
            messages.error(request, 'Error al crear la cita. Revisa los datos.')
    else:
        form = CitaForm()
    
    citas = Cita.objects.all().order_by('-fecha_cita')
    
    context = {
        'form': form,
        'citas': citas,
    }
    return render(request, 'citas/lista_citas.html', context)