from blogapp.models import users,posts

# authenticate
# username
# password

#user={"id": 1, "username": "akhil", "email": "akhil@gmail.com", "password": "Password@123"},

# user=[user for user in users if user["username"]==username and user["password"]==password]
# print(user)

# def authenticate(username,password):
#     user = [user for user in users if user["username"] == username and user["password"] == password]
#     return user
# print(authenticate("anu","Password@123"))
def signinrequired(fn):
     def wrapper(*args,**kwargs):
         if "user" in session:
             return fn(*args,**kwargs)
         else:
             print("you must login")

     return wrapper



session={}

def authenticate(**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user = [user for user in users if user["username"] == username and user["password"] == password]
    return user
print(authenticate(username="anu",password="Password@123"))


class Signinview:
     def post(self,*args,**kwargs):
         username=kwargs.get("username")
         password=kwargs.get("password")
         user=authenticate(username=username,password=password)
         if user:
             session["user"]=user[0]
             print("success")
         else:
             print("invalid")


class Postview():
    @signinrequired
    def get(self,*args,**kwargs):
        return posts

    @signinrequired
    def post(self,*args,**kwargs):
        userId=session["user"]["id"]
        kwargs["userID"]=["userid"]
        posts.append(kwargs)
        print(posts)



class Mypostlistview():

    @signinrequired
    def get(self,*args,**kwargs):
        print(session)
        userId=session["user"]["id"]
        print(userId)
        my_post=[post for post in posts if post["userId"]==userId]
        return my_post



class Postdetailsview:

    def get_object(self,id):
        post=[post for post in posts if post["postId"]==id]
        return post

    @signinrequired
    def get(self,*args,**kwargs):
        post_id=kwargs.get("post_id")
        post=self.get_object(post_id)
        return post

    @signinrequired
    def delete(self,*args,**kwargs):
        post_id=kwargs.get("post_id")
        data=self.get_object(post_id)
        if data:
            post=data[0]
            posts.remove(post)
            print("post removed")
            print(len(posts))

    def put(self,*args,**kwargs):
        post_id=kwargs.get("post_id")
        instance=self.get_object(post_id)
        data=kwargs.get("data")
        if instance:
            post_obj=instance[0]
            post_obj.update(data)
            return post_obj

class Likeview:

    @signinrequired
    def get(self,*args,**kwargs):
        postid=kwargs.get("postid")
        post=[post for post in posts if post["postId"]==postid]
        if post:
            post=post[0]
            userid = session["user"]["id"]
            post["liked_by"].append(userid)
            # print(post["liked_by"])
            print(post)

@signinrequired
def signout(*args,**kwargs):
    user=session.pop("user")
    print(f"the user {user['username']} has been logged out")


log=Signinview()
log.post(username="richard",password="Password@123")


like=Likeview()
like.get(postid=6)

signout()

# mypost=Mypostlistview()
# print(mypost.get())



# p=Postdetailsview()
# p.delete(post_id=6)
# print(p.get(post_id=6))
#
# data={
#     "title":"hai hello"
# }
# p=Postdetailsview()
# print(p.put(post_id=4,data=data))

# data=Postview()
# print(data.get())
#
# data.post(postId=9,
#           title="hai  world",
#           content="ghghjgj",
#           liked_by=[])






