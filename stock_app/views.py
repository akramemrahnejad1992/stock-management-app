from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Stock, UserStock, Price
from .serializers import StockSerializer, UserStockSerializer
from rest_framework.permissions import IsAuthenticated
from .forms import StockDataForm
from .utils import download_stock_data
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

def home(request):
    all_stocks = Stock.objects.all()
    available_stocks = all_stocks
    # Get selected stocks for the logged-in user
    if request.user.is_authenticated:
        selected_stocks = UserStock.objects.filter(user=request.user).values_list('stock_id', flat=True)
        # Filter stocks to show only those that are not selected
        available_stocks = all_stocks.exclude(id__in=selected_stocks)
        if request.method == 'POST':
            selected_stocks = request.POST.getlist('stocks')
            print(selected_stocks, 'selected_stocks')
            for stock_id in selected_stocks:
                UserStock.objects.get_or_create(user=request.user, stock_id=stock_id)
            return redirect('dashboard')
    return render(request, 'stocks/home.html', {'all_stocks':all_stocks, 'stocks': available_stocks})
    
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a token for the user
            Token.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'stocks/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Render the login template with an error message
            return render(request, 'stocks/login.html', {'error': 'Invalid credentials'})

    return render(request, 'stocks/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        selected_stocks = UserStock.objects.filter(user=request.user).select_related('stock')
        stock_data = {}
        # Fetch price data for each selected stock
        for data in selected_stocks:
            prices = Price.objects.filter(stock=data.stock).order_by('date')  # Get prices for the stock
            stock_data[data.stock.symbol] = {
                'dates':[price.date.strftime('%Y-%m-%d') for price in prices],
                'open':[price.open_price for price in prices],
                'high':[price.high_price for price in prices],
                'low':[price.low_price for price in prices],
                'close': [price.close_price for price in prices],
            }
        return render(request, 'stocks/dashboard.html', {'selected_stocks': selected_stocks, 'stock_data':stock_data})
    return redirect('home')

def stock_lists(request):
    stocks = Stock.objects.all()
    if request.method == 'POST':
        selected_stocks = request.POST.getlist('stocks')
        for stock_id in selected_stocks:
            UserStock.objects.get_or_create(user=request.user, stock_id=stock_id)
        return redirect('dashboard')
    return render(request, 'stocks/stock_list.html', {'stocks': stocks})


@login_required
def stock_data_view(request):
    status_message = 'An Error Occured in data fetching...'
    if request.method == 'POST':
        form = StockDataForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            period = form.cleaned_data['period']
            result_data = download_stock_data(symbol, period, start_date, end_date, user=request.user)
            if len(result_data):
                status_message = 'Data Downloaded Successfully and Saved in DB...'
            return render(request, 'stocks/stock_data_form.html', {'form': form, 'status_message':status_message})
    else:
        form = StockDataForm()
    return render(request, 'stocks/stock_data_form.html', {'form': form})


@login_required
def generate_token(request):
    token = None
    if request.method == 'POST':
        token, created = Token.objects.get_or_create(user=request.user)
    return render(request, 'stocks/generate_token.html', {'token': token})

class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
    operation_description="List all stocks",
    responses={200: StockSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific stock",
        responses={200: StockSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class UserStockViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserStockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserStock.objects.filter(user=self.request.user)
    
    @swagger_auto_schema(
        operation_description="List all stocks for the authenticated user",
        responses={
            200: UserStockSerializer(many=True),
            401: "Authentication credentials were not provided."
        },
        security=[{'Token': []}]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific stock for the authenticated user",
        responses={
            200: UserStockSerializer(),
            401: "Authentication credentials were not provided.",
            404: "Not found."
        },
        security=[{'Token': []}]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

