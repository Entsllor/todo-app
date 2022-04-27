import React from "react";
import {ITask} from "../../interfaces"
import TasksService from "../../services/tasksService";

const TableInner: React.FC<{ tasks: ITask[], updater: CallableFunction; }> = (props) => {
    let tasks = props.tasks;

    const deleteTask = async (taskID: string) => {
        await TasksService.deleteTask(taskID).catch(() => alert("Failed to delete"));
        props.updater()
    }

    return (
        <div className="Table">
            <div style={{overflowX: "auto"}}>
                <table className="table">
                    <thead>
                    <tr>
                        <th>
                            Title
                        </th>
                        <th>
                            Deadline
                        </th>
                        <th>
                            Status
                        </th>
                        <th>
                            Delete
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    {tasks.map(task =>
                        <tr key={task.id}>
                            <td>{task.title}</td>
                            <td>{task.deadline}</td>
                            <td>{task.status}</td>
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

export default TableInner
