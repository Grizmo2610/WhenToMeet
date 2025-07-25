const loginButton = document.getElementById("nav-login-button");
const signInButton = document.getElementById("nav-signup-button");
const tabLogIn = document.getElementById("tabLogin");
const tabSignUp = document.getElementById("tabSignup");
const submitButton = document.getElementById("submit-button");

function switchTab(activeBtn, inactiveBtn, showTab, hideTab, submitText, submitColor) {
    showTab.classList.remove("hidden");
    hideTab.classList.add("hidden");

    activeBtn.classList.add(...submitColor);
    activeBtn.classList.remove("bg-gray-300", "text-black");

    inactiveBtn.classList.remove("bg-blue-500", "bg-green-500", "text-white");
    inactiveBtn.classList.add("bg-gray-300", "text-black");

    submitButton.classList.remove("bg-blue-500", "bg-green-500");
    submitButton.classList.add(submitColor[0]);
    submitButton.textContent = submitText;
}

loginButton.addEventListener("click", () => {
    switchTab(
        loginButton,
        signInButton,
        tabLogIn,
        tabSignUp,
        "Log In",
        ["bg-blue-500", "text-white"],
    );
});

signInButton.addEventListener("click", () => {
    switchTab(
        signInButton,
        loginButton,
        tabSignUp,
        tabLogIn,
        "Sign Up",
        ["bg-green-500", "text-white"]

    );
});


submitButton.addEventListener('click', async () => {
    try {
        const formData = new FormData();
        if (submitButton.textContent == "Log In") {
            const email = document.getElementById("login-email");
            const password = document.getElementById("login-password");
            formData.append("email", email.value);
            formData.append("password", password.value);
            try {
                const res = await fetch('/user/api/login', { 
                    method: "POST", 
                    body: formData 
                }
            );
                const data = await res.json();
                console.log(data.status);
            } catch (err) {
                console.log(err);
            }

        } else if (submitButton.textContent == "Sign Up") {
            const email = document.getElementById("signup-email");
            const password = document.getElementById("signup-password");
            formData.append("email", email.value);
            formData.append("password", password.value);
            try {
                const res = await fetch('/user/api/signup', { 
                    method: "POST", 
                    body: formData 
                }
            );
                const data = await res.json();
                console.log(data.status);
            } catch (err) {
                console.log(err);
            }
        }
    } catch (err) {

    }
})