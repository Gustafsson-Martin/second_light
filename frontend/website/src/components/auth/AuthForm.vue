<script setup lang="ts">
import {ref} from "vue";
import SigninForm from "./SigninForm.vue";
import SignupForm from "./SignupForm.vue";

const emit = defineEmits(["authenticated"]);

const tabs = {SigninForm, SignupForm};
const tab = ref<keyof typeof tabs>("SigninForm");
</script>

<template>
    <div id="background">
        <div id="container">
            <span>Second Light</span>
            <div id="tabs">
                <button :class="{active: tab == 'SigninForm'}" @click="tab = 'SigninForm'">Signin</button>
                <button :class="{active: tab == 'SignupForm'}" @click="tab = 'SignupForm'">Signup</button>
            </div>
            <KeepAlive>
                <component :is="tabs[tab]" @authenticated="emit('authenticated')"></component>
            </KeepAlive>
        </div>
    </div>
</template>

<style scoped>
#background {
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-wrap: wrap;
    align-content: center;
    justify-content: center;
    background-color: transparent;
}

#background:before {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: -1;
    filter: blur(5px);
    background-size: 100% 100%;
    background-image: url(../../../public/background.jpg);
}

div {
    font-size: 4vh;
    font-family: inherit;
    color: var(--color-grey-200);
    background-color: var(--color-grey-700);
    align-content: center;
    text-align: center;
    border-radius: 10px;
}

span {
    font-size: 7vh;
    font-family: "Brush Script MT";
    padding: 2vh;
    display: block;
}

#container {
    width: 60vw;
    filter: none;
}

button {
    font-size: inherit;
    color: var(--color-grey-200);
    background-color: var(--color-grey-600);
    border: none;
    width: 16vw;
    padding: 2vh 1vw 2vh 1vw;
    border-bottom: 1vh solid var(--color-grey-600);
    cursor: pointer;
}

.active {
    color: var(--color-accent-1);
    border-bottom: 1vh solid var(--color-accent-1) !important;
}

button:hover {
    background-color: var(--color-grey-500);
    border-bottom: 1vh solid var(--color-grey-500);
}
</style>
