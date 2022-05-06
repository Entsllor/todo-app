import React from "react";
import TasksService from "../../services/tasksService";

const TaskForm: React.FC<{ updater: CallableFunction }> = (props) => {
  const createTask = async () => {
    let descriptionInput = document.getElementById("task-create-input-description")! as HTMLInputElement;
    let titleInput = document.getElementById("task-create-input-title")! as HTMLInputElement;
    let deadlineInput = document.getElementById("task-create-input-deadline")! as HTMLInputElement;
    let description = descriptionInput.value || ""
    let title = titleInput.value || ""
    let deadline = deadlineInput.value || ""
    await TasksService.createTask(title, description, deadline);
    props.updater()
  }

  return <div className="TaskForm">
    <div className="card-body">
      <div className="row row-cols-1 row-cols-md-2 h-100">
        <div className="col mb-3">
                    <textarea
                      id="task-create-input-description"
                      className="form-control h-100"
                      placeholder="description"
                    />
        </div>
        <div className="col mb-3">
          <div className="col mb-3">
            <input
              id="task-create-input-title"
              className="form-control"
              type="text"
              placeholder="title"
            />
          </div>
          <div className="col mb-3">
            <label htmlFor="task-create-input-deadline"><strong>Deadline</strong></label>
            <input
              id="task-create-input-deadline"
              className="form-control"
              type="datetime-local"
              placeholder="deadline"
            />
          </div>
          <button
            className="btn btn-success w-100"
            onClick={() => createTask()}
          >
            Create
          </button>
        </div>
      </div>
    </div>
  </div>;
};

export default TaskForm
