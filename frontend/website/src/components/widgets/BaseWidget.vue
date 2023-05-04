<script setup lang="ts">
import {computed, onMounted, ref} from "vue";
import type {AxiosInstance} from "axios";
import CogOutlineIcon from "vue-material-design-icons/CogOutline.vue";
import ShareIcon from "vue-material-design-icons/Share.vue";
import {WidgetSettings, WidgetSettingsOptions} from "./widgetSettings";
import {injectStrict} from "@/helper";
import {widgetKeys, widgetTypes} from "./widgets";

const props = defineProps<{
    id: string;
}>();

const type = ref<keyof typeof widgetTypes>(widgetKeys[0]);
const container = ref<HTMLDivElement>();

const widgetContainer = ref<HTMLDivElement>();
const widgetContent = ref<unknown>({});
const widgetSettings = ref<WidgetSettings>(new WidgetSettings());
const widgetSettingsOptions = ref<WidgetSettingsOptions>(new WidgetSettingsOptions());

const showSettings = ref<boolean>(false);
const settingsColor = computed(() => (showSettings.value ? "red" : "white"));
const isLoaded = ref<boolean>(false);
const showShareId = ref<boolean>(false);
const shareColor = computed(() => (showShareId.value ? "green" : "white"));

const storageServer: AxiosInstance = injectStrict("storageServer");

function widgetData() {
    if (container.value?.style == null || widgetContainer.value?.style == null) return;
    return {
        id: props.id,
        left: parseFloat(container.value.style.left),
        top: parseFloat(container.value.style.top),
        width: parseFloat(widgetContainer.value.style.width),
        height: parseFloat(widgetContainer.value.style.height),
        settings: widgetSettings.value,
        content: widgetContent.value,
    };
}

async function loadContent() {
    try {
        const response = await storageServer.get("/widget/", {params: {id: props.id}});
        widgetContent.value = response.data.content;
    } catch (error) {
        console.log(error);
    }
}

async function save(value: unknown = widgetContent.value) {
    widgetContent.value = value;
    try {
        await storageServer.post("/widget/update", widgetData());
    } catch (error) {
        console.log(error);
    }
}

async function load() {
    if (container.value?.style == null || widgetContainer.value?.style == null) return;
    try {
        const response = await storageServer.get("/widget", {params: {id: props.id}});
        container.value.style.left = response.data.left + "px";
        container.value.style.top = response.data.top + "px";
        widgetContainer.value.style.width = response.data.width + "px";
        widgetContainer.value.style.height = response.data.height + "px";
        widgetContent.value = response.data.content;
        widgetSettings.value = new WidgetSettings(response.data.settings);
        type.value = response.data.type;
        isLoaded.value = true;
    } catch (error) {
        console.log(error);
    }
}

function drag(event: MouseEvent) {
    window.addEventListener("mousemove", mousemove);
    window.addEventListener("mouseup", mouseup);
    const prev = {x: event.clientX, y: event.clientY};

    function mousemove(event: MouseEvent) {
        if (container.value?.style == null) return;
        const rect = container.value.getBoundingClientRect();
        container.value.style.left = rect.left + event.clientX - prev.x + "px";
        container.value.style.top = rect.top + event.clientY - prev.y + "px";
        prev.x = event.clientX;
        prev.y = event.clientY;
    }

    function mouseup() {
        window.removeEventListener("mousemove", mousemove);
        window.removeEventListener("mouseup", mouseup);
        save();
    }
}

const toggleSettings = () => (showSettings.value = !showSettings.value);
const toggleShare = () => (showShareId.value = !showShareId.value);

function options(obj: WidgetSettingsOptions) {
    widgetSettingsOptions.value = obj;
}

function initSettings(obj: WidgetSettings) {
    widgetSettings.value = obj;
}

onMounted(() => {
    load();
});
</script>

<template>
    <div id="container" ref="container">
        <span id="top-banner" @mousedown.self="drag">
            <button @click="toggleSettings" title="Settings">
                <CogOutlineIcon :fillColor="settingsColor" />
            </button>
            <button @click="toggleShare" title="Share">
                <ShareIcon :fillColor="shareColor" />
            </button>
        </span>
        <div id="widget-container" ref="widgetContainer">
            <component
                v-if="isLoaded"
                :is="widgetTypes[type]"
                :content="widgetContent"
                :settings="widgetSettings"
                @save-content="save"
                @load-content="loadContent"
                @define-settings-options="options"
                @define-initial-settings="initSettings"
            ></component>
        </div>
        <div id="settings" v-if="showSettings">
            <h3 v-if="Object.keys(widgetSettingsOptions.config).length !== 0">Config</h3>
            <label v-for="(values, key) in widgetSettingsOptions.config" :key="key">
                {{ key }}:
                <select v-model="widgetSettings.config[key]">
                    <option v-for="obj in values" :key="obj.value" :value="obj.value">{{ obj.text }}</option>
                </select>
            </label>
            <h3 v-if="Object.keys(widgetSettingsOptions.style).length !== 0">Style</h3>
            <label v-for="(values, key) in widgetSettingsOptions.style" :key="key">
                {{ key }}:
                <select v-model="widgetSettings.style[key]">
                    <option v-for="obj in values" :key="obj.value" :value="obj.value">{{ obj.text }}</option>
                </select>
            </label>
        </div>
        <div id="shareid" v-if="showShareId">
            Share:
            <input :value="props.id" disabled />
        </div>
    </div>
</template>

<style scoped>
label {
    display: block;
    width: 100%;
}

button {
    color: inherit;
    background-color: inherit;
    border: none;
    outline: none;
    cursor: pointer;
    padding: 0;
    margin: 0;
}

#settings {
    position: absolute;
    left: -310px;
    top: 0;
    width: 300px;
    height: 100%;
    resize: none;
    z-index: 1;
    background-color: var(--color-grey-600);
    overflow: auto;
}

#shareid {
    position: absolute;
    left: 0;
    top: -42px;
    width: 100%;
    height: 36px;
    resize: none;
    z-index: 1;
    background-color: var(--color-grey-600);
    overflow: hidden;
    display: flex;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    font-size: 32px;
    padding: 2px;
}

input {
    resize: none;
    overflow-y: scroll;
    overflow-x: scroll;
    height: 32px;
    width: 60%;
}

ul {
    list-style: none;
    padding-left: 1em;
}

#widget-container {
    resize: both;
    overflow: auto;
    margin: 24px 0px 0px 0px;
    padding: 0;
}

#top-banner {
    position: absolute;
    top: 0;
    left: 0;
    height: 24px;
    width: 100%;
    cursor: move;
    background-color: var(--color-grey-800);
}

#container {
    position: absolute;
    margin: 0;
    font-size: 24px;
    color: var(--color-grey-100);
    background-color: var(--color-grey-700);
    border: none;
}
</style>
