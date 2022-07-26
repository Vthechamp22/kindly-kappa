<script setup lang="ts">
import { ref, watch } from "vue";

const emit = defineEmits(["join"]);

const code = ref("");
const username = ref("");
const difficulty = ref(1);
const theme = ref("onedarkpro");
let connecting = false;

const errors = ref({
    code: "",
    username: "",
});

const loading = ref(false);

watch(theme, (newTheme) => {
    document
        .querySelector("body")
        .setAttribute("data-theme", newTheme.toLowerCase());
});

watch(difficulty, (newDiff) => {
    console.log(newDiff);
});

const hackyObject = {
    switchToRoom: function () {
        emit("join", { code: code.value, username: username.value });
    },
    reportMissingRoom: function () {
        connecting = false;
        alert("That room doesn't exist :/");
    },
    reportConnectionError: function () {
        connecting = false;
        alert("Well shit, if your reading this then somethings gone wrong.\nit genuinely is a bug, not a feature")
    },
    reportWSClose: function () {
        connecting = false;
    }
}

function joinRoom() {
    if (
        !code.value ||
        code.value.length != 4 ||
        !/^[a-zA-Z]+$/.test(code.value)
    ) {
        errors.value.code = "Please enter a valid code!";
    } else {
        errors.value.code = "";
    }

    if (!username.value) {
        errors.value.username = "Please enter a username!";
    } else {
        errors.value.username = "";
    }

    if (errors.value.code || errors.value.username) {
        return;
    }

    if (!connecting) {
        connecting = true;
        connect(username, code.value, undefined, hackyObject);
    }
}

function createRoom() {
    if (!username.value) {
        errors.value.username = "Please enter a username!";
    } else {
        errors.value.username = "";
    }

    if (errors.value.username) {
        return;
    }

    if (!connecting) {
        connecting = true;
        connect(username, undefined, difficulty, hackyObject);
    }
}
</script>

<template>
    <div id="main">
        <div id="login">
            <form id="theme-form" class="m-3">
                <select class="select select-primary w-full max-w-xs" v-model="theme">
                    <option selected value="onedarkpro">One Dark Pro</option>
                    <option>Night</option>
                    <option>Dark</option>
                    <option>Emerald</option>
                    <option>Forest</option>
                    <option>Dracula</option>
                    <option>Lemonade</option>
                    <option>Winter</option>
                </select>
            </form>
            <div class="tooltip"
                data-tip="japan PNG Designed By tsuki from https://pngtree.com/freepng/cute-kappa-in-japanese-mythology-cartoon-style_6544405.html?sol=downref&id=bef">
                <img class="mx-auto" src="imgs/kappa-left.png" alt="kappa1" />
            </div>
            <div class="text-center h-full flex justify-center flex-col">
                <h2>Kindly Kappas</h2>
                <form @submit.prevent="joinRoom">
                    <input type="text" placeholder="Room code" class="input input-bordered border-primary w-full"
                        v-model="code" />
                    <label class="label">
                        <span class="label-text-alt text-error font-bold">{{
                                errors.code
                        }}</span>
                    </label>
                    <input type="text" placeholder="Username" class="input input-bordered border-primary w-full"
                        v-model="username" />
                    <label class="label">
                        <span class="label-text-alt text-error font-bold">{{
                                errors.username
                        }}</span>
                    </label>
                    <button type="submit" class="btn btn-primary mt-4">
                        <i v-if="loading" class="gg-spinner"></i>
                        <span v-else>Join Room</span>
                    </button>
                    <label for="create-room-modal" class="btn modal-button flex w-1/4 mx-auto my-2">Create Room</label>
                </form>
            </div>
            <div class="tooltip"
                data-tip="cute PNG Designed By Reiko from https://pngtree.com/freepng/japanese-kappa-monster-cartoon_6544406.html?sol=downref&id=bef">
                <img class="mx-auto" src="imgs/kappa-right.png" alt="kappa2" />
            </div>
        </div>

        <!-- Modal box -->
        <input type="checkbox" id="create-room-modal" class="modal-toggle" />
        <label for="create-room-modal" class="modal cursor-pointer">
            <label class="modal-box relative" for="">
                <label for="create-room-modal" class="btn btn-sm btn-circle absolute right-2 top-2">
                    <i class="gg-close-o" style="--ggs: 1.2"></i>
                </label>
                <h3 class="text-lg font-bold my-4">
                    Choose Difficulty: {{ difficulty }}
                </h3>
                <input type="range" min="1" max="5" class="range w-full" step="1" v-model="difficulty" />
                <div class="w-full flex justify-between text-xs px-2">
                    <span>|</span>
                    <span>|</span>
                    <span>|</span>
                    <span>|</span>
                    <span>|</span>
                </div>
                <button @click="createRoom()" class="btn my-4">Create</button>
            </label>
        </label>
    </div>
</template>

<style scoped>
#main {
    height: 100%;
    border: 3px solid hsl(var(--bc));
}

#login {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    height: 100%;
    justify-items: center;
    align-items: center;
}

form#theme-form {
    width: 10em;
    position: absolute;
    top: 0;
    right: 0;
}

img {
    max-width: 50%;
    max-height: 50%;
    width: auto;
    height: auto;
}

h2 {
    font-size: 64px;
    color: hsl(var(--bc));
    margin: 12px;
    margin-bottom: 8rem;
}
</style>
