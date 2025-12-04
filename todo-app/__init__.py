"""Todo CLI application package."""

from .models import Task
from .service import TodoService
from todo_app import Task, TodoService

__version__ = "1.0.0"
__all__ = ["Task", "TodoService"]