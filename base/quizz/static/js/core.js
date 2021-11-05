function getCookie() {
    const cookieString = document.cookie;
    const cookieArray = cookieString.split(';');
    const cookie = {};
    for (let i = 0; i < cookieArray.length; i++) {
        const cookiePair = cookieArray[i].split('=');
        cookie[cookiePair[0].trim()] = cookiePair[1];
    }
    return cookie;
}

function getCsrfToken() {
    return getCookie()['csrftoken'];
}

async function sendRequest(url, data, method = 'GET') {
    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (error) {
        console.log(error);
        throw error;
    }
}