const activeFiltersContainer = document.getElementById("active-filters");

function createChip(icon, value, key){
    const chip = document.createElement("div");
    chip.className = "filter-chip";
    chip.innerHTML = `${icon} ${value}
        <button>✕</button>`;
    const button = chip.querySelector("button");
    button.addEventListener("click", async () => {currentFilters[key] = ""; await loadJobs(currentFilters);if(key === "search"){searchInput.value = "";};});
    activeFiltersContainer.appendChild(chip);
}

function renderActiveFilters(){
    activeFiltersContainer.innerHTML = "";
    let activeCount = 0;
    if(currentFilters.search){
        createChip("🔍", currentFilters.search,"search"); activeCount++;
    }
    if(currentFilters.empresa){
        createChip("🏢", currentFilters.empresa,"empresa"); activeCount++;
    }
    if(currentFilters.fuente){
        createChip("🌐", currentFilters.fuente,"fuente"); activeCount++;
    }
    if(activeCount >= 2){
        createClearButton();
    }
}

function createClearButton(){
    const button = document.createElement("button");
    button.className = "clear-filters-button";
    button.innerHTML = "🗑";
    button.title = "Limpiar filtros";
    button.addEventListener("click", async () => {Object.keys(currentFilters).forEach(key => {currentFilters[key] = "";});searchInput.value = "";await loadJobs(currentFilters);});
    activeFiltersContainer.appendChild(button);
}