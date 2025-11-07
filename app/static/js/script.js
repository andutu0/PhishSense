document.getElementById("analyze-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(e.target);
  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "Analyzing... ⏳";

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    if (data.error) {
      resultDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
    } else {
      const color = data.verdict === "malicious" ? "red" : "green";
      resultDiv.innerHTML = `
        <h3 style="color:${color}">Verdict: ${data.verdict.toUpperCase()}</h3>
        <p>Confidence: ${(data.confidence * 100).toFixed(1)}%</p>
      `;
    }
  } catch (err) {
    resultDiv.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
  }
});
