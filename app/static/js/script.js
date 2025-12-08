document.addEventListener("DOMContentLoaded", function () {

    // ============================
    // FORM SUBMIT ANALYSIS
    // ============================
    const analyzeForm = document.getElementById("analyze-form");

    if (analyzeForm) {
        analyzeForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const formData = new FormData(analyzeForm);
            const resultDiv = document.getElementById("result");
            resultDiv.innerHTML = "Analyzing... ⏳";
            resultDiv.className = "result";

            try {
                const response = await fetch("/analyze", {
                    method: "POST",
                    body: formData
                });

                const data = await response.json();

                if (data.error) {
                    resultDiv.innerHTML = "<p style='color:red;'>" + data.error + "</p>";
                    resultDiv.className = "result";
                } else {
                    const isMalicious = data.verdict === "malicious" || data.verdict === "phishing";
                    const statusClass = isMalicious ? "malicious" : "safe";
                    const statusText = isMalicious ? "MALICIOUS" : "SAFE";
                    
                    resultDiv.className = "result " + statusClass;
                    resultDiv.innerHTML =
                        "<h3>" + statusText + "</h3>" +
                        "<p>" + (data.confidence * 100).toFixed(1) + "% confidence</p>";
                }

            } catch (err) {
                resultDiv.innerHTML = "<p style='color:red;'>Error: " + err.message + "</p>";
                resultDiv.className = "result";
            }
        });
    }

});