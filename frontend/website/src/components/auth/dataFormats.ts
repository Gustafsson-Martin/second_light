export function signupFormData(email: string, password: string) {
    return {
        formFields: [
            {
                id: "email",
                value: email,
            },
            {
                id: "password",
                value: password,
            },
        ],
    };
}
