import React, {useEffect, useState} from "react";
import ToDoListList from "../table/ToDoList"
import {ITask} from "../../interfaces";
import TasksService from "../../services/tasksService";
import TaskForm from "../task_form/TaskForm"

const ToDoListWrapper: React.FC = () => {
    const [tasks, setTasks] = useState<ITask[]>([]);
    const updateTasks = async () => {
        let response = await TasksService.getTasks();
        setTasks(response.data)
    }

    useEffect(() => {
            updateTasks()
        }, []
    )


    return <div className="TableWrapper">
        <div className="card">
            <div className="main-card-title">My Tasks</div>
            <ToDoListList updater={updateTasks} tasks={tasks}/>
            <TaskForm updater={updateTasks}/>
        </div>
    </div>
};

export default ToDoListWrapper;
