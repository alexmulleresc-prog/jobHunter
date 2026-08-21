async function init(){

    await loadDashboard();
    await loadJobs();
    initializeSearch();
    await initializeDashboardFilters();
    initializeUpdateButton();
    initializeSort();
    initializeNewJobsCard();
    initializeFavoritesButton();
    initializeBackButton();
}
init();