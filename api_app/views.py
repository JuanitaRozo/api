from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404

from .models import Persona,Tarea
from .serializers import PersonaSerializer, TareaSerializer

# Create your views here.
class PersonaList(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    
    def get(self, request):
        personas = Persona.objects.all()
        serializer = PersonaSerializer(personas, many=True)
        if not personas:
            raise NotFound('No se encontraron personas')
        return Response({'success': True, 'detail': 'listado de personas', 'data': serializer.data}, status=status.HTTP_200_OK)


# Crear personas
class CrearPersona(generics.CreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def post(self, request):
        serializer = PersonaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'detail': 'Persona creada', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    
    
#Actualizar personas
class ActualizarPersona(generics.UpdateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def put(self, request, pk):
        persona = get_object_or_404(Persona, pk=pk)
        
        #verifica si email ha cambiado
        email = request.data.get('email')
        if email and email != persona.email:
            # verificar si ya existe otra persona con el mismo email
            if Persona.objects.filter(email=email).exclude(pk=pk).exists():
                return Response({'email':['Este email ya está en uso por otra persona.']}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PersonaSerializer(persona, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'detail': 'Persona actualizada', 'data': serializer.data}, status=status.HTTP_200_OK)
    
    
# buscar persona por documento
class PersonaByDocumento(generics.ListAPIView):
    serializer_class = PersonaSerializer

    def get(self, request, documento):
        persona = Persona.objects.filter(documento=documento).first()
        if not persona:
            raise NotFound('Persona no encontrada con este documento')
        serializer = PersonaSerializer(persona)
        return Response({'success': True, 'detail': 'Persona encontrada', 'data': serializer.data}, status=status.HTTP_200_OK)
    


class EliminarPersona(generics.DestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def delete(self, request, pk):
        persona = get_object_or_404(Persona, pk=pk)
        persona.delete()
        return Response({'success': True, 'detail': 'Persona eliminada'}, status=status.HTTP_204_NO_CONTENT)



#Tareas
class TList(generics.ListCreateAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    def get(self, request):
        tareas = Tarea.objects.all()
        serializer = TareaSerializer(tareas, many=True)
        if not tareas:
            raise NotFound('Ruta no encontrada')
        return Response({'success': True, 'detail': 'Listado', 'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TareaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'detail': 'Tarea creada', 'data': serializer.data}, status=status.HTTP_201_CREATED)



class UpdateTarea(generics.UpdateAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    def put(self, request, pk):
        tarea = get_object_or_404(Tarea, pk=pk)
        serializer = TareaSerializer(tarea, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'detail': 'Actualizada', 'data': serializer.data}, status=status.HTTP_200_OK)


class Delete_Tarea(generics.DestroyAPIView):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    def delete(self, request, pk):
        tarea = get_object_or_404(Tarea, pk=pk)
        tarea.delete()
        return Response({'success': True, 'detail': 'Tarea eliminada'}, status=status.HTTP_204_NO_CONTENT)


class Tarea_Date(generics.ListAPIView):
    serializer_class = TareaSerializer

    def get(self, request, fecha):
        tareas = Tarea.objects.filter(fecha_limite=fecha)
        if not tareas:
            raise NotFound('No se encontraron')
        serializer = TareaSerializer(tareas, many=True)
        return Response({'success': True, 'detail': 'Tareas por fecha ', 'data': serializer.data}, status=status.HTTP_200_OK)


class TareaRangoFecha(generics.ListAPIView):
    serializer_class = TareaSerializer

    def get(self, request, inicio, fin):
        tareas = Tarea.objects.filter(fecha_limite__range=[inicio, fin])
        if not tareas:
            raise NotFound('No se encontraron')
        serializer = TareaSerializer(tareas, many=True)
        return Response({'success': True, 'detail': 'Tareas por rango de fechas', 'data': serializer.data}, status=status.HTTP_200_OK)


class Tarea_Persona(generics.ListAPIView):
    serializer_class = TareaSerializer

    def get(self, request, documento):
        persona = Persona.objects.filter(documento=documento).first()
        if not persona:
            raise NotFound('No existe registro de persona con este numero de documento')
        tareas = Tarea.objects.filter(persona=persona)
        serializer = TareaSerializer(tareas, many=True)
        return Response({'success': True, 'detail': f'lista de pendientes de: {persona.nombre}', 'data': serializer.data}, status=status.HTTP_200_OK)