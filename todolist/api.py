from datetime import datetime

from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from ninja import NinjaAPI
from ninja.security import django_auth

from todolist.models import Creds, Task, TaskData, TaskModel

api = NinjaAPI(csrf=True)


@api.post("/sign_up", tags=["auth"], response={201: str, 401: str})
@csrf_exempt
def sign_up(request, data: Creds):
    try:
        user = User.objects.create_user(data.login, data.login, data.password)
        login_user(request, user)
        return 201, f"{user}"
    except Exception as err:
        return 401, f"{err}"


@api.post("/sign_in", tags=["auth"])
@csrf_exempt
def sign_in(request, data: Creds):
    user = authenticate(username=data.login, password=data.password)
    if user is not None:
        login_user(request, user)
        return f"Authenticated user {user}"
    else:
        return f"Not authenticated"


@api.get("/sign_out", tags=["auth"], auth=django_auth)
def sign_out(request):
    logout_user(request)
    return f"{request.auth}"


@api.get("/tasks", tags=["todo"], auth=django_auth)
def get_task(request):
    tasks = Task.objects.filter(owner=request.auth)
    return [TaskModel.from_orm(task) for task in tasks]


@api.post("/tasks", tags=["todo"], auth=django_auth)
@csrf_exempt
def create_task(request, task: TaskData):
    task = Task.objects.create(**task.dict(), created_at=datetime.now(), is_active=True, owner=request.auth)
    return TaskModel.from_orm(task)


@api.post("/task/{id}/deactive", tags=["todo"], auth=django_auth)
@csrf_exempt
def active_task(request, id: int):
    try:
        task = Task.objects.get(id=id, owner=request.auth)
        task.is_active = False
        task.save()
        return TaskModel.from_orm(task)
    except Exception as err:
        return f"{err}"


@api.put("/task/{id}", tags=["todo"], auth=django_auth)
@csrf_exempt
def update_task(request, id: int, data: TaskData):
    try:
        task = Task.objects.get(id=id, owner=request.auth)
        task.title = data.title if data.title else task.title
        task.text = data.text if data.text else task.text
        task.save()
        return TaskModel.from_orm(task)
    except Exception as err:
        return f"{err}"


@api.delete("/task/{id}", tags=["todo"], auth=django_auth)
@csrf_exempt
def delete_task(request, id: int):
    try:
        task = Task.objects.get(id=id, owner=request.auth)
        task.delete()
        return "deleted"
    except Exception as err:
        return f"{err}"
