function checkStatus() {
  fetch("http://localhost:8000/api/status")
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
  fetch("http://localhost:8000/api/vectors")
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

setInterval(checkStatus, 5000)
fetchVectors()