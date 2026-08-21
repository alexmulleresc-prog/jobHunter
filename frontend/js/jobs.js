const jobsContainer = document.getElementById("jobs");
const resultsCount = document.getElementById("results-count");

function formatDate(dateString){
    const date = new Date(dateString);
    return date.toLocaleDateString("es-AR",{
        day:"numeric",
        month:"short",
        year:"numeric"
    });

}

function formatLocation(location){

    if(!location) return "🌍 No especificada";
    if(location.toLowerCase().includes("world"))
        return "🌍 Worldwide";
    if(location.toLowerCase().includes("europe"))
        return "🇪🇺 Europe";
    return `📍 ${location}`;

}

function createJobCard(job){
    const card = document.createElement("article");
    card.className = "job-card";
    card.innerHTML = `
        <div class="job-header">
            <div>
                <h2 class="job-title">${job.titulo}</h2>
                <p class="job-company">${job.empresa}</p>
                
            </div>
            <button class="favorite-button ${isFavorite(job.url) ? "favorite-active" : ""}"
                    onclick="toggleFavorite('${job.url}', this)">
                ${isFavorite(job.url) ? "♥" : "♡"}
            </button>
        </div>
        <div class="job-meta">
            <div class="location">${formatLocation(job.ubicacion)}</div>
            <div class="salary">${job.salario ? job.salario : ""}</div>
        </div>
        <div class="job-tags">
            ${
                (job.tags ?? [])
                    .slice(0,6)
                    .map(tag => `<span class="tag">${tag}</span>`)
                    .join("")
                    
            }
        </div>
        <div class="job-footer">
            <span class="job-date">
                ${formatDate(job.fecha_publicacion)}
            </span>
            <p class="job-source">🌐 ${job.fuente}</p>
            <a
                href="${job.url}"
                target="_blank"
                class="job-link"
            >
                Ver oferta →
            </a>
        </div>
    `;
    jobsContainer.appendChild(card)
}

function getOrderLabel(order){
    const labels = {
        recientes: "Más recientes",
        antiguos: "Más antiguos",
        titulo_az: "Título A → Z",
        titulo_za: "Título Z → A",
        empresa_az: "Empresa A → Z",
        empresa_za: "Empresa Z → A"
    };
    return labels[order] || "Más recientes";
}

let currentPage = 1;
const jobsPerPage = 25;
let totalResults = 0;
let currentOrder = "recientes";
let currentView = "all";
let specialJobs = [];

async function loadJobs(filters = {}){
    currentView = "all";
    const result = await getJobs({...filters, orden: currentOrder, limit: jobsPerPage, offset: (currentPage - 1) * jobsPerPage});
    const jobs =result.jobs;
    totalResults = result.total;
    jobsContainer.innerHTML = "";
    const firstResult = (currentPage - 1) * jobsPerPage + 1;
    const lastResult = Math.min(currentPage * jobsPerPage, result.total);
    resultsCount.textContent =`Mostrando ${firstResult} - ${lastResult} de ${result.total} resultados · Orden: ${getOrderLabel(currentOrder)}`;
    jobs.forEach(createJobCard);
    renderActiveFilters();
    renderPagination();
}

function renderPagination(){
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";
    const totalPages = Math.ceil(totalResults / jobsPerPage);
    if(totalPages <= 1){
        return;}
    const previousButton = document.createElement("button");
    previousButton.textContent = "Anterior";
    previousButton.disabled = currentPage === 1;
    previousButton.addEventListener("click", async () => {currentPage--;
        if(currentView === "all"){
            await loadJobs(currentFilters);}
        else {renderSpecialJobsPage();}
        window.scrollTo({top: 0,behavior: "smooth"});
    });
    pagination.appendChild(previousButton);
    const pages = [];
    pages.push(1);
    if(currentPage > 3){pages.push("...");}
    for(
        let page = currentPage - 1;
        page <= currentPage + 1;
        page++
    ){
        if(page > 1 && page < totalPages){
            pages.push(page);}
    }
    if(currentPage < totalPages - 2){
        pages.push("...");
    }
    if(totalPages > 1){
        pages.push(totalPages);
    }
    pages.forEach(page => {
        if(page === "..."){
            const dots = document.createElement("span");
            dots.textContent = "...";
            pagination.appendChild(dots);
            return;
        }
        const pageButton = document.createElement("button");
        pageButton.textContent = page;
        if(page === currentPage){
            pageButton.classList.add("active");
        }
        pageButton.addEventListener("click", async () => {
            currentPage = page;
            if(currentView === "all"){
                await loadJobs(currentFilters);
            } else {
                renderSpecialJobsPage();
            }
            window.scrollTo({top: 0,behavior: "smooth"});
        });
        pagination.appendChild(pageButton);
    });
    const nextButton = document.createElement("button");
    nextButton.textContent = "Siguiente";
    nextButton.disabled = currentPage === totalPages;
    nextButton.addEventListener("click", async () => {
        currentPage++;
        if(currentView === "all"){
            await loadJobs(currentFilters);}
        else {renderSpecialJobsPage();}
        window.scrollTo({top: 0,behavior: "smooth"});
    });
    pagination.appendChild(nextButton);
}
function renderSpecialJobsPage(){
    jobsContainer.innerHTML = "";
    const start = (currentPage - 1) * jobsPerPage;
    const end = Math.min(start + jobsPerPage, specialJobs.length);
    const jobsToShow = specialJobs.slice(start, end);
    if(currentView === "new"){
        resultsCount.textContent =
            `Mostrando ${start + 1} - ${end} de ${specialJobs.length} resultados · Nuevos empleos`;
    }
    if(currentView === "favorites"){
        resultsCount.textContent =
            `Mostrando ${start + 1} - ${end} de ${specialJobs.length} empleos favoritos`;
    }
    jobsToShow.forEach(createJobCard);
    renderPagination();
}

function initializeNewJobsCard(){
    const newJobsCard = document.getElementById("new-jobs-card");
    const backButton = document.getElementById("back-to-all-jobs"); 
    newJobsCard.addEventListener("click", async () => {
        const response = await fetch(`${API_URL}/empleos/nuevos`);
        const jobs = await response.json();
        jobsContainer.innerHTML = "";
        totalResults = jobs.length;
        currentPage = 1;
        currentView = "new";
        specialJobs = jobs;
        renderSpecialJobsPage();
        backButton.style.display = "block";
        window.scrollTo({top: 0, behavior: "smooth"});
    });
}

function initializeFavoritesButton(){
    const favoritesButton =document.getElementById("favorites-button");
    const backButton = document.getElementById("back-to-all-jobs"); 
    favoritesButton.addEventListener("click", async () => {await loadFavorites();
        backButton.style.display = "block";
    });
}

async function loadFavorites(){
    const favorites = JSON.parse(localStorage.getItem("jobhunter-favorites") || "[]");
    const favoritesButton = document.getElementById("favorites-button");
    favoritesButton.classList.add("favorite-active");
    jobsContainer.innerHTML = "";
    currentView = "favorites";
    currentPage = 1;
    totalResults = 0;
    specialJobs = [];
    if(favorites.length === 0){
        resultsCount.textContent = "No tenés empleos favoritos"; pagination.innerHTML = ""; return;}
    const response = await fetch(`${API_URL}/empleos/todos`);
    const allJobs = await response.json();
    const favoriteJobs = allJobs.filter(job =>favorites.includes(job.url));
    specialJobs = favoriteJobs;
    totalResults = favoriteJobs.length;
    renderSpecialJobsPage();
    window.scrollTo({top: 0,behavior: "smooth"});
}

function toggleFavorite(url, button){
    const favorites = JSON.parse(localStorage.getItem("jobhunter-favorites") || "[]");
    const index = favorites.indexOf(url);
    if(index === -1){favorites.push(url);button.textContent = "♥";button.classList.add("favorite-active");}
        else {favorites.splice(index, 1);button.textContent = "♡";button.classList.remove("favorite-active");}
    localStorage.setItem("jobhunter-favorites",JSON.stringify(favorites));
}
function isFavorite(url){
    const favorites = JSON.parse(localStorage.getItem("jobhunter-favorites") || "[]");
    return favorites.includes(url);
}

function initializeBackButton(){
    const backButton = document.getElementById("back-to-all-jobs");
    const favoritesButton = document.getElementById("favorites-button");
    backButton.addEventListener("click", async () => {
        backButton.style.display = "none";
        favoritesButton.classList.remove("favorite-active");
        currentPage = 1;
        await loadJobs(currentFilters);
        window.scrollTo({top: 0,behavior: "smooth"});
    });
}