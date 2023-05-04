<script setup lang="ts">
import LoginIcon from "vue-material-design-icons/Login.vue";
import type {AxiosInstance} from "axios";
import {computed, ref} from "vue";
import {signupFormData} from "./dataFormats";
import {injectStrict} from "@/helper";

const STATUS_WRONG_CREDENTIALS = "WRONG_CREDENTIALS_ERROR";
const STATUS_FIELD_ERROR = "FIELD_ERROR";

const emit = defineEmits(["authenticated"]);

const loginServer: AxiosInstance = injectStrict("loginServer");

const email = ref<string>("");
const password = ref<string>("");
const error = ref<boolean>(false);

const signinData = () => signupFormData(email.value, password.value);

async function signin() {
    let response = await loginServer.post("/signin", signinData());
    const status = response.data.status;
    if (status == STATUS_WRONG_CREDENTIALS || status == STATUS_FIELD_ERROR) {
        error.value = true;
        return;
    }
    console.log(response);
    emit("authenticated");
}

const inputStyle = computed(() => {
    if (error.value) return {"border-bottom": "0.5vh solid red"};
    return {};
});

const errorTextVisible = computed(() => {
    if (!error.value) return {display: "none"};
    return {display: "block"};
});

async function thirdPartySignin(thirdPartyId: string) {
    const response = await loginServer.get(`/authorisationurl?thirdPartyId=${thirdPartyId}`);
    const urlObj = new URL(response.data.url);
    urlObj.searchParams.append("redirect_uri", `${window.location.origin}/?thirdPartyId=${thirdPartyId}`);
    const url = urlObj.toString();
    window.location.replace(url);
}
</script>

<template>
    <h3 :style="errorTextVisible">Invalid credentials</h3>
    <div id="thirdParty">
        <button class="thirdPartyButton" id="google" @click="thirdPartySignin('google')">Google</button>
        <button class="thirdPartyButton" id="github" @click="thirdPartySignin('github')">GitHub</button>
    </div>
    <div>
        <input v-model="email" :style="inputStyle" placeholder="Email" type="email" @input="error = false" />
        <label>Email</label>
    </div>
    <div>
        <input v-model="password" :style="inputStyle" placeholder="Password" type="password" @input="error = false" />
        <label>Password</label>
    </div>
    <div>
        <button @click="signin">Sign in <LoginIcon size="4vh" /></button>
    </div>
</template>

<style scoped>
@import "../../assets/form.css";
#thirdParty {
    font-size: 2vh;
    display: flex;
    flex-wrap: wrap;
    align-content: flex-end;
    justify-content: center;
    height: 8vh;
}

.thirdPartyButton {
    position: relative;
    font-size: inherit;
    top: 0;
    transform: none;
    width: 10vw;
    height: 4vh;
    border-radius: 100px;
    padding: 0;
    color: white;
    outline: none;
    border: none;
    box-shadow: 0 1.2vh var(--color-grey-800);
    cursor: pointer;
    margin-left: 1vw;
    margin-right: 1vw;
}

#google {
    background-color: #0059ff;
}

#google:hover {
    background-color: #0400ff;
}

#github {
    background-color: var(--color-dark-grey);
}

#github:hover {
    background-color: var(--color-grey-900);
}

.thirdPartyButton:active {
    transform: translateY(5%);
    box-shadow: 0 0.6vh var(--color-grey-900);
}

div {
    font-size: 4vh;
    width: 100%;
    height: 14vh;
    padding: 0;
    margin: 0;
}

label {
    bottom: calc(4vh + 4vh + 1vh); /* div: font-size + input padding + label: font-size/2 */
}
</style>
