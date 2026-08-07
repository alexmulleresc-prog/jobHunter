const searchInput = document.getElementById("search-input");

function initializeSearch(){
    searchInput.addEventListener("input", handleSearch);
}

let timeout;

function handleSearch(){
    clearTimeout(timeout);
    timeout = setTimeout(async () => {
        const query = searchInput.value.trim();
        currentFilters.search = query;
        await loadJobs(currentFilters);
    },300);
}

function initializeFilters(){

}