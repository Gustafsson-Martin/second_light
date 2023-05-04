<script setup lang="ts">
import {computed} from "@vue/reactivity";
import {onMounted, ref, watch} from "vue";
import MenuIcon from "vue-material-design-icons/Menu.vue";
import PlusIcon from "vue-material-design-icons/Plus.vue";
import LogoutIcon from "vue-material-design-icons/Logout.vue";
import FolderAccountIcon from "vue-material-design-icons/FolderAccount.vue";
import ImageIcon from "vue-material-design-icons/Image.vue";
import AccountCircleIcon from "vue-material-design-icons/AccountCircle.vue";
import {widgetKeys} from "./widgets/widgets";
import type {AxiosInstance} from "axios";
import {injectStrict} from "@/helper";
import axios from "axios";

const props = defineProps<{
    username: string;
    availableBackgroundImages: Array<string>;
    selectedBackgroundImages: Array<string>;
}>();

const emit = defineEmits(["logout", "change-username", "apply-background-images", "file-uploaded", "widget-created"]);

const isExpanded = ref<boolean>(false);
const dropdowns = ref({
    addWidget: false,
    background: false,
    shared: false,
    profile: false,
});

const newUsername = ref<string>("");
const shareid = ref<string>("");
const imageFile = ref<File>();

const unsupportedFormatError = ref<boolean>();
const shareidError = ref<boolean>();

const backgroundImageUrls = ref<Array<string>>([]);
const selectedBackgroundImages = ref<Set<string>>(new Set(props.selectedBackgroundImages));

const storageServer: AxiosInstance = injectStrict("storageServer");

watch(
    () => props.availableBackgroundImages,
    () => fetchBackgroundImageUrls()
);

async function fetchBackgroundImageUrls() {
    for (let i = 0; i < props.availableBackgroundImages.length; i++) {
        fetchBackgroundImageUrl(i);
    }
}

async function fetchBackgroundImageUrl(index: number) {
    const response = await storageServer.get("user/background_image", {
        params: {key: props.availableBackgroundImages[index]},
    });
    backgroundImageUrls.value[index] = response.data.url;
}

function expand() {
    isExpanded.value = !isExpanded.value;
    if (!isExpanded.value) {
        for (let key in dropdowns.value) {
            dropdowns.value[key as keyof typeof dropdowns.value] = false;
        }
    }
}

function toggleDropdown(key: keyof typeof dropdowns.value) {
    dropdowns.value[key] = !dropdowns.value[key];
    isExpanded.value = true;
}

function changeUsername() {
    emit("change-username", newUsername.value);
    newUsername.value = "";
}

async function createWidget(type: string) {
    try {
        const response = await storageServer.post("/widget/create", {type: type});
        emit("widget-created", response.data.id);
    } catch (error) {
        console.log(error);
    }
}

async function createSharedWidget() {
    try {
        const response = await storageServer.post("/widget/create/shared", {widgetid: shareid.value});
        emit("widget-created", response.data.id);
    } catch (error) {
        shareidError.value = true;
    }
}

const buttonText = computed(() => {
    if (isExpanded.value) {
        return {
            username: props.username,
            collapse: "Collapse",
            addWidget: "Add widget",
            shared: "Shared",
            logout: "Logout",
            background: "Background",
        };
    }
    return {}; // No text when collapsed
});

const sideBarMenuWidth = computed(() => {
    if (isExpanded.value) return {width: "16vw"};
    return {width: "4vw"};
});

function clickImage(index: number) {
    const key = props.availableBackgroundImages[index];
    if (selectedBackgroundImages.value.has(key)) selectedBackgroundImages.value.delete(key);
    else selectedBackgroundImages.value.add(key);
}

const imageBorders = computed(() => {
    const borders = [];
    for (let i = 0; i < props.availableBackgroundImages.length; i++) {
        const key = props.availableBackgroundImages[i];
        if (selectedBackgroundImages.value.has(key)) borders[i] = "4px solid orange";
        else borders[i] = "none";
    }
    return borders;
});

async function uploadFile() {
    try {
        let response = await storageServer.get("user/background_image_upload_url");
        const url = response.data.url;
        response = await axios.put(url, imageFile.value);
        emit("file-uploaded");
    } catch (error) {
        console.log("File upload failed");
        console.log(error);
    }
}

function selectFile(event: Event) {
    unsupportedFormatError.value = false;
    const elem = event.target as HTMLInputElement;
    const files = elem.files;
    if (!files) return;
    const file = files[0];
    const validFormats = ["image/png", "image/jpeg"];
    if (!validFormats.includes(file.type)) {
        unsupportedFormatError.value = true;
        return;
    }
    imageFile.value = file;
}

const applyBackgroundImages = () => emit("apply-background-images", selectedBackgroundImages.value);

onMounted(() => {
    fetchBackgroundImageUrls();
});
</script>

<template>
    <div id="menu" :style="sideBarMenuWidth">
        <button @click="expand">
            <MenuIcon :size="32" />
            {{ buttonText.collapse }}
        </button>
        <button @click="toggleDropdown('profile')" title="Profile">
            <AccountCircleIcon :size="32" />
            {{ buttonText.username }}
        </button>
        <div v-if="dropdowns.profile" class="dropdown">
            <input v-model="newUsername" placeholder="new username" />
            <button @click="changeUsername">Change username</button>
        </div>
        <button @click="toggleDropdown('addWidget')" title="Add widget">
            <PlusIcon :size="32" />
            {{ buttonText.addWidget }}
        </button>
        <div v-if="dropdowns.addWidget" class="dropdown">
            <button v-for="widget in widgetKeys" :key="widget" @click="createWidget(widget)">
                <!-- <PlusIcon :size="20" /> -->
                {{ widget }}
            </button>
        </div>
        <button @click="toggleDropdown('shared')" title="Shared Widgets">
            <FolderAccountIcon :size="32" />
            {{ buttonText.shared }}
        </button>
        <div v-if="dropdowns.shared" class="dropdown">
            <p v-if="shareidError" :style="{color: 'red'}">Widget does not exist</p>
            <input v-model="shareid" placeholder="share id" @focus="shareidError = false" />
            <button @click="createSharedWidget">Create shared widget</button>
        </div>
        <button @click="toggleDropdown('background')" title="Backgrounds">
            <ImageIcon :size="32" />
            {{ buttonText.background }}
        </button>
        <div v-if="dropdowns.background" class="dropdown">
            <img
                v-for="(url, index) in backgroundImageUrls"
                :key="url"
                :src="url"
                @click="clickImage(index)"
                @error="fetchBackgroundImageUrl(index)"
                :style="{border: imageBorders[index]}"
            />
            <button @click="applyBackgroundImages">Apply</button>
            <p v-if="unsupportedFormatError" :style="{color: 'red'}">Unsupported File Format</p>
            <input id="fileInput" type="file" @change="selectFile" />
            <button @click="uploadFile">Upload File</button>
        </div>
        <button @click="emit('logout')" id="logout">
            {{ buttonText.logout }}
            <LogoutIcon :size="32" />
        </button>
    </div>
</template>

<style scoped>
#logout {
    color: red;
}
.dropdown {
    font-size: 1vw;
    background-color: var(--color-grey-800);
    display: flex;
    flex-wrap: wrap;
    align-content: center;
    justify-content: center;
}

img {
    width: 4vw;
    height: 4vw;
    margin: 0.5vw;
}

#menu {
    position: absolute;
    top: 0;
    right: 0;
    width: 4vw;
    height: 100%;
    font-size: 1.6vw;
    transition: width 0.25s;
    background-color: var(--color-grey-900);
    color: var(--color-accent-1);
    overflow-y: auto;
}

.dropdown button {
    width: 80%;
    background-color: var(--color-grey-700);
    margin: 0.5vh 0 0.5vh 0;
    border-radius: 10px;
}

.dropdown input {
    font-size: 1vw;
    width: 80%;
    background-color: var(--color-grey-700);
    color: white;
    margin: 0.5vh 0 0.5vh 0;
    outline: none;
    border: none;
    border-bottom: 0.2vh solid var(--color-grey-700);
}

.dropdown input:focus {
    border-bottom: 0.2vh solid var(--color-accent-1);
}

.dropdown button:hover {
    background-color: var(--color-grey-600);
}

button {
    position: relative;
    font-size: inherit;
    margin: 2vh 0 2vh 0;
    width: 100%;
    padding: 8px;
    background-color: inherit;
    outline: none;
    border: none;
    color: inherit;
    vertical-align: text-bottom;
    transition: width 2s;
    cursor: pointer;
    word-break: break-all;
}

button:hover {
    background-color: var(--color-grey-800);
}
</style>
