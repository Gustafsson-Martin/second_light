import axios from "axios";
import SuperTokens from "supertokens-website";
import type {App} from "vue";

export default {
    install: (app: App<Element>) => {
        const storageServer = axios.create({
            baseURL: "http://localhost:5002/",
            timeout: 9000,
            withCredentials: true,
        });

        const loginServer = axios.create({
            baseURL: "http://localhost:5001/auth/",
            timeout: 8000,
        });

        SuperTokens.addAxiosInterceptors(loginServer);
        SuperTokens.addAxiosInterceptors(storageServer);

        SuperTokens.init({
            apiDomain: "http://localhost:5001",
            apiBasePath: "/auth",
        });

        app.provide("loginServer", loginServer);
        app.provide("storageServer", storageServer);
    },
};
