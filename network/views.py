from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from itertools import chain
from django.core.paginator import Paginator
from django.shortcuts import render


from .models import User, Post, Follows, Like
from .forms import PostForm

def index(request):
    postForm = PostForm()

    all_posts = Post.objects.all().order_by('-date')
    #Handle likes stuff
    #Aca tendria todos los likes de todos los usuarios no puedo filtrar esto?
    #si yo agarro todos lso IDS de los POSTS que el user puso like lo puedo mandar al front y dsp chequear if post id IN liked posts
    if (request.user.id):
        likedPostIds = Like.objects.filter(user = request.user).values_list('post', flat=True)
    else:
        likedPostIds =[]

    #Bueno me falta solo CONTAR LA CANTIDAD DEL LIKES DE CADA POSSSSSSSST
    likes = {}
    for post in all_posts:
        postLikes = Like.objects.filter(post = post.id).count()
        likes[post.id] = postLikes

    print(all_posts)
    #Pagination a ver:
    paginator = Paginator(all_posts, 10) # Show 10 post per page.
    #El get este calculo que lo mando desde el HTML
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)




    return render(request, "network/index.html", 
                {"postForm": postForm,
                "all_posts": all_posts,
                "newPost": 'true',
                'page_obj': page_obj,
                'likedPostIds': likedPostIds,
                'likes': likes
                }
    )


#view para aseguarme ue el post ande
@login_required
def newpost(request):
    #imagino que aca SAVEO el psot y redriect a la pagina princpial ???
    #return 'test'
    #workea el reDDRIECT
    #user = User.objects.create_user(username, email, password)
    #user.save()
    #recivo los parametros
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
                        #Guardar el post DATA posdata jaja 
            # Save the record
            post = Post(
                #Asi obtengo el current logged in user
                user = User.objects.get(pk=request.user.id),
                text = form.cleaned_data['text']
            )
            post.save()

            return HttpResponseRedirect(reverse("index"))   
    else:
        return HttpResponse(status=405)
    

def editPost(request):
    #Parseo la data del body que viene en el post.
    data = request.body
    data = data.decode('utf-8')
    data = json.loads(data)
    #data es : {'postId': 2, 'text': 'afsdfadsf'}
    #data['postId']

    post = Post.objects.get(pk = data['postId'])
    if(post.user != request.user):
        HttpResponse(status=404) 


    post.text = data['text']
    post.save()

    return HttpResponse(status=200)





def profile(request, username):
    #print(user)
    #USERname ES EL /SODIFJAS osea el user del profile.
    #Chequeo que el profile sea de un user registrado
    user = User.objects.filter(username = username)
    if (not user):
        return render(request, "network/profile.html", {
        "notFound": 'true',
        "message": "The user: " +username + " doesn't exist!"
        })
    #Actually cargo el profile:


    #Cargo los posts del usuario]
    user = User.objects.get(username = username)
    allUserPosts = Post.objects.filter(user = user).order_by('-date')
    #WORKSSS -- Eventualmetne aca voy at ner que buscar los follows y followers, y tmb un flag para ver si el usuario es el usuario del perfil 
    #y tamiben otro flag para que vea si el usuario SIgue o no lo sigue.
    #Tengo que hacer un get en Follows y ver si el usuario logged in sigue al usuario del profile. No se como fijarme el currently logged in tho.

    #Aca ya tengo el total de Seguidores y Seguidos.
    seguidores  = Follows.objects.filter(seguido = user).count()
    seguidos = Follows.objects.filter(seguidor = user).count()

    #Me falta saber si el logged in user sigue al profile user
    #Esto es un if request.user.id in seguidores.
    seguidores_id_list = Follows.objects.filter(seguido = user).values_list('seguidor', flat=True)
    followFlag = 'unfollow' if request.user.id in seguidores_id_list else 'follow'

    paginator = Paginator(allUserPosts, 10) # Show 10 post per page.
    #El get este calculo que lo mando desde el HTML
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #los Likes:
    if (request.user.id):
        likedPostIds = Like.objects.filter(user = request.user).values_list('post', flat=True)
    else:
        likedPostIds =[]

    #Bueno me falta solo CONTAR LA CANTIDAD DEL LIKES DE CADA POSSSSSSSST
    likes = {}
    for post in allUserPosts:
        postLikes = Like.objects.filter(post = post.id).count()
        likes[post.id] = postLikes



    return render(request, "network/profile.html", {
        "userProfile": username,
        "user_id": user.id,
        "page_obj": page_obj,
        "seguidores": seguidores,
        "seguidos":  seguidos,
        "followFlag": followFlag,
        'likedPostIds': likedPostIds,
        'likes': likes
    })


def follow(request):
    
    #Parseo la data del body que viene en el post.
    data = request.body
    data = data.decode('utf-8')
    data = json.loads(data)
    #data es : {'action': 'follow', 'user_id': 3}
    #Action es la accion que tengo que realizar, si es follow insert si es unfollow drop, y user_id es el USER PROFILE, para sabre el logged in request.user.id
    if data['action'] == 'follow':
        # Asignar seguidor   
        following = Follows(
            seguido = User.objects.get(pk=data['user_id']),
            seguidor = User.objects.get(pk=request.user.id)
        )
        following.save()
    else:
        #Desasignar seguidor
        instance = Follows.objects.get(seguido=data['user_id'], seguidor = request.user.id)
        instance.delete()

    return HttpResponse("Correct un/follow")

def unLike(request):
     #Parseo la data del body que viene en el post.
    data = request.body
    data = data.decode('utf-8')
    data = json.loads(data)
    #data es : {'action': 'unlike', 'post_id': 3}
    #Action es la accion que tengo que realizar, si es like agrego una neuva relacion en el model Likes, post viene en data, user id es request.user.id, si un like GET esa relacion y DROp
    if data['action'] == 'like':
        # Asignar like  

        like = Like(
            user = User.objects.get(pk=request.user.id),
            post = Post.objects.get(pk=data['post_id'])
        )
        print(like)
        like.save()
    else:
        #Desasignar Like
        instance = Like.objects.get(user=request.user.id, post = data['post_id'])
        instance.delete()

    return HttpResponse("Correct Like")



@login_required
def following(request):
    #Agarro el current user
    currentUser = User.objects.get(pk = request.user.id)
    #Me fijo a quien sigue el current user
    followingPeople = Follows.objects.filter(seguidor=currentUser)
    #Traigo todo los posts, esto no es SUPER eficiente, pero no se sino como ordenarlos cronologicamente.
    allPosts = Post.objects.all().order_by('date').reverse()

    followingPosts = []
    #Aca loopeo los posts y las personas, y si coincide el usuario que hizo el post con un follow, lo agrego.
    for post in allPosts:
        for person in followingPeople:
            if person.seguido == post.user:
                followingPosts.append(post)

    paginator = Paginator(followingPosts, 10) # Show 10 post per page.
    #El get este calculo que lo mando desde el HTML
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    #los Likes:
    if (request.user.id):
        likedPostIds = Like.objects.filter(user = request.user).values_list('post', flat=True)
    else:
        likedPostIds =[]

    #Bueno me falta solo CONTAR LA CANTIDAD DEL LIKES DE CADA POSSSSSSSST
    likes = {}
    for post in followingPosts:
        postLikes = Like.objects.filter(post = post.id).count()
        likes[post.id] = postLikes



    return render(request, "network/index.html", 
                {
                "page_obj": page_obj,
                'likedPostIds': likedPostIds,
                'likes': likes
                }
    )


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
