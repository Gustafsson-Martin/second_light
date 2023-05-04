import {inject} from "vue";

export function injectStrict<T>(key: string) {
    const resolved = inject<T>(key);
    if (!resolved) throw new Error(`Could not resolve inject ${key}`);
    return resolved;
}
