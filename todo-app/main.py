import typer
from service import TodoService
import ui
import time

app = typer.Typer()
todo_service = TodoService()
todo_service.generate_recurring_tasks() # Generate recurring tasks at startup


def main():
    """A simple CLI to-do app."""
    while True:
        reminders = todo_service.check_for_reminders()
        if reminders:
            for task in reminders:
                ui.show_reminder_notification(task)

        ui.display_menu()
        choice = ui.get_menu_choice()

        if choice == "1":  # Add task
            (
                title,
                description,
                priority,
                due_date,
                tags,
                recurrence_pattern,
                recurrence_start_date,
                recurrence_end_date,
            ) = ui.get_new_task_details()
            task = todo_service.add_task(
                title,
                description,
                priority,
                due_date,
                tags,
                recurrence_pattern,
                recurrence_start_date,
                recurrence_end_date,
            )
            ui.show_confirmation(f"Task '{task.title}' added with ID: {task.id}")

        elif choice == "2":  # View all tasks
            tasks = todo_service.get_all_tasks()
            if tasks:
                ui.display_tasks(tasks)
            else:
                ui.show_error("No tasks found.")

        elif choice == "3":  # Mark task as complete
            task_id = ui.get_task_id()
            task = todo_service.mark_task_complete(task_id)
            if task:
                ui.show_confirmation(f"Task '{task.title}' marked as complete.")
            else:
                ui.show_error("Task not found.")

        elif choice == "4":  # Update task
            task_id = ui.get_task_id()
            (
                title,
                description,
                priority,
                due_date,
                tags,
                recurrence_pattern,
                recurrence_start_date,
                recurrence_end_date,
            ) = ui.get_update_task_details()
            task = todo_service.update_task(
                task_id,
                title,
                description,
                priority,
                due_date,
                tags,
                recurrence_pattern,
                recurrence_start_date,
                recurrence_end_date,
            )
            if task:
                ui.show_confirmation(f"Task '{task.title}' updated.")
            else:
                ui.show_error("Task not found.")

        elif choice == "5":  # Delete task
            task_id = ui.get_task_id()
            if todo_service.delete_task(task_id):
                ui.show_confirmation("Task deleted.")
            else:
                ui.show_error("Task not found.")

        elif choice == "6":  # Search tasks
            keyword = ui.get_search_keyword()
            tasks = todo_service.search_tasks(keyword)
            if tasks:
                ui.display_tasks(tasks)
            else:
                ui.show_error("No tasks found matching the keyword.")

        elif choice == "7":  # Filter tasks
            status, priority, tag = ui.get_filter_options()
            tasks = todo_service.filter_tasks(status, priority, tag)
            if tasks:
                ui.display_tasks(tasks)
            else:
                ui.show_error("No tasks found with the given filters.")

        elif choice == "8":  # Sort tasks
            sort_by, reverse = ui.get_sort_options()
            tasks = todo_service.sort_tasks(sort_by, reverse)
            if tasks:
                ui.display_tasks(tasks)
            else:
                ui.show_error("No tasks to sort.")

        elif choice == "9":  # Exit
            ui.show_confirmation("Exiting...")
            break

        else:
            ui.show_error("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
