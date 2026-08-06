const searchInput = document.getElementById("search-input");

function initializeSearch(){
    searchInput.addEventListener("input", handleSearch);
}

let timeout;

function handleSearch(){
    clearTimeout(timeout);
    timeout = setTimeout(async () => {
        const query = searchInput.value.trim();
        await loadJobs({search: query});
    },300);
}

function initializeFilters(){

}