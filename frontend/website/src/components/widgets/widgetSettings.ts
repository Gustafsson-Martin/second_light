type Option = {
    value: string;
    text: string;
};

export class WidgetSettings {
    config: Record<string, string>;
    style: Record<string, string>;

    constructor(object?: Record<string, Record<string, string>>) {
        if (!object || Object.keys(object).length == 0) {
            this.config = {};
            this.style = {};
        } else {
            this.config = object.config;
            this.style = object.style;
        }
    }

    isNotInitialized() {
        return Object.keys(this.config).length == 0 && Object.keys(this.style).length == 0;
    }
}

export class WidgetSettingsOptions {
    config: Record<string, Option[]>;
    style: Record<string, Option[]>;

    constructor() {
        this.config = {};
        this.style = {};
    }

    setStyleOptions(key: string, values: string[], texts?: string[]) {
        if (!texts) texts = values;
        if (values.length != texts.length) throw new Error("values and texts need to be the same length");
        const options: Option[] = [];
        for (let i = 0; i < values.length; i++) {
            options.push({value: values[i], text: texts[i]});
        }
        this.style[key] = options;
    }

    setConfigOptions(key: string, values: string[], texts?: string[]) {
        if (!texts) texts = values;
        if (values.length != texts.length) throw new Error("values and texts need to be the same length");
        const options: Option[] = [];
        for (let i = 0; i < values.length; i++) {
            options.push({value: values[i], text: texts[i]});
        }
        this.config[key] = options;
    }
}
