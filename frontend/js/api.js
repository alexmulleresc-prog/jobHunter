const API_URL = "http://127.0.0.1:8000";

async function getStats(){
    const response = await fetch(`${API_URL}/stats`);
    return await response.json();
}

async function getJobs(filters = {}){
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_URL}/empleos?${params}`);
    return await response.json();
}

async function getFilters(){
    const response = await fetch(`${API_URL}/filters`);
    return await response.json();
}

async function runScrapers(){
    const response = await fetch(`${API_URL}/scrapers/run`,{method: "POST"});
    return await response.json();
}