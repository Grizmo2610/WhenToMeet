window.addEventListener("DOMContentLoaded", () => {
    switchTab(loginTab, signupTab, loginForm, signupForm, toSignup, toLogin);
});

const loginTab = document.getElementById("loginTab");
const signupTab = document.getElementById("signupTab");
const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const switchToSignup = document.getElementById("switchToSignup");
const switchToLogin = document.getElementById("switchToLogin");
const toLogin = document.getElementById("toLoginLink");
const toSignup = document.getElementById("toSignupLink");

function switchTab(activeTab, inactiveTab, showForm, hideForm, showSwitch, hideSwitch) {
    showForm.classList.remove("hidden");
    hideForm.classList.add("hidden");

    showSwitch.classList.remove("hidden");
    hideSwitch.classList.add("hidden");

    activeTab.classList.add("text-indigo-600", "border-indigo-600");
    activeTab.classList.remove("text-gray-500");

    inactiveTab.classList.add("text-gray-500");
    inactiveTab.classList.remove("text-indigo-600", "border-indigo-600");
}

loginTab.addEventListener("click", () => {
    switchTab(loginTab, signupTab, loginForm, signupForm, toSignup, toLogin);
});

signupTab.addEventListener("click", () => {
    switchTab(signupTab, loginTab, signupForm, loginForm, toLogin, toSignup);
});

switchToSignup.addEventListener("click", (e) => {
    e.preventDefault();
    switchTab(signupTab, loginTab, signupForm, loginForm, toLogin, toSignup);
});

switchToLogin.addEventListener("click", (e) => {
    e.preventDefault();
    switchTab(loginTab, signupTab, loginForm, signupForm, toSignup, toLogin);
});


async function request_api(endpoint, formData) {
    try {
        const res = await fetch(endpoint, {
            method: "POST",
            body: formData
        });
        return await res.json();
    } catch (err) {
        console.error("Error during request:", err);
        return { status: 409, message: "Error: " + err };
    }
}

function getFormData(fields) {
    const formData = new FormData();
    for (const [key, id] of Object.entries(fields)) {
        const value = document.getElementById(id).value.trim();
        if (!value) {
            alert("Please fill in all fields");
            return null;
        }
        formData.append(key, value);
    }
    return formData;
}

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = getFormData({
        email: "email",
        password: "password"
    });
    if (!formData) return;

    const result = await request_api("/user/api/login", formData);
    if (result.status == 200) {
        console.log("Log in Successfully!");
    } else {
        alert("Log In failed: " + result.message);
        console.log(result.status);
    }
});

function checkPassword(password) {
    const checks = [
        password.length >= 8,
        /[A-Z]/.test(password),
        /[a-z]/.test(password),
        /[0-9]/.test(password),
        /[!@#$%^&*(),.?":{}|<>]/.test(password),
        !/^[a-zA-Z]+$/.test(password),
        !/^\d+$/.test(password),
    ];
    return checks.every(Boolean);
}

function resetSignupForm() {
    ["name", "signupEmail", "signupPassword", "confirmPassword"].forEach(
        id => document.getElementById(id).value = ""
    );
}


signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const password = document.getElementById("signupPassword").value;
    const confirm = document.getElementById("confirmPassword").value;
    if (!checkPassword(password)) {
        alert("Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.");
        return;
    } else if (password !== confirm) {
        alert("Passwords do not match");
        return;
    }

    const formData = getFormData({
        username: "name",
        email: "signupEmail",
        password: "signupPassword"
    });
    if (!formData) return;

    const result = await request_api("/user/api/signup", formData);

    if (result.status === 200) {
        console.log("Sign up successfully");
        switchTab(loginTab, signupTab, loginForm, signupForm, toSignup, toLogin);
        resetSignupForm();
        document.getElementById("email").value = formData.get("email");
        document.getElementById("password").value = formData.get("password");
    } else {
        alert("Sign up failed: " + result.message);
        console.log(result.status);
    }
});