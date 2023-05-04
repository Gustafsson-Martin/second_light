<script setup lang="ts">
import {computed, onMounted, ref} from "vue";
import {WidgetSettings, WidgetSettingsOptions} from "../widgetSettings";

const emit = defineEmits(["save-content", "load-content", "define-settings-options", "define-initial-settings"]);

const props = defineProps<{
    content: unknown;
    settings: WidgetSettings;
}>();

const query = ref<string>("");

const style = computed(() => {
    return props.settings.style;
});

const config = computed(() => {
    return props.settings.config;
});

function search() {
    window.open(config.value["SearchEngine"] + query.value, "_blank");
}

function settingsOptions() {
    const options = new WidgetSettingsOptions();
    options.setStyleOptions("fontSize", ["24px", "32px", "48px"]);
    options.setConfigOptions(
        "SearchEngine",
        ["https://google.com/search?q=", "https://duckduckgo.com/?q=", "https://www.bing.com/search?q="],
        ["Google", "DuckDuckGo", "Bing"]
    );
    return options;
}

function initialSettings() {
    const settings = new WidgetSettings();
    settings.style["fontSize"] = "32px";
    settings.config["SearchEngine"] = "https://google.com/search?q=";
    return settings;
}

onMounted(() => {
    emit("define-settings-options", settingsOptions());
    if (props.settings.isNotInitialized()) emit("define-initial-settings", initialSettings());
});
</script>

<template>
    <input :style="style" type="text" v-model="query" placeholder="Seach query" @keyup.enter="search" />
</template>

<style scoped>
input {
    font-size: 32px;
    width: 100%;
    height: 100%;
    background-color: inherit;
    color: inherit;
    outline: none;
    border: none;
}
</style>
