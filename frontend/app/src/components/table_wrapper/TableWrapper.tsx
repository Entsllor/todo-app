import React, {useEffect, useState} from "react";
import TableInner from "../table/TableInner"
import {ITask} from "../../interfaces";
import TasksService from "../../services/tasksService";
import TaskForm from "../task_form/TaskForm"

const TableWrapper: React.FC = () => {
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
            <div className="main-card-title">Main Table</div>
            <TableInner updater={updateTasks} tasks={tasks}/>
            <TaskForm updater={updateTasks}/>
        </div>
    </div>
};

export default TableWrapper;
