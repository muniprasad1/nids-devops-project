let chart;
let labels = [];
let values = [];
let attackCounter = 0;

function updateChart(rate) {
    labels.push(new Date().toLocaleTimeString());
    values.push(rate);

    if (labels.length > 10) {
        labels.shift();
        values.shift();
    }

    if (!chart) {
        const ctx = document.getElementById("chart").getContext("2d");
        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Packet Rate",
                    data: values,
                    borderWidth: 2
                }]
            }
        });
    } else {
        chart.data.labels = labels;
        chart.data.datasets[0].data = values;
        chart.update();
    }
}

async function fetchLogs() {
    try {
        const res = await fetch("http://127.0.0.1:5000/logs");
        const data = await res.json();

        const table = document.getElementById("logTable");
        table.innerHTML = "";

        document.getElementById("totalLogs").innerText = data.length;

        attackCounter = 0;

        data.slice().reverse().forEach(log => {

            updateChart(log.packet_rate);

            if (log.status === "ATTACK") {
                attackCounter++;
            }

            const row = `<tr>
                <td>${log.time}</td>
                <td>${log.packet_rate.toFixed(2)}</td>
                <td class="${log.status}">${log.status}</td>
                <td>${log.ip || "N/A"}</td>
                <td class="${log.action || "ALLOWED"}">${log.action || "ALLOWED"}</td>
            </tr>`;

            table.innerHTML += row;
        });

        document.getElementById("attackCount").innerText = attackCounter;

    } catch (error) {
        console.error("Error fetching logs:", error);
    }
}

setInterval(fetchLogs, 3000);