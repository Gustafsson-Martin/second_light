<script setup lang="ts">
import {onMounted, ref, computed} from "vue";
import {WidgetSettings, WidgetSettingsOptions} from "../widgetSettings";

const emit = defineEmits(["save-content", "load-content", "define-settings-options", "define-initial-settings"]);

const props = defineProps<{
    content: unknown;
    settings: WidgetSettings;
}>();

const time = ref<string>("");

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
        time.value = new Date().toTimeString().split(" ")[0];
    }, 200);
    emit("define-settings-options", settingsOptions());
    if (props.settings.isNotInitialized()) emit("define-initial-settings", initialSettings());
});
</script>

<template>
    <span :style="style">{{ time }}</span>
</template>

<style scoped>
span {
    width: 100%;
    height: 100%;
    font-size: 64px;
    font-family: "Brush Script MT";
    overflow: hidden;
    display: flex;
    flex-wrap: wrap;
    align-content: center;
    justify-content: center;
}
</style>
