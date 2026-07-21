function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);

    if (parts.length === 2) {
        return parts.pop().split(";").shift();
    }

    return null;
}

async function api(url, options = {}) {

    const csrf = getCookie("csrf_access_token");

    options.credentials = "same-origin";

    options.headers = {
        ...(options.headers || {}),
        "X-CSRF-TOKEN": csrf
    };

    return fetch(url, options);
}   