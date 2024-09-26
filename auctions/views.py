from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Category,Lista,comentarios,bid


def index(request):
    activateList = Lista.objects.filter(activate = True)
    CategoryList = Category.objects.all()
    return render(request, "auctions/index.html",{
        "activateList":activateList,
        "category":CategoryList
        })

def addBids(request, id):
    newBid = request.POST['newBid']
    listData = Lista.objects.get(pk=id)

    # Verificar si el campo 'newBid' no está vacío y es un número
    if not newBid or not newBid.isdigit():
        return render(request, "auctions/listing.html", {
            'dataList': listData,
            'message': "Por favor, ingresa una cantidad válida para la oferta.",
            'update': False,
            'esDueno':esDueno,
        })

    newBid = int(newBid)  # Convertir a entero solo después de validar

    # Verificar si la lista tiene una oferta (bid) asociada
    if listData.price is None or newBid > listData.price.bid_amount:
        # Crear nueva oferta
        updateBid = bid(user=request.user, bid_amount=newBid)
        updateBid.save()

        # Actualizar el precio de la lista con la nueva oferta
        listData.price = updateBid
        listData.save()

        return render(request, "auctions/listing.html", {
            'dataList': listData,
            'message': "Oferta realizada con éxito.",
            'update': True,
            'esDueno':esDueno,
        })
    else:
        return render(request, "auctions/listing.html", {
            'dataList': listData,
            'message': "La oferta debe ser mayor a la oferta actual.",
            'update': False,
            'esDueno':esDueno,
        })

def listing(request, id ):
    listaDetails = Lista.objects.get(pk=id)
    isListWatch  = request.user in listaDetails.listWatch.all()
    allComment = comentarios.objects.filter(listing=listaDetails)
    esDueno = request.user.username == listaDetails.key.username
    return render (request, "auctions/listing.html",{
        'dataList':listaDetails,
        'isListWatch':isListWatch,
        'allComments':allComment,
        'esDueno':esDueno
        })

def close(request,id ):
    listaDetails = Lista.objects.get(pk=id)
    listaDetails.activate = False
    listaDetails.save()
    esDueno = request.user.username == listaDetails.key.username
    isListWatch  = request.user in listaDetails.listWatch.all()
    allComment = comentarios.objects.filter(listing=listaDetails)
    return render (request, "auctions/listing.html",{
        'dataList':listaDetails,
        'isListWatch':isListWatch,
        'allComments':allComment,
        'esDueno':esDueno,
        'message':"la subasta se cerro",
        'update':True, 
        })

def addComment(request,id):
    currentUser = request.user
    listingData = Lista.objects.get(pk=id)
    mensaje = request.POST['newComment']
    newComment = comentarios(
        user=currentUser,
        listing=listingData,
        comentario= mensaje
        )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args =(id,)) )

def viewsLitWatch(request):
    currentUser = request.user
    listing = currentUser.watch_lists.all()
    
    return render(request, "auctions/watchlist.html",{
        'list':listing
        })
    
def removeList(request, id):
    listData = Lista.objects.get(pk= id )
    currentUser = request.user
    listData.listWatch.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args =(id,)) )

def addList(request, id):
    listData = Lista.objects.get(pk= id )
    currentUser = request.user
    listData.listWatch.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args =(id,)) )

def filterCategory(request):
   if request.method == "POST":
    CategoryFrom = request.POST["categoryIndex"]
    # Verifica si se seleccionó "none"
    if CategoryFrom == "none":
        activateList = Lista.objects.filter(activate=True)  
    else:
        category = Category.objects.get(category=CategoryFrom)
        activateList = Lista.objects.filter(activate=True, category=category)
    
    CategoryList = Category.objects.all()
    
    return render(request, "auctions/index.html", {
        "activateList": activateList,
        "category": CategoryList,
        "elementCat":CategoryFrom
    })

def PageList(request):
    if request.method == "GET":
        allCategory = Category.objects.all()
        return render(request, "auctions/create.html", {
            "Category": allCategory,
        })
    else:
        title = request.POST["Title"]
        description = request.POST["Description"]
        price = request.POST["Price"]
        url = request.POST["URL"]
        category = request.POST["Category"]

        currentUser = request.user  # Usuario actual

        # Verificamos que la categoría exista. Si 'category' es un nombre único, funciona bien.
        dateCategory = Category.objects.get(category=category)

        # Creación de la oferta (bid) con el nombre del campo correcto
        Bid = bid(bid_amount=float(price), user=currentUser)
        Bid.save()

        # Creación de la nueva lista/artículo
        newList = Lista(
            title=title,
            description=description,
            price=Bid,  # Asociamos la oferta creada con el nuevo artículo
            url=url,
            category=dateCategory,
            key=currentUser,
        )
        newList.save()

        # Redirigimos al índice (asegúrate que 'index' está correctamente definido)
        return HttpResponseRedirect(reverse('index'))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
