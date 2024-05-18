// Універсальна функція для побудови таблиць
function generateMatrixHTML(matrixData) {
    const table = document.createElement("table");
    table.classList.add("matrix-table");
    const tableBody = document.createElement("tbody");
    matrixData.forEach((row, rowIndex) => {
        const tableRow = document.createElement("tr");
        row.forEach((cell, cellIndex) => {
            const tableCell = document.createElement("td");
            tableCell.textContent = cell;
            tableRow.appendChild(tableCell);
        });
        const indexCell = document.createElement("td");
        indexCell.textContent = rowIndex + 1;
        tableRow.insertBefore(indexCell, tableRow.firstChild);
        tableBody.appendChild(tableRow);
    });

    table.appendChild(tableBody);
    return table;
}

//функція для додавання до контейнера
function appendListToContainer(list, container) {
    list.forEach((number) => {
        const span = document.createElement("span");
        span.textContent = number + " ";
        container.appendChild(span);
    });
}

// Функція для заповнення варіантів в селекторі
function populateSelectOptions(data, elementId, valueProperty, textProperties) {
    const elementSelect = document.getElementById(elementId);
    elementSelect.innerHTML = "";
    data.forEach((item) => {
        const option = document.createElement("option");
        option.value = item[valueProperty];
        option.textContent = textProperties.map((prop) => item[prop]).join(" ");
        elementSelect.appendChild(option);
    });
    elementSelect.disabled = false;
}

function createCharts(data, containerSelector, chunkSize = 2000, maxDataLength = 300) {
    containerSelector.innerHTML = '';
    const chunkedData = [];
    for (let i = 0; i < data.length; i += chunkSize) {
        chunkedData.push(data.slice(i, i + chunkSize));
    }
    let indexOffs = 0;

    const charts = [];
    for (let i = 0; i < chunkedData.length; i++) {

        const config = {
            type: 'line',
            data: {
                labels: chunkedData[i].map((_, index) => index + 1 + indexOffs),
                datasets: [{
                    label: 'Percentage (%)',
                    data: chunkedData[i],
                    borderColor: 'green',
                    fill: false,
                }]
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        };
        indexOffs += chunkSize;
        const ctx = document.createElement('canvas');
        containerSelector.appendChild(ctx);
        const myChart = new Chart(ctx, config);
        charts.push(myChart);
    }

    if (data.length > maxDataLength) {
        const newWidth = 700 + 20000;
        containerSelector.style.width = `${newWidth}px`;
    }

    return charts;
}

//функція відображення кожного елементу на сторінці
function display(outputContainers) {

    const headings = document.querySelectorAll('[id^="toggleVisible"]');
    const containers = document.querySelectorAll(".container");
    const columns6 = document.querySelectorAll(".col-md-6");
    const columns4 = document.querySelectorAll(".col-md-4");
    // Display all elements when the button is clicked
    outputContainers.forEach((container) => {
        container.style.display = "block";
    });
    headings.forEach((heading) => {
        heading.style.display = "block";
    });

    containers.forEach((container) => {
        container.style.display = "block";
    });

    outputContainers.forEach((oc) => {
        oc.style.display = "block";
    });

    columns6.forEach((cols) => {
        cols.style.display = "block";
    });

    columns4.forEach((cols) => {
        cols.style.display = "block";
    });
}

//функція відображення
function visualization() {
    const button = document.getElementById("buildMatrixButton");
    const outputContainers = document.querySelectorAll(".output-container");
    button.addEventListener("click", function () {
        outputContainers.forEach((container) => {
            container.style.display = "block";
        });
    });

    button.addEventListener("click", () => display(outputContainers));
}