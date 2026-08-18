async function loadDashboard(){
    const stats = await getStats();
    console.log(stats);
    document.getElementById("total-jobs").textContent = stats.total_jobs;
    document.getElementById("total-companies").textContent = stats.total_companies;
    document.getElementById("total-sources").textContent = Object.keys(stats.sources).length;
    updateLastUpdateCard(stats);
    //document.getElementById("jobs-added").textContent = "-";
    
}
function updateLastUpdateCard(stats){

    document.getElementById("jobs-added").textContent = `+${stats.last_new_jobs}`;

    document.getElementById("last-update").textContent =
        formatRelativeTime(stats.last_update);
}
function formatRelativeTime(dateString){
    if(!dateString){
        return "Nunca";}
    const now = new Date();
    const date = new Date(dateString);
    const diff = Math.floor((now - date) / 1000);
    if(diff < 60){
        return "Hace unos segundos";}
    const minutes = Math.floor(diff / 60);
    if(minutes < 60){
        return `Hace ${minutes} min`;}
    const hours = Math.floor(minutes / 60);
    if(hours < 24){
        return `Hace ${hours} h`;}
    const days = Math.floor(hours / 24);
    return `Hace ${days} días`;
}
async function initializeDashboardFilters() {
    const filters = await getFilters();
    const companyCard = document.getElementById("companies-card");
    const sourceCard = document.getElementById("sources-card");
    companyCard.addEventListener("click", () => {
        showDropdown(companyCard, filters.companies,async(company) =>{currentFilters.empresa = company.name; await loadJobs(currentFilters)});});
    sourceCard.addEventListener("click", () => {
        showDropdown(sourceCard, filters.sources,async(source) =>{currentFilters.fuente = source.name; await loadJobs(currentFilters)});});
}

setInterval(async() =>{
    const stats = await getStats();
    document.getElementById("last-update").textContent = formatRelativeTime(stats.last_update);
},60000);