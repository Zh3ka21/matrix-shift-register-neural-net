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
function display() {
    const containers = document.querySelectorAll(".container");
    containers.forEach((container) => {
        container.style.display = "block";
    });
}

function visualization() {
    const button = document.getElementById("buildMatrixButton");
    button.addEventListener("click", () => display());
}

function showError(errorMessage) {
// Проверяем, если сообщение об ошибке является массивом
    if (Array.isArray(errorMessage)) {
        errorMessage = errorMessage.join(''); // Соединяем элементы массива в одну строку
    }

    // Убираем квадратные скобки, если они есть
    if (errorMessage.startsWith('[') && errorMessage.endsWith(']')) {
        errorMessage = errorMessage.substring(1, errorMessage.length - 1);
    }

    let errorModal = document.getElementById('errorModal');
    let errorText = document.getElementById('errorText');
    errorText.innerText = errorMessage;
    errorModal.style.display = 'flex';
}

function closeErrorModal() {
    let errorModal = document.getElementById('errorModal');
    errorModal.style.display = 'none';
}