<script setup lang="ts">
import {computed, ref} from "vue";
import DeleteIcon from "vue-material-design-icons/Delete.vue";

const props = defineProps<{
    text: string;
    checked: boolean;
}>();

const emit = defineEmits(["input-changed", "remove-item"]);

const deleteVisible = ref<boolean>(false);

const deleteButtonStyle = computed(() => {
    if (deleteVisible.value) return {display: "block"};
    return {display: "none"};
});

const textStyle = computed(() => {
    if (props.checked) return {textDecoration: "line-through"};
    return {textDecoration: "none"};
});

var updateInput = (event: Event) => {
    if (!(event.target instanceof HTMLInputElement)) return;
    emit("input-changed", (event.target as HTMLInputElement).checked);
};

const remove = () => emit("remove-item");
</script>

<template>
    <label :style="textStyle" @mouseover="deleteVisible = true" @mouseleave="deleteVisible = false">
        <input type="checkbox" @change="updateInput" :checked="checked" />
        {{ props.text }}
        <button :style="deleteButtonStyle" @click.stop="remove">
            <DeleteIcon :size="20" />
        </button>
    </label>
</template>

<style scoped>
input {
    font-size: 20px;
    height: 20px;
    width: 20px;
    filter: invert(100%) hue-rotate(70deg) brightness(2.5);
    cursor: pointer;
}

label {
    padding-left: 10%;
    padding-right: 10%;
    cursor: pointer;
}

label:hover {
    background-color: var(--color-grey-600);
}

button {
    position: absolute;
    top: 0;
    left: 0;
    margin: 0;
    padding: 0;
    background-color: transparent;
    border: none;
    outline: none;
    color: white;
    cursor: pointer;
}

button:hover {
    color: red;
    background-color: var(--color-grey-400);
}
</style>
