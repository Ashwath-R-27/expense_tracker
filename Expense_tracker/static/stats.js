// Category Chart
const labels = window.labels || [];
const values = window.values || [];

console.log(labels, values);

if (labels.length > 0) {
    const data = [{
        x: labels,
        y: values,
        type: 'bar',
        marker: {
            color: "#06bd5e"
        }
    }];

    const layout = {
        title: "Expenses by Category",
        xaxis: { title: "Category" },
        yaxis: { title: "Amount (₹)" }
    };

    Plotly.newPlot('barChart', data, layout, { responsive: true });
} else {
    document.getElementById("barChart").innerHTML = "No data available";
}


// Payment Chart
const payLabels = window.pay_labels || [];
const payValues = window.pay_values || [];

console.log("Payment:", payLabels, payValues);

if (payLabels.length > 0) {
    const pieData = [{
        labels: payLabels,
        values: payValues,
        type: 'pie',
        hole: 0,
        textinfo: "label+percent",
        marker: {
            colors: [
                "#003d5c", "#ff5f66", "#ffa600", "#594e90", "#bc4c96"
            ]
        }
    }];

    const pieLayout = {
        title: "Mode of Payment Distribution"
    };

    Plotly.newPlot('pieChart', pieData, pieLayout, { responsive: true });
} else {
    document.getElementById("pieChart").innerHTML = "No data available";
}