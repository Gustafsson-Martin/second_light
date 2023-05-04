<script setup lang="ts">
import type {AxiosInstance} from "axios";
import {computed, ref} from "vue";
import AccountPlusIcon from "vue-material-design-icons/AccountPlus.vue";
import {signupFormData} from "./dataFormats";
import SuperTokens from "supertokens-website";
import {injectStrict} from "@/helper";

enum Error {
    NONE,
    EMAIL_INVALID,
    EMAIL_ALREADY_EXISTS,
    USERNAME_INVALID,
    PASSWORD_INVALID,
    CONFIRM_PASSWORD_INVALID,
    MISMATCHED_PASSWORDS,
    USERNAME_TAKEN,
}

const emit = defineEmits(["authenticated"]);

const loginServer: AxiosInstance = injectStrict("loginServer");
const storageServer: AxiosInstance = injectStrict("storageServer");

const email = ref<string>("");
const username = ref<string>("");
const password = ref<string>("");
const confirmPassword = ref<string>("");
const error = ref<Error>(Error.NONE);

const signupData = () => signupFormData(email.value, password.value);

function isValidEmail() {
    return email.value.includes("@");
}

function isValidPassword() {
    return password.value.length >= 8 && /\d/.test(password.value);
}

function isValidForm() {
    if (confirmPassword.value == "") error.value = Error.CONFIRM_PASSWORD_INVALID;
    if (!isValidPassword()) error.value = Error.PASSWORD_INVALID;
    if (username.value == "") error.value = Error.USERNAME_INVALID;
    if (!isValidEmail()) error.value = Error.EMAIL_INVALID;
    if (password.value != confirmPassword.value) error.value = Error.MISMATCHED_PASSWORDS;
    return error.value == Error.NONE;
}

async function signup() {
    if (!isValidForm()) return;
    let response = await loginServer.post("/signup", signupData());
    if (response.data.status == "FIELD_ERROR") {
        response.data.formFields.forEach((field: Record<string, string>) => {
            if (field.id == "email") error.value = Error.EMAIL_INVALID;
            if (field.id == "password") error.value = Error.PASSWORD_INVALID;
        });
        return;
    }
    if (response.data.status == "EMAIL_ALREADY_EXISTS_ERROR") {
        error.value = Error.EMAIL_ALREADY_EXISTS;
        return;
    }
    console.log(response);
    if (!(await SuperTokens.doesSessionExist())) return;
    response = await storageServer.post("/user/create", {username: username.value});
    console.log(response);
    emit("authenticated");
}

const style = computed(() => {
    const style = {
        email: {},
        username: {},
        password: {},
        confirmPassword: {},
    };
    if (error.value == Error.EMAIL_INVALID || error.value == Error.EMAIL_ALREADY_EXISTS)
        style.email = {"border-bottom": "0.5vh solid red"};
    if (error.value == Error.USERNAME_INVALID) style.username = {"border-bottom": "0.5vh solid red"};
    if (error.value == Error.PASSWORD_INVALID) style.password = {"border-bottom": "0.5vh solid red"};
    if (error.value == Error.CONFIRM_PASSWORD_INVALID) style.confirmPassword = {"border-bottom": "0.5vh solid red"};
    if (error.value == Error.USERNAME_TAKEN) style.username = {"border-bottom": "0.5vh solid red"};
    if (error.value == Error.MISMATCHED_PASSWORDS) {
        style.password = {"border-bottom": "0.5vh solid red"};
        style.confirmPassword = {"border-bottom": "0.5vh solid red"};
    }
    return style;
});

const errorTextVisible = computed(() => {
    if (error.value == Error.NONE) return {display: "none"};
    return {display: "block"};
});

const errorText = computed(() => {
    if (error.value == Error.EMAIL_INVALID) return "Email is not valid";
    if (error.value == Error.EMAIL_ALREADY_EXISTS) return "Email already exists";
    if (error.value == Error.USERNAME_INVALID) return "Username required";
    if (error.value == Error.PASSWORD_INVALID) return "Password must contain at least 8 characters, including a number";
    if (error.value == Error.CONFIRM_PASSWORD_INVALID) return "Confirm password required";
    if (error.value == Error.MISMATCHED_PASSWORDS) return "Passwords do not match";
    if (error.value == Error.USERNAME_TAKEN) return "Username taken";
    return "";
});
</script>

<template>
    <h3 :style="errorTextVisible">{{ errorText }}</h3>
    <div>
        <input :style="style.email" v-model="email" placeholder="Email" type="email" @input="error = Error.NONE" />
        <label>Email</label>
    </div>
    <div>
        <input
            :style="style.username"
            v-model="username"
            placeholder="Username"
            type="text"
            @input="error = Error.NONE"
        />
        <label>Username</label>
    </div>
    <div>
        <input
            :style="style.password"
            v-model="password"
            placeholder="Password"
            type="password"
            @input="error = Error.NONE"
        />
        <label>Password</label>
    </div>
    <div>
        <input
            :style="style.confirmPassword"
            v-model="confirmPassword"
            placeholder="Confirm Password"
            type="password"
            @input="error = Error.NONE"
        />
        <label>Confirm Password</label>
    </div>
    <div>
        <button @click="signup">Sign up <AccountPlusIcon size="3vh" /></button>
    </div>
</template>

<style scoped>
@import "../../assets/form.css";
div {
    font-size: 3vh;
    width: 100%;
    height: 13vh;
    padding: 0;
    margin: 0;
}

label {
    bottom: calc(3vh + 4vh + 1vh); /* div: font-size + input padding + label: font-size/2 */
}
</style>
