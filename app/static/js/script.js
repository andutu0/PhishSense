document.addEventListener("DOMContentLoaded", function () {
    const analyzeForm = document.getElementById("analyze-form");

    if (analyzeForm) {
        analyzeForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const textInput = document.getElementById("text").value.trim();
            const fileInput = document.getElementById("image").files[0];
            const resultDiv = document.getElementById("result");
            
            resultDiv.innerHTML = "Analyzing... ⏳";
            resultDiv.className = "result";

            try {
                let response;
                
                // determine input type and call appropriate API
                if (fileInput) {
                    // QR code image uploaded
                    const formData = new FormData();
                    formData.append("qr_image", fileInput);
                    formData.append("log", "false");
                    
                    response = await fetch("/api/analyze_qr", {
                        method: "POST",
                        body: formData
                    });
                } else if (textInput.includes("http://") || textInput.includes("https://")) {
                    // URL detected
                    response = await fetch("/api/analyze_url", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            url: textInput,
                            log: false
                        })
                    });
                } else if (textInput) {
                    // Email text
                    response = await fetch("/api/analyze_email", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            subject: "",
                            body: textInput,
                            sender: "",
                            log: false
                        })
                    });
                } else {
                    resultDiv.innerHTML = "<p style='color:red;'>Please provide text or upload an image</p>";
                    resultDiv.className = "result";
                    return;
                }

                const data = await response.json();

                if (data.error) {
                    resultDiv.innerHTML = "<p style='color:red;'>" + data.error + "</p>";
                    resultDiv.className = "result";
                } else {
                    // check for malicious verdict
                    // we got the words mixed up so we check for phishing, malicious, or suspicious
                    // as we lost count of what we named things
                    const isMalicious = data.verdict === "phishing" || 
                                       data.verdict === "malicious" || 
                                       data.verdict === "suspicious";
                    const statusClass = isMalicious ? "malicious" : "safe";
                    const statusText = isMalicious ? "MALICIOUS" : "SAFE";

                    const confidence = (data.confidence ?? data.score ?? 0) * 100;

                    resultDiv.className = "result " + statusClass;
                    resultDiv.innerHTML =
                        "<h3>" + statusText + "</h3>" +
                        "<p>" + confidence.toFixed(1) + "% confidence</p>";
                }
            } catch (err) {
                resultDiv.innerHTML = "<p style='color:red;'>Error: " + err.message + "</p>";
                resultDiv.className = "result";
            }
        });
    }
}
);