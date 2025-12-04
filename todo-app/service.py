import uuid
import json
import os
from datetime import date, datetime, timedelta
from typing import List, Optional
from models import Task


DATA_FILE = "tasks.json"


class TodoService:
    """Manages the to-do list."""

    def __init__(self):
        self._tasks: List[Task] = []
        self._load_tasks()

    def _save_tasks(self):
        """Saves current tasks to a JSON file."""
        with open(DATA_FILE, "w") as f:
            # Custom encoder for UUID, date, and datetime objects
            serializable_tasks = []
            for task in self._tasks:
                task_dict = task.__dict__.copy()
                task_dict["id"] = str(task_dict["id"])
                if isinstance(task_dict["created_at"], datetime):
                    task_dict["created_at"] = task_dict["created_at"].isoformat()
                if isinstance(task_dict["due_date"], date):
                    task_dict["due_date"] = task_dict["due_date"].isoformat()
                if isinstance(task_dict["next_recurrence_date"], date):
                    task_dict["next_recurrence_date"] = task_dict["next_recurrence_date"].isoformat()
                if isinstance(task_dict["recurrence_start_date"], date):
                    task_dict["recurrence_start_date"] = task_dict["recurrence_start_date"].isoformat()
                if isinstance(task_dict["recurrence_end_date"], date):
                    task_dict["recurrence_end_date"] = task_dict["recurrence_end_date"].isoformat()
                if isinstance(task_dict["reminder_time"], datetime):
                    task_dict["reminder_time"] = task_dict["reminder_time"].isoformat()
                serializable_tasks.append(task_dict)
            json.dump(serializable_tasks, f, indent=4)

    def _load_tasks(self):
        """Loads tasks from a JSON file."""
        if not os.path.exists(DATA_FILE):
            return

        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
                self._tasks = []
                for item in data:
                    # Convert back UUID, date, and datetime objects
                    item["id"] = uuid.UUID(item["id"])
                    if "created_at" in item and isinstance(item["created_at"], str):
                        item["created_at"] = datetime.fromisoformat(item["created_at"])
                    if "due_date" in item and isinstance(item["due_date"], str):
                        item["due_date"] = date.fromisoformat(item["due_date"])
                    if "next_recurrence_date" in item and isinstance(item["next_recurrence_date"], str):
                        item["next_recurrence_date"] = date.fromisoformat(item["next_recurrence_date"])
                    if "recurrence_start_date" in item and isinstance(item["recurrence_start_date"], str):
                        item["recurrence_start_date"] = date.fromisoformat(item["recurrence_start_date"])
                    if "recurrence_end_date" in item and isinstance(item["recurrence_end_date"], str):
                        item["recurrence_end_date"] = date.fromisoformat(item["recurrence_end_date"])
                    if "reminder_time" in item and isinstance(item["reminder_time"], str):
                        item["reminder_time"] = datetime.fromisoformat(item["reminder_time"])
                    self._tasks.append(Task(**item))
            except json.JSONDecodeError:
                self._tasks = []


    def add_task(
        self,
        title: str,
        description: str,
        priority: int,
        due_date: Optional[date],
        tags: List[str],
        recurrence_pattern: Optional[str] = None,
        recurrence_start_date: Optional[date] = None,
        recurrence_end_date: Optional[date] = None,
        reminder_time: Optional[datetime] = None,
    ) -> Task:
        """Adds a new task to the list."""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            tags=tags,
            recurrence_pattern=recurrence_pattern,
            recurrence_start_date=recurrence_start_date,
            recurrence_end_date=recurrence_end_date,
            reminder_time=reminder_time,
        )
        if recurrence_pattern:
            task.next_recurrence_date = self._calculate_next_recurrence_date(
                recurrence_start_date or (due_date if due_date else datetime.now().date()),
                recurrence_pattern
            )
        self._tasks.append(task)
        self._save_tasks()
        return task

    def _calculate_next_recurrence_date(
        self, start_date: date, pattern: str
    ) -> Optional[date]:
        """Calculates the next recurrence date based on the pattern."""
        if pattern == "daily":
            return start_date + timedelta(days=1)
        elif pattern == "weekly":
            return start_date + timedelta(weeks=1)
        elif pattern == "monthly":
            # Advance monthly: handle month end overflows more accurately
            year = start_date.year
            month = start_date.month + 1
            if month > 12:
                month = 1
                year += 1
            # Get the last day of the next month
            last_day_of_next_month = (date(year, month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            # Take the minimum of the original day and the last day of the next month
            day = min(start_date.day, last_day_of_next_month.day)
            return date(year, month, day)
        elif pattern == "yearly":
            return start_date.replace(year=start_date.year + 1)
        return None

    def get_all_tasks(self) -> List[Task]:
        """Returns all tasks in the list."""
        return self._tasks.copy()

    def get_task_by_id(self, task_id: uuid.UUID) -> Optional[Task]:
        """Gets a task by its ID."""
        return next((task for task in self._tasks if task.id == task_id), None)

    def update_task(
        self,
        task_id: uuid.UUID,
        title: str,
        description: str,
        priority: int,
        due_date: Optional[date],
        tags: List[str],
        recurrence_pattern: Optional[str] = None,
        recurrence_start_date: Optional[date] = None,
        recurrence_end_date: Optional[date] = None,
        reminder_time: Optional[datetime] = None,
    ) -> Optional[Task]:
        """Updates a task's details."""
        task = self.get_task_by_id(task_id)
        if task:
            task.title = title
            task.description = description
            task.priority = priority
            task.due_date = due_date
            task.tags = tags
            task.recurrence_pattern = recurrence_pattern
            task.recurrence_start_date = recurrence_start_date
            task.recurrence_end_date = recurrence_end_date
            task.reminder_time = reminder_time
            if recurrence_pattern:
                task.next_recurrence_date = self._calculate_next_recurrence_date(
                    recurrence_start_date or (due_date if due_date else datetime.now().date()),
                    recurrence_pattern
                )
            self._save_tasks()
            return task
        return None

    def mark_task_complete(self, task_id: uuid.UUID) -> Optional[Task]:
        """Marks a task as complete."""
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = True
            self._save_tasks()
            return task
        return None

    def delete_task(self, task_id: uuid.UUID) -> bool:
        """Deletes a task from the list."""
        task = self.get_task_by_id(task_id)
        if task:
            self._tasks.remove(task)
            self._save_tasks()
            return True
        return False

    def search_tasks(self, keyword: str) -> List[Task]:
        """Searches for tasks by keyword in title or description."""
        return [
            task
            for task in self._tasks
            if keyword.lower() in task.title.lower()
            or keyword.lower() in task.description.lower()
        ]

    def filter_tasks(
        self, status: Optional[bool], priority: Optional[int], tag: Optional[str]
    ) -> List[Task]:
        """Filters tasks by status, priority, or tag."""
        tasks = self._tasks.copy()
        if status is not None:
            tasks = [task for task in tasks if task.completed == status]
        if priority is not None:
            tasks = [task for task in tasks if task.priority == priority]
        if tag is not None:
            tasks = [task for task in tasks if tag in task.tags]
        return tasks

    def sort_tasks(self, sort_by: str, reverse: bool = False) -> List[Task]:
        """Sorts tasks by a given key."""
        return sorted(self._tasks, key=lambda task: getattr(task, sort_by), reverse=reverse)

    def generate_recurring_tasks(self) -> None:
        """Generates new instances of recurring tasks if their next recurrence date has passed."""
        today = datetime.now().date()
        new_tasks = []
        for task in self._tasks:
            # Check if it's a recurring task, not completed, and due for recurrence
            if (
                task.recurrence_pattern
                and task.next_recurrence_date
                and task.next_recurrence_date <= today
                and (not task.recurrence_end_date or task.recurrence_end_date >= today)
            ):
                # Create a new task instance
                new_task = Task(
                    title=task.title,
                    description=task.description,
                    priority=task.priority,
                    due_date=self._calculate_next_recurrence_date(task.next_recurrence_date, task.recurrence_pattern),
                    tags=list(task.tags),
                    recurrence_pattern=task.recurrence_pattern,
                    recurrence_start_date=task.recurrence_start_date,
                    recurrence_end_date=task.recurrence_end_date,
                )
                new_tasks.append(new_task)

                # Update the next recurrence date for the original task
                while task.next_recurrence_date and task.next_recurrence_date <= today:
                    task.next_recurrence_date = self._calculate_next_recurrence_date(
                        task.next_recurrence_date, task.recurrence_pattern
                    )
                    if task.recurrence_end_date and task.next_recurrence_date and task.next_recurrence_date > task.recurrence_end_date:
                        task.next_recurrence_date = None # Stop recurrence

        self._tasks.extend(new_tasks)
        if new_tasks:  # Only save if new tasks were actually added
            self._save_tasks()

    def check_for_reminders(self) -> List[Task]:
        """Checks for tasks with upcoming or past-due reminders."""
        now = datetime.now()
        reminders_due = []
        for task in self._tasks:
            if task.reminder_time and not task.completed and task.reminder_time <= now:
                reminders_due.append(task)
        return reminders_due
