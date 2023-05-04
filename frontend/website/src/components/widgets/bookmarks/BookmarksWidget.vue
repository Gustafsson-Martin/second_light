<script setup lang="ts">
import {computed, onMounted, ref, watch} from "vue";
import {WidgetSettings, WidgetSettingsOptions} from "../widgetSettings";
import BookmarkItem from "./BookmarkItem.vue";
import PlusIcon from "vue-material-design-icons/Plus.vue";

type Item = {link: string; name: string};

type Content = {
    bookmarks: Item[];
};

const emit = defineEmits(["save-content", "load-content", "define-settings-options", "define-initial-settings"]);

const props = defineProps<{
    content: Content;
    settings: WidgetSettings;
}>();

const invalidUrl = ref<boolean>(false);
const addBookmarkExpanded = ref<boolean>(false);
const addLink = ref<string>("");
const addName = ref<string>("");

const content = ref<Content>(props.content);
watch(
    () => props.content,
    (newContent: Content) => {
        content.value = newContent;
    }
);

const save = () => emit("save-content", content.value);

function settingsOptions() {
    const options = new WidgetSettingsOptions();
    options.setStyleOptions("justifyContent", ["flex-start", "center", "space-around"]);
    return options;
}

function initialSettings() {
    const settings = new WidgetSettings();
    settings.style["justifyContent"] = "flex-start";
    return settings;
}

const style = computed(() => {
    return props.settings.style;
});

function create() {
    if (!addLink.value.includes("://")) addLink.value = "https://" + addLink.value;
    try {
        new URL(addLink.value);
    } catch {
        invalidUrl.value = true;
        return;
    }
    if (content.value.bookmarks == undefined) content.value.bookmarks = [];
    content.value.bookmarks.push({link: addLink.value, name: addName.value});
    save();
    addBookmarkExpanded.value = false;
}

function expand() {
    addBookmarkExpanded.value = !addBookmarkExpanded.value;
}

function removeBookmark(index: number) {
    content.value.bookmarks.splice(index, 1);
    save();
}

onMounted(() => {
    emit("define-settings-options", settingsOptions());
    if (props.settings.isNotInitialized()) emit("define-initial-settings", initialSettings());
});
</script>

<template>
    <div id="content" :style="style">
        <BookmarkItem
            v-for="(item, i) in content.bookmarks"
            :key="i"
            :link="item.link"
            :name="item.name"
            @remove-bookmark="removeBookmark(i)"
        />
    </div>
    <button id="expandButton" @click="expand">
        <PlusIcon :size="32" />
    </button>
    <div id="AddBookmarkInput" v-if="addBookmarkExpanded">
        <span v-if="invalidUrl">Invalid url</span>
        <input type="text" v-model="addLink" placeholder="Bookmark url" @input="invalidUrl = false" />
        <input type="text" v-model="addName" placeholder="Bookmark name" />
        <button @click="create">Create</button>
    </div>
</template>

<style scoped>
#content {
    width: 100%;
    height: 95%;
    display: flex;
    flex-wrap: wrap;
    align-content: flex-start;
    justify-content: flex-start;
    margin-left: auto;
    overflow: hidden; /* To avoid problem with position of add button */
}

#AddBookmarkInput {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 60%;
    height: 60%;
    background-color: var(--color-grey-600);
    border-radius: 10px;
    display: flex;
    flex-wrap: wrap;
    align-content: center;
    justify-content: center;
    margin-left: auto;
}

input {
    width: 80%;
    height: 20%;
}

button {
    outline: none;
    border: none;
    cursor: pointer;
    font-size: 1.4vw;
    margin-top: 1vw;
}

#expandButton {
    position: absolute;
    bottom: 2%;
    right: 2%;
    border-radius: 100%;
    width: 48px;
    height: 48px;
    background-color: var(--color-accent-2);
    color: black;
    outline: none;
    border: none;
    cursor: pointer;
}

#expandButton:hover {
    background-color: var(--color-accent-2-dark);
}
</style>
