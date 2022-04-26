import {AxiosResponse} from "axios";
import {ITask} from "../interfaces";
import {api} from "./api";

export default class TasksService {
    static async getTasks(): Promise<AxiosResponse<ITask[]>> {
        return api.get(
            `tasks/`,
            {headers: {"Authorization": `Bearer ${localStorage.getItem("JWT")}`}}
        );
    }

    static async createTask(title: string, description: string, deadline: string): Promise<AxiosResponse> {
        return api.post(
            "tasks/",
            {title: title, description: description, deadline: deadline},
            {headers: {"Authorization": `Bearer ${localStorage.getItem("JWT")}`}}
        );
    }
}
