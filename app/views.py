from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login

def index_page(request):
    return render(request, 'index.html')

def home(request):
    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)
    
    # Paginación con 12 imágenes por página
    paginator = Paginator(images, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'home.html', {
        'page_obj': page_obj,
        'favourite_list': favourite_list
    })

def search(request):
    search_msg = request.POST.get('query', '') or request.GET.get('query', '')
    
    if search_msg:
        images = services.getAllImages(search_msg)
        print(f"Número total de resultados: {len(images)}")  # Imprime el número total de resultados
        favourite_list = services.getAllFavourites(request)
        
        paginator = Paginator(images, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'home.html', {
            'page_obj': page_obj,
            'favourite_list': favourite_list,
            'query': search_msg
        })
    else:
        return redirect('home')

@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', {
        'favourite_list': favourite_list
    })

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    pass


def register(request):
    data = {
        'form': CustomUserCreationForm()
    } 
    
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data = request.POST)
        
        if user_creation_form.is_valid():
            user_creation_form.save()
            
            
            
            user = authenticate(username=user_creation_form.cleaned_data['username'], password= user_creation_form.cleaned_data['password1'])
            login(request,user)
            
            return redirect('home') 
     
        
    
    return render(request, 'registration/registro.html',data)





