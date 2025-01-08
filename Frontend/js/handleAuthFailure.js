import { refreshAccessToken } from './authenticate.js';

export async function handleAuthFailure(instance) {
    if (instance.retryCount < instance.maxRetries) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        instance.retryCount++;

        const refreshSuccess = await refreshAccessToken();

        if (refreshSuccess) {
            await instance.fetchInventory();
        } else {
            console.error("handleAuthFailure() refresh failed");
        }
    } else {
        console.error("handleAuthFailure() max retries reached");
    }
}
