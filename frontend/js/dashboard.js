async function loadDashboard(){
    const stats = await getStats();
    console.log(stats);
    document.getElementById("total-jobs").textContent = stats.total_jobs;
    document.getElementById("total-companies").textContent = stats.total_companies;
    document.getElementById("total-sources").textContent = Object.keys(stats.sources).length;
    //document.getElementById("jobs-added").textContent = "-";
    
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