from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from pydantic import BaseModel


class Task(models.Model):
    title = models.TextField()
    text = models.TextField()
    created_at = models.DateTimeField()
    is_active = models.BooleanField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class TaskData(BaseModel):
    title: str
    text: str


class TaskModel(BaseModel):
    id: int
    title: str
    text: str
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True


class Creds(BaseModel):
    login: str
    password: str
