from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .forms import DataFileForm
from .models import DataFile
from .utils import RocketDataAnalyzer
from datetime import datetime
import os
import json

def upload_file(request):
    if request.method == 'POST':
        form = DataFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Archivo subido correctamente')
            return redirect('analyze:dashboard')
        else:
            messages.error(request, '❌ Error al subir el archivo')
            return redirect('analyze:dashboard')
    
    # Si llega GET, redirigir al dashboard
    return redirect('analyze:dashboard')

def dashboard(request):
    files = DataFile.objects.all()
    form = DataFileForm()
    return render(request, 'analyze/dashboard.html', {'files': files, 'form': form})

def file_analyze(request, file_id):
    data_file = get_object_or_404(DataFile, id=file_id)
    
    # Analizar el archivo
    analyzer = RocketDataAnalyzer(data_file.file.path)
    stats = analyzer.get_basic_stats()
    matplotlib_plot = analyzer.create_matplotlib_plots()
    interactive_plots = analyzer.create_interactive_plots()
    combined_plot = analyzer.create_combined_plot()
    
    # Obtener el tipo de análisis solicitado
    analysis_type = request.GET.get('analysis', 'basic')
    
    # Obtener fecha específica para datos meteorológicos (si se proporciona)
    weather_date = request.GET.get('weather_date', None)  # Formato: YYYY-MM-DD
    
    advanced_analysis = {}
    if analysis_type == 'complete':
        # Realizar análisis completo de todos los requerimientos
        advanced_analysis = analyzer.get_comprehensive_analysis(weather_date=weather_date)
    
    context = {
        'file': data_file,
        'stats': stats,
        'matplotlib_plot': matplotlib_plot,
        'interactive_plots': interactive_plots,
        'combined_plot': combined_plot,
        'analysis_type': analysis_type,
        'advanced_analysis': advanced_analysis,
        'today': datetime.now().date(),  # Para limitar el selector de fecha
    }
    
    return render(request, 'analyze/file_detail.html', context)

def delete_file(request, file_id):
    data_file = get_object_or_404(DataFile, id=file_id)

    # Eliminar el fichero del storage (si existe)
    if data_file.file:
        try:
            data_file.file.delete(save=False)
        except Exception:
            # opcional: registrar el error si usas logging
            pass

    # Eliminar la instancia de la base de datos
    data_file.delete()
    messages.success(request, '✅ Archivo eliminado correctamente')
    return redirect('analyze:dashboard')

def api_file_stats(request, file_id):
    """API endpoint para obtener estadísticas del archivo"""
    data_file = get_object_or_404(DataFile, id=file_id)
    analyzer = RocketDataAnalyzer(data_file.file.path)
    stats = analyzer.get_basic_stats()
    
    return JsonResponse(stats)