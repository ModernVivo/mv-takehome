from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Paper
from .serializers import PaperListSerializer, PaperDetailSerializer
from django.db.models import Q

class PaperListView(generics.ListAPIView):
    serializer_class = PaperListSerializer

    def get_queryset(self):
        queryset = Paper.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(authors__icontains=search)
            )
        return queryset

class PaperDetailView(generics.RetrieveAPIView):
    queryset = Paper.objects.all()
    serializer_class = PaperDetailSerializer

@api_view(['POST'])
def mark_important(request, pk):
    try:
        paper = Paper.objects.get(pk=pk)
    except Paper.DoesNotExist:
        return Response({'error': 'Paper not found.'}, status=404)
    paper.is_important = not paper.is_important
    paper.save()
    return Response({'is_important': paper.is_important})
