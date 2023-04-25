from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go

# Create your views here.
def home(requests) :

    return render(requests, 'DjangoDash/welcome.html')