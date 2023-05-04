<script setup lang="ts">
import {computed, onMounted, ref, watch} from "vue";
import {WidgetSettings, WidgetSettingsOptions} from "../widgetSettings";

type Content = {
    text: string;
};

const emit = defineEmits(["save-content", "load-content", "define-settings-options", "define-initial-settings"]);

const props = defineProps<{
    content: Content;
    settings: WidgetSettings;
}>();

const isActive = ref<boolean>(false);
const content = ref<string>(props.content.text);
watch(
    () => props.content,
    (newContent: Content) => {
        if (!isActive.value) {
            content.value = newContent.text;
        }
    }
);

const save = () => emit("save-content", {text: content.value} as Content);
const focusOut = () => {
    isActive.value = false;
    save();
};

function input(event: Event) {
    if (!(event.target instanceof HTMLTextAreaElement)) return;
    content.value = event.target.value;
    save();
}

const style = computed(() => {
    return props.settings.style;
});

function settingsOptions() {
    const options = new WidgetSettingsOptions();
    options.setStyleOptions("fontSize", ["32px", "64px", "96px"]);
    options.setStyleOptions("fontFamily", ["Brush Script MT", "Arial", "Droid Sans"]);
    options.setStyleOptions("fontStyle", ["normal", "italic"]);
    options.setStyleOptions("color", ["white", "red", "green", "blue"]);
    options.setStyleOptions("letter-spacing", ["0px", "10px", "5px", "-10px"]);
    options.setStyleOptions("text-shadow", ["none", "2px 2px red"]);
    return options;
}

function initialSettings() {
    const settings = new WidgetSettings();
    settings.style["fontSize"] = "32px";
    settings.style["fontFamily"] = "Arial";
    settings.style["fontStyle"] = "normal";
    settings.style["color"] = "white";
    settings.style["letter-spacing"] = "0px";
    settings.style["text-shadow"] = "none";
    return settings;
}

onMounted(() => {
    window.setInterval(() => {
        emit("load-content");
    }, 500);
    emit("define-settings-options", settingsOptions());
    if (props.settings.isNotInitialized()) emit("define-initial-settings", initialSettings());
});
</script>

<template>
    <textarea :style="style" @focusin="isActive = true" @focusout="focusOut" :value="content" @input="input"></textarea>
</template>

<style scoped>
textarea {
    width: 100%;
    height: 95%;
    resize: none;
    color: inherit;
    background-color: inherit;
    outline: none;
    border: none;
    font-size: 24px;
}
</style>
