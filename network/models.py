from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

#faltan models para:
#posts(user on delete cascade/realted name, content nonblank, date), comments(user, post, content, date), likes(user, post liked), followers(user y user followed).
#cada vez que cambio en models tengo que runnear python manage.py makemigrations y python manage.py migrate

#user on delete cascade/realted name, content nonblank, date
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)

#Cuando haga el de likes que sea POST la primary key -- user l osecundarioa pra optimziar el search.
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')


#Necesito el Model de followers...
class Follows(models.Model):
    seguido = models.ForeignKey(User, on_delete=models.CASCADE, related_name="siguiendo")
    seguidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seguidores")
