<script setup lang="ts">
import {computed, ref} from "vue";
import DeleteIcon from "vue-material-design-icons/Delete.vue";

const props = defineProps<{
    link: string;
    name: string;
}>();

const emit = defineEmits(["remove-bookmark"]);

const deleteVisible = ref<boolean>(false);

/* Fetch favicon from link and have that as icon for bookmark */
const iconUrl = computed(() => {
    return "http://www.google.com/s2/favicons?domain=" + props.link;
});

const deleteButtonStyle = computed(() => {
    if (deleteVisible.value) return {display: "block"};
    return {display: "none"};
});

const open = () => window.open(props.link, "_blank");
const remove = () => emit("remove-bookmark");
</script>

<template>
    <div @click="open" @mouseover="deleteVisible = true" @mouseleave="deleteVisible = false" :title="props.link">
        <img :src="iconUrl" />
        <p>{{ props.name }}</p>
        <button :style="deleteButtonStyle" @click.stop="remove">
            <DeleteIcon :size="20" />
        </button>
    </div>
</template>

<style scoped>
div {
    font-size: 1vw;
    padding: 1vw;
    cursor: pointer;
    display: flex;
    flex-wrap: wrap;
    align-content: center;
    justify-content: center;
    flex-direction: column;
}

div:hover {
    background-color: var(--color-grey-600);
}

img {
    width: 2.5vw;
    height: 2.5vw;
    left: 50%;
    transform: translateX(-50%);
}

button {
    position: absolute;
    top: 0;
    right: 0;
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
