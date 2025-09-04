from django.urls import path
from .views import (
    PersonaList, ActualizarPersona, CrearPersona, PersonaByDocumento, EliminarPersona,
    TList, UpdateTarea,  Delete_Tarea, Tarea_Date, Tarea_Persona, TareaRangoFecha
)

urlpatterns = [
    # Operaciones de personas
    path('personas/', PersonaList.as_view(), name='persona-list'),           # GET: listar todas
    path('personas/crear/', CrearPersona.as_view(), name='persona-create'),  # POST: crear nueva
    path('personas/<int:pk>/', ActualizarPersona.as_view(), name='persona-update'),  # PUT: actualizar
    path('personas/buscar/<str:documento>/', PersonaByDocumento.as_view(), name='persona-search'),
    path('personas/eliminar/<int:pk>/', EliminarPersona.as_view(), name='persona-delete'),  # DELETE: eliminar
    path('tareas/', TList.as_view(), name='tarea-list'),                 # GET: listar todas las tareas
    path('tareas/persona/<str:documento>/', Tarea_Persona.as_view(), name='tareas-by-persona'),  # GET: tareas por persona
    path('tareas/crear/', UpdateTarea.as_view(), name='tarea-create'),        # POST: crear nueva tarea
    path('tareas/eliminar/<int:pk>/', Delete_Tarea.as_view(), name='tarea-delete'),  # DELETE: eliminar tarea
    path('tareas/fecha/<str:fecha>/', Tarea_Date.as_view(), name='tareas-by-date'),  # GET: tareas por fecha límite
    path('tareas/rango/<str:inicio>/<str:fin>/', TareaRangoFecha.as_view(), name='tareas-by-date-range'),  # GET: tareas por rango de fechas
]
