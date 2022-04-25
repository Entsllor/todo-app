import React from "react";
import {ITask} from "../../interfaces"

const TableInner: React.FC<{ tasks: ITask[] }> = (props) => {
    let tasks = props.tasks;
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
                    </tr>
                    </thead>
                    <tbody>
                    {tasks.map(value =>
                        <tr key={value.id}>
                            <td>{value.title}</td>
                            <td>{value.deadline}</td>
                            <td>{value.status}</td>
                        </tr>
                    )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default TableInner
