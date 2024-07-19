document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.task-checkbox').forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            const taskId = this.getAttribute('data-task-id');
            const completed = this.checked;

            fetch('/complete_task', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ task_id: taskId, completed: completed })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Task updated successfully');
            })
            .catch(error => {
                console.error('Error updating task:', error);
            });
        });
    });
});
