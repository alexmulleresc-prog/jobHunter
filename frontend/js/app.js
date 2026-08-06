async function init(){

    await loadDashboard();
    await loadJobs();
    initializeSearch();
    await initializeDashboardFilters();
}
init();