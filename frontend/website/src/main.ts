import {createApp} from "vue";
import App from "./App.vue";
import ServerConnectionPlugin from "./plugins/serverConnection";

const app = createApp(App);
app.use(ServerConnectionPlugin);
app.mount("#app");
