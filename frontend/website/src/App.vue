<script setup lang="ts">
import BaseWidget from "./components/widgets/BaseWidget.vue";
import SideBarMenu from "./components/SideBarMenu.vue";
import type {AxiosInstance} from "axios";
import SuperTokens from "supertokens-website";
import {onMounted, ref, onBeforeMount} from "vue";
import AuthForm from "./components/auth/AuthForm.vue";
import {injectStrict} from "./helper";

const loggedin = ref(false);
const widgetids = ref<Array<string>>([]);
const username = ref<string>("");

const availableBackgroundImages = ref<Array<string>>([]);
const selectedBackgroundImages = ref<Array<string>>([]);
let backgroundImageIndex = 0;
let backgroundIntervalId = 0; /* setInterval id returned can never be 0 so: 0 => no interval active */

const storageServer: AxiosInstance = injectStrict("storageServer");
const loginServer: AxiosInstance = injectStrict("loginServer");

async function doesSessionExist() {
    if (!(await SuperTokens.attemptRefreshingSession())) return false;
    try {
        const response = await storageServer.get("/user");
        selectedBackgroundImages.value = response.data.background_images;
        widgetids.value = response.data.widgets;
        username.value = response.data.username;
        await reloadAvailableBackgroundImages();
        startBackgroundImageRotation();
    } catch (error) {
        console.log(error);
        return false;
    }
    return true;
}

async function reloadAvailableBackgroundImages() {
    const response = await storageServer.get("/user/available_background_images");
    availableBackgroundImages.value = response.data.items;
}

async function logout() {
    await SuperTokens.signOut();
    widgetids.value = [];
    document.body.style.backgroundImage = "none";
    clearInterval(backgroundIntervalId);
    loggedin.value = false;
}

function widgetCreated(id: string) {
    widgetids.value.push(id);
}

async function changeUsername(newUsername: string) {
    await storageServer.post("/user/username/set", {username: newUsername});
    username.value = newUsername;
}

function isThirdPartyRedirect() {
    return new URLSearchParams(window.location.search).get("thirdPartyId") !== null;
}

function applyBackgroundImages(selected: Set<string>) {
    selectedBackgroundImages.value = [...selected];
    backgroundImageIndex = 0;
    storageServer.post("/user/selected_backgrounds", {backgrounds: selectedBackgroundImages.value});
    startBackgroundImageRotation();
}

function startBackgroundImageRotation() {
    clearInterval(backgroundIntervalId);
    if (selectedBackgroundImages.value.length == 0) {
        document.body.style.backgroundImage = "none";
        return;
    }
    setAsBackground(selectedBackgroundImages.value[backgroundImageIndex]);
    if (selectedBackgroundImages.value.length == 1) return;
    backgroundIntervalId = window.setInterval(() => {
        backgroundImageIndex = (backgroundImageIndex + 1) % selectedBackgroundImages.value.length;
        setAsBackground(selectedBackgroundImages.value[backgroundImageIndex]);
    }, 10000);
}

/* 
Preload image to img tag and then wait some time before assigning to background,
this results in less flickering when swapping background images.
*/
async function setAsBackground(backgroundImageKey: string) {
    const response = await storageServer.get("user/background_image", {params: {key: backgroundImageKey}});
    const img = new Image(document.documentElement.clientWidth, document.documentElement.clientHeight);
    img.src = response.data.url;
    img.addEventListener("load", () => {
        window.setTimeout(() => {
            document.body.style.backgroundImage = `url(${img.src})`;
        }, 1000);
    });
}

async function authenticationCheck() {
    loggedin.value = await doesSessionExist();
}

onMounted(async () => {
    await authenticationCheck();
});

/* ThirdParty redirect handling */
onBeforeMount(async () => {
    if (isThirdPartyRedirect()) {
        const params = new URLSearchParams(window.location.search);
        const code = params.get("code");
        const thirdPartyId = params.get("thirdPartyId");
        const response = await loginServer.post("/signinup", {
            redirectURI: `${window.location.origin}/?thirdPartyId=${thirdPartyId}`,
            thirdPartyId: thirdPartyId,
            code: code,
        });
        if (response.data.createdNewUser) {
            await storageServer.post("/user/create", {username: "GreatUsername"});
        }
        window.location.replace(window.location.origin);
    }
});
</script>

<template>
    <AuthForm v-if="!loggedin" @authenticated="authenticationCheck" />
    <BaseWidget v-for="(id, index) in widgetids" :key="index" :id="id" />
    <SideBarMenu
        v-if="loggedin"
        :username="username"
        :availableBackgroundImages="availableBackgroundImages"
        :selectedBackgroundImages="selectedBackgroundImages"
        @logout="logout"
        @change-username="changeUsername"
        @apply-background-images="applyBackgroundImages"
        @file-uploaded="reloadAvailableBackgroundImages"
        @widget-created="widgetCreated"
    />
</template>

<style>
@import "./assets/base.css";
</style>
