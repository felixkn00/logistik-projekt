import { authenticate, refreshAccessToken } from './authenticate.js'

export async function authGuard() {
    console.log("auth guard")
    
    const isAuthenticated = await authenticate()
    
    if (isAuthenticated) {
       
    } else {
        
        const refreshed = await refreshAccessToken()
        if (refreshed) {
            const retryAuth = await authenticate()
            if (retryAuth) {
                return
            }
        }
        
        window.location.href = "index.html";
    }
}
