function checkStatus() {
  fetch("/api/status")
  .then(() => {
    document.querySelector('#server-status').textContent = "Online";
    document.getElementById('server-status').style.color = "green";
  })
  .catch(() => {
    document.querySelector('#server-status').textContent = "Offline"
    document.getElementById('server-status').style.color = "red";
  });
}

function fetchVectors() {
  fetch("/api/vectors")
  .then(response => response.json())
  .then(data => {
    document.getElementById("vocab-container").textContent = data.master_vocabulary.join(", ");
    const vectorsList = document.getElementById("vector-container");
    vectorsList.innerHTML = "";
    for (const [docName, vectorArray] of Object.entries(data.vector)) {
      const listItem = document.createElement("li");
      listItem.textContent = `${docName} : [${vectorArray.join(", ")}]`;
      vectorsList.appendChild(listItem);
    }
  })
  .catch(error => {
    console.error("Failed to load vector:", error);
    document.getElementById("vocab-container").textContent = "Error loading data.";
    document.getElementById("vocab-container").style.color = "red";
  });
}

function performSearch() {
  const query = document.getElementById("search-box").value;
  if (!query) return;
  const resultsList = document.getElementById("search-results");
  resultsList.innerHTML = "<li>Searching...</li>";

  fetch(`/api/search?search_input=${encodeURIComponent(query)}`)
  .then(response => response.json())
  .then(data => {
    console.log("Search payload:", data);
    resultsList.innerHTML = "";
    for (const[docName, score] of Object.entries(data)) {
      const listItem = document.createElement("li");
      const cleanScore = typeof score === 'number' ? score.toFixed(4) : score;
      listItem.textContent = `${docName} - Similarity: ${cleanScore}`;
      resultsList.appendChild(listItem);
    }
  })
  .catch(error => {
    console.error("Search failed:", error);
    resultsList.innerHTML = "<li style='color: red;'>Error performing search.</li>";
  })
}

setInterval(checkStatus, 5000)
fetchVectors()