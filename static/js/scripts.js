document.getElementById("listen-button").addEventListener("click", function() {
    fetch("/listen", {
        method: "POST"
    })
    .then(response => response.json())
    .then(data => {
        const outputDiv = document.getElementById("output");
        const userInput = document.createElement("p");
        userInput.innerHTML = `<strong>You:</strong> ${data.user_input}`;
        const aiResponse = document.createElement("p");
        aiResponse.innerHTML = `<strong>AI:</strong> ${data.response}`;
        outputDiv.appendChild(userInput);
        outputDiv.appendChild(aiResponse);
        outputDiv.scrollTop = outputDiv.scrollHeight;
    })
    .catch(error => console.error("Error:", error));
});
