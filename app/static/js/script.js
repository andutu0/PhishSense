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

            try {
                const response = await fetch("/analyze", {
                    method: "POST",
                    body: formData
                });

                const data = await response.json();

                if (data.error) {
                    resultDiv.innerHTML =
                        "<p style='color:red;'>" + data.error + "</p>";
                } else {
                    const color = data.verdict === "malicious" ? "red" : "green";
                    resultDiv.innerHTML =
                        "<h3 style='color:" + color + "'>Verdict: " +
                        data.verdict.toUpperCase() + "</h3>" +
                        "<p>Confidence: " +
                        (data.confidence * 100).toFixed(1) + "%</p>";
                }

            } catch (err) {
                resultDiv.innerHTML =
                    "<p style='color:red;'>Error: " + err.message + "</p>";
            }
        });
    }

});
