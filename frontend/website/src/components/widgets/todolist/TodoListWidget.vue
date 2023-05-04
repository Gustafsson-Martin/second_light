<script setup lang="ts">
import TodoListItem from "./TodoListItem.vue";
import {computed, onMounted, ref, watch} from "vue";
import PlusIcon from "vue-material-design-icons/Plus.vue";
import {WidgetSettings, WidgetSettingsOptions} from "../widgetSettings";

type Item = {content: string; checked: boolean};

type Content = {
    todolist: Item[];
};

const props = defineProps<{
    content: Content;
    settings: WidgetSettings;
}>();
const emit = defineEmits(["save-content", "load-content", "define-settings-options", "define-initial-settings"]);

const content = ref<Content>(props.content);
const addTodolistExpanded = ref<boolean>(false);
const expand = () => (addTodolistExpanded.value = !addTodolistExpanded.value);

const todoListItem = ref<string>("");

watch(
    () => props.content,
    (newContent: Content) => {
        // TODO: Do some kind of check to not overwrite unsaved changes.
        content.value = newContent;
    }
);

const save = () => emit("save-content", content.value);

function create() {
    if (content.value.todolist == undefined) content.value.todolist = [];
    content.value.todolist.push({
        content: todoListItem.value,
        checked: false,
    });
    addTodolistExpanded.value = false;
    todoListItem.value = "";
    save();
}

function removeItem(index: number) {
    content.value.todolist.splice(index, 1);
    save();
}

function inputChanged(index: number, value: boolean) {
    content.value.todolist[index].checked = value;
    save();
}

function settingsOptions() {
    const options = new WidgetSettingsOptions();
    options.setStyleOptions("fontSize", ["20px", "26px", "32px"]);
    return options;
}

function initialSettings() {
    const settings = new WidgetSettings();
    settings.style["fontSize"] = "26px";
    return settings;
}

const style = computed(() => {
    return props.settings.style;
});

onMounted(() => {
    window.setInterval(() => {
        emit("load-content");
    }, 500);
    emit("define-settings-options", settingsOptions());
    if (props.settings.isNotInitialized()) emit("define-initial-settings", initialSettings());
});
</script>

<template>
    <div class="content" :style="style">
        <TodoListItem
            v-for="(item, i) in content.todolist"
            :key="i"
            :text="content.todolist[i].content"
            :checked="item.checked"
            @input-changed="(value: boolean) => inputChanged(i, value)"
            @remove-item="removeItem(i)"
        />
    </div>
    <button id="expandButton" @click="expand">
        <PlusIcon :size="32" />
    </button>
    <div id="AddTodolistInput" v-if="addTodolistExpanded">
        <input type="text" v-model="todoListItem" placeholder="Item" />
        <button @click="create">Create</button>
    </div>
</template>

<style scoped>
.content {
    width: 100%;
    height: 95%;
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: space-evenly;
    overflow: hidden; /* To avoid problem with position of add button */
}

#AddTodolistInput {
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
</style>
