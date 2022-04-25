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
}
