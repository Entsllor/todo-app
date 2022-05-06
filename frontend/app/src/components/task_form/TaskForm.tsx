import React, {useState} from "react";
import TasksService from "../../services/tasksService";

const TaskForm: React.FC<{ tasksUpdater: CallableFunction }> = (props) => {
  const createTask = async () => {
    await TasksService.createTask(title, description, deadline);
    props.tasksUpdater()
  }

  const [description, setDescription] = useState<string>('');
  const [title, setTitle] = useState<string>('')
  const [deadline, setDeadline] = useState<string>('');


  return <div className="TaskForm">
    <div className="card-body">
      <div className="row row-cols-1 row-cols-md-2 h-100">
        <div className="col mb-3">
          <textarea
            id="task-create-input-description"
            className="form-control h-100"
            onChange={event => setDescription(event.target.value)}
            placeholder="description"
          />
        </div>
        <div className="col mb-3">
          <div className="col mb-3">
            <input
              id="task-create-input-title"
              className="form-control"
              type="text"
              onChange={event => setTitle(event.target.value)}
              placeholder="title"
            />
          </div>
          <div className="col mb-3">
            <label htmlFor="task-create-input-deadline"><strong>Deadline</strong></label>
            <input
              id="task-create-input-deadline"
              className="form-control"
              type="datetime-local"
              onChange={event => setDeadline(event.target.value)}
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
