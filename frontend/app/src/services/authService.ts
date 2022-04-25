import {AxiosResponse} from "axios";
import {api} from "./api";

export default class AuthService {
    static async login(login: string, password: string): Promise<AxiosResponse<{ access_token: string }>> {
        return api.post(
            "auth/login",
            {login: login, password: password}
        ).then(response => {
            localStorage.setItem("JWT", response.data.access_token);
            return response
        });
    }

    static async registration(login: string, password: string): Promise<AxiosResponse<{}>> {
        return api.post(
            "auth/sign-up",
            {login: login, password: password},
        )
    }

    static async revoke(): Promise<AxiosResponse<{ access_token: string }>> {
        return api.post("auth/revoke").then(response => {
            localStorage.setItem("JWT", response.data.access_token);
            return response
        })
    }

    static async logout(): Promise<AxiosResponse<void>> {
        return api.post("auth/logout")
    }
}
