// Polls the server every 5 seconds to update the online/offlnie status indicator
function checkStatus() {
  fetch("/api/status")
  .then(() => {
    const status = document.querySelector('#server-status')
    status.textContent = "Online";
    status.style.color = "#16a34a";
  })
  .catch(() => {
    const status = document.querySelector('#server-status')
    status.textContent = "Offline"
    status.style.color = "#dc2626";
  });
}

// Deletes a document
function deleteDocument(docName) {
  const isConfirmed = confirm(`Are you sure you want to delete "${docName}"?`)
  if (!isConfirmed) return;

  fetch(`/api/delete?doc_name=${encodeURIComponent(docName)}`, { method: "DELETE"})
  .then(response => {
    if (response.ok) {
      fetchVectors(); // refreshes the UI immediately after successful deletion
    } else {
      alert("Failed to delete document from the server.");
    }
  })
  .catch(error => console.error("Error deleting document:", error));
}

// Fetches the latest vocabulary and vector data from the backend to populate the UI
function fetchVectors() {
  fetch("/api/vectors")
  .then(response => response.json())
  .then(data => {
    // Displays the master vocabulary list as a scrollable container
    const vocabContainer = document.getElementById("vocab-container");
    const totalLabel = document.createElement("strong");
    totalLabel.textContent = "Total global dimensions:";
    const total = document.createElement("div");
    total.append(totalLabel, ` ${data.master_vocabulary.length}`);

    const vocabScroll = document.createElement("div");
    vocabScroll.className = "vocab-scroll";
    for (const word of data.master_vocabulary) {
      const tag = document.createElement("span");
      tag.className = "vocab-tag";
      tag.textContent = word;
      vocabScroll.appendChild(tag);
    }

    vocabContainer.replaceChildren(total, vocabScroll);
    
    // Clears and rebuild the list of document vectors
    const vectorsList = document.getElementById("vector-container");
    vectorsList.innerHTML = "";

    for (const [docName, vectorArray] of Object.entries(data.vector)) {
      const listItem = document.createElement("li");
      listItem.style.display = "flex";
      listItem.style.justifyContent = "space-between";
      listItem.style.alignItems = "center";
      listItem.style.padding = "5px 0";

      // Calculates active dimensions (non-zero values)
      const uniqueWords = vectorArray.filter(val => val > 0).length;

      // Shows metadata instead of raw floats
      const label = document.createElement("span");
      const nameElement = document.createElement("strong");
      nameElement.textContent = docName;
      label.append(nameElement, ` - ${uniqueWords} unique words`);

      const deleteButton = document.createElement("button");
      deleteButton.className = "delete-btn";
      deleteButton.textContent = "Delete";
      deleteButton.addEventListener("click", () => deleteDocument(docName));

      listItem.append(label, deleteButton);
      vectorsList.appendChild(listItem);
    }
  })
  .catch(error => {
    console.error("Failed to load vector:", error);
    const vocabContainer = document.getElementById("vocab-container");
    vocabContainer.textContent = "Error loading data.";
    vocabContainer.style.color = "#dc2626";
  });
}

// Sends the user's search query to the backend and displays ranked similarity scores
function performSearch() {
  const query = document.getElementById("search-box").value;
  if (!query) return; // Prevent empty searches
  const resultsList = document.getElementById("search-results");
  resultsList.innerHTML = "<li>Searching...</li>";

  fetch(`/api/search?search_input=${encodeURIComponent(query)}`)
  .then(response => response.json())
  .then(data => {
    console.log("Search payload:", data);
    resultsList.innerHTML = ""; // Clear loading text

    // Displays each matched document and its formatted similarity score
    for (const[docName, score] of Object.entries(data)) {
      const listItem = document.createElement("li");
      const cleanScore = typeof score === 'number' ? score.toFixed(4) : score;
      listItem.textContent = `${docName} - Similarity: ${cleanScore}`;
      resultsList.appendChild(listItem);
    }

    // Shows a message when no document shares words with the query
    if (resultsList.children.length === 0) {
      resultsList.textContent = "No matching documents.";
    }
  })
  .catch(error => {
    console.error("Search failed:", error);
    resultsList.innerHTML = "<li class='error-msg'>Error performing search.</li>";
  })
}

// Handles the file upload process and updates the inline UI status message
async function uploadDocument() {
  const fileInput = document.getElementById('docUpload');
  const statusText = document.getElementById('upload-status');

  // Ensures a file is actually selected
  if (fileInput.files.length === 0) {
    statusText.textContent = "Please select a file first";
    statusText.className = "error-msg";
    return;
  }

  // Packages the file into a FormData object for the POST request
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  statusText.textContent = "Uploading...";
  statusText.className = ""; 
  try {
    const response = await fetch('/api/upload', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      fetchVectors(); // Refreshes the data views to include the new document
      statusText.textContent = "Document uploaded successfully!";
      statusText.className = "success-msg";
      fileInput.value=""; // Clears the file picker
    } else {
      statusText.textContent = "Upload failed on the server.";
      statusText.className = "error-msg";
    }
  } catch (error) {
    statusText.textContent = "Network error during upload.";
    statusText.className = "error-msg";
  }
}

// Runs a search when the search form is submitted by pressing Enter key or clicking on Search button
document.getElementById("search-form").addEventListener("submit", event => {
  event.preventDefault(); // Stops the browser from reloading the page
  performSearch();
});

// Initialises application state on load
setInterval(checkStatus, 5000); // Checks server status every 5 seconds
fetchVectors(); // Loads initial database contents