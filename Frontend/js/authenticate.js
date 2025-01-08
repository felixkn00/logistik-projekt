async function retryWithDelay(func, attempts, delay) {
    for (let i = 0; i < attempts; i++) {
        const result = await func()
        if (result) {
            return result
        }
        console.warn(`retryWithDelay() try ${i + 1} ${delay} Delay Time`)
        await new Promise(resolve => setTimeout(resolve, delay))
    }
    console.error("retryWithDelay() Failed")
    return null
}


async function accessTokenAuthReq() {
    const access_token = Cookies.get('access_token')
    const refresh_token = Cookies.get('refresh_token')
    const uid = Cookies.get('uid')

    if (!access_token || !refresh_token || !uid) {
        console.error("accessTokenAuthReq() empty values, access_token, refresh_token, uid");
        return null
    }

    try {
        const response = await fetch('http://localhost:5001/auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=UTF-8',
                'accesstoken': access_token,
                'refreshtoken': refresh_token,
                'uid': uid
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP Status: ${response.status}`)
        }

        const data = await response.json();
        console.log("accessTokenAuthReq() Token successful received:", data)
        return data
    } catch (error) {
        console.error('accessTokenAuthReq() Failed to retrieve token:', error)
        return null
    }
}

async function refreshAccessTokenAuthRequest() {
    const refresh_token = Cookies.get('refresh_token')
    const uid = Cookies.get('uid')

    if (!refresh_token || !uid) {
        console.error("refreshAccessTokenAuthRequest() empty values, refresh_token, uid")
        return null
    }

    try {
        const response = await fetch('http://localhost:5001/refresh_access_token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'refreshtoken': refresh_token,
                'uid': uid
            },
            body: JSON.stringify({})
        });

        if (!response.ok) {
            throw new Error(`HTTP Status: ${response.status}`)
        }

        const data = await response.json();
        console.log("refreshAccessTokenAuthRequest() Token successful received:", data)
        return data
    } catch (error) {
        console.error('refreshAccessTokenAuthRequest() Failed to retrieve token:', error)
        return null
    }
}

export async function authenticate() {
    let result = await retryWithDelay(accessTokenAuthReq, 5, 250)

    if (result && result.status === "access_token_auth_successful") {
        Cookies.set('access_token', result.new_access_token);
        console.log("authenticate() Access Token successfully set", result.new_access_token)
        return true
    } 
    else {
        console.log("authenticate() Access Token Authentication is failed")

        result = await retryWithDelay(refreshAccessToken, 5, 250)
        if (result) {
            console.log("authenticate() Retry Token Authentication")
            result = await retryWithDelay(accessTokenAuthReq, 5, 250)

            if (result && result.status === "access_token_auth_successful") {
                Cookies.set('access_token', result.new_access_token)
                console.log("authenticate() Access Token successfully set", result.new_access_token)
                return true
            }
        }

        console.error("authenticate() Access Token Authentication is failed")
        return false
    }
}

export async function refreshAccessToken() {
    const result = await retryWithDelay(refreshAccessTokenAuthRequest, 5, 250)
    if (result && result.status === "refresh_token_auth_successful") {
        Cookies.set('access_token', result.new_access_token)
        console.log("refreshAccessToken() Access Token successfully set:", result.new_access_token)
        return true
    }

    console.error("refreshAccessToken() Access Token Authentication is failed")
    return false
}

