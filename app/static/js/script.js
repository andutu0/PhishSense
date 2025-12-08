document.addEventListener("DOMContentLoaded", function () {
    const analyzeForm = document.getElementById("analyze-form");
    const historyButton = document.getElementById("load-history");
    const historySection = document.getElementById("history");
    const logToggle = document.getElementById("log-toggle");

    async function fetchSessionHistory() {
        if (!historySection) return;

        historySection.className = "history";
        historySection.innerHTML = "";
        if (historyButton) {
            historyButton.disabled = true;
            historyButton.textContent = "Loading...";
        }

        try {
            const resp = await fetch("/api/session_history?limit=20");
            const data = await resp.json();
            const items = data.items || [];

            if (!items.length) {
                historySection.innerHTML = "<p class='muted'>No session history yet.</p>";
                return;
            }

            const list = document.createElement("ul");
            list.className = "history-list";

            items.forEach((rec) => {
                const li = document.createElement("li");
                const verdict = rec.verdict || "?";
                const verdictClass = verdict === "phishing" || verdict === "malicious" || verdict === "suspicious" ? "bad" : "good";
                const tsRaw = rec.timestamp || "";
                const tsDate = tsRaw ? new Date(tsRaw) : null;
                const ts = tsDate
                    ? tsDate.toLocaleTimeString("ro-RO", { hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false, timeZone: "Europe/Bucharest" })
                    : "?";
                const type = rec.type || "?";

                let inputPreview = "";
                const makeEmailPreview = (obj) => {
                    const subj = obj?.subject || "";
                    const body = obj?.body || "";
                    return `subject: ${subj.slice(0, 50)} | body: ${body.slice(0, 50)}`.trim();
                };

                if (typeof rec.input === "string") {
                    inputPreview = rec.input.slice(0, 120);
                } else if (rec.input && typeof rec.input === "object") {
                    inputPreview = makeEmailPreview(rec.input);
                } else if (rec.parsed && typeof rec.parsed === "object") {
                    inputPreview = makeEmailPreview(rec.parsed);
                } else {
                    inputPreview = JSON.stringify(rec).slice(0, 120);
                }

                li.innerHTML = `<span class="pill ${verdictClass}">${verdict}</span> <strong>${type}</strong> <span class="muted">${ts}</span><br><span class="small">${inputPreview}</span>`;
                list.appendChild(li);
            });

            historySection.appendChild(list);
        } catch (err) {
            historySection.innerHTML = `<p style='color:red;'>Error loading history: ${err.message}</p>`;
        } finally {
            if (historyButton) {
                historyButton.disabled = false;
                historyButton.textContent = "View session history";
            }
        }
    }

    if (analyzeForm) {
        analyzeForm.addEventListener("submit", async function (e) {
            e.preventDefault();

            const textInput = document.getElementById("text").value.trim();
            const fileInput = document.getElementById("image").files[0];
            const shouldLog = logToggle ? Boolean(logToggle.checked) : false;
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
                    formData.append("log", String(shouldLog));
                    
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
                            log: shouldLog
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
                            log: shouldLog
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

    if (historyButton && historySection) {
        historyButton.addEventListener("click", fetchSessionHistory);
    }
});
