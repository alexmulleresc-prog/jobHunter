const API_URL = "http://127.0.0.1:8000";

async function getStats(){
    const response = await fetch(`${API_URL}/stats`);
    return await response.json();
}

async function getJobs(search = ""){
    const response = await fetch(`${API_URL}/empleos?search=${encodeURIComponent(search)}`);
    return await response.json();
}

async function searchJobs(query){

}