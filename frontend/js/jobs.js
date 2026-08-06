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
            <button class="favorite-button">
                ♡
            </button>
        </div>
        <div class="job-meta">
            <div class="location">${formatLocation(job.ubicacion)}</div>
            <div class="salary">${job.salario ? `<div class="salary">${job.salario}</div>` : ""}</div>
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

async function loadJobs(filters = {}){
    const jobs = await getJobs(filters);
    jobsContainer.innerHTML = "";
    resultsCount.textContent =`${jobs.length} resultados encontrados`;
    jobs.forEach(createJobCard);
}
