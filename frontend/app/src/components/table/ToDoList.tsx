import React from "react";
import {ITask} from "../../interfaces"
import TasksService from "../../services/tasksService";

const ToDoList: React.FC<{ tasks: ITask[], updater: CallableFunction; }> = (props) => {
  let tasks = props.tasks;

  const deleteTask = async (taskID: string) => {
    await TasksService.deleteTask(taskID).catch(() => alert("Failed to delete"));
    props.updater()
  }

  const setTaskStatus = async (taskID: string, newStatus: boolean = true) => {
    await TasksService.updateTask(taskID, {is_completed: newStatus}).catch(() => alert("Failed to update"));
    props.updater()
  }

  return (
    <div className="Table">
      <div style={{overflowX: "auto"}}>
        <table className="table">
          <thead>
          <tr>
            <th>
              Completed
            </th>
            <th>
              Title
            </th>
            <th>
              Deadline
            </th>
            <th>
              Delete
            </th>
          </tr>
          </thead>
          <tbody>
          {tasks
            .sort((a, b) => {
              if (a.is_completed === b.is_completed)
                return a.deadline.localeCompare(b.deadline);
              return a.is_completed ? 1 : -1
            })
            .map(task =>
              <tr key={task.id} className={task.is_completed ? "text-secondary" : ""}>
                <td>
                  <input
                    className="form-check-input"
                    checked={task.is_completed}
                    onInput={() => setTaskStatus(task.id, !task.is_completed)}
                    type="checkbox"
                  />
                </td>
                <td title={task.description}>{task.title}</td>
                <td>{new Date(task.deadline).toLocaleString()}</td>
                <td>
                  <button
                    onClick={() => deleteTask(task.id)}
                    className="btn btn-danger btn-sm">
                    X
                  </button>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ToDoList
