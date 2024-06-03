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

function createCharts(data, containerSelector, chunkSize = 50000, maxDataLength = 300) {
    console.log(data)
    containerSelector.innerHTML = '';
    const charts = [];

    // Розділити дані на частини
    for (let i = 0; i < data.length; i += chunkSize) {
        const chunkedData = data.slice(i, i + chunkSize);

        const labels = chunkedData.map((_, index) => index + i);
        const dataset = {
            label: 'Graph',
            data: chunkedData,
            borderColor: 'purple',
            fill: false,
        };

        // Створення конфігурації графіка
        const config = {
            type: 'line',
            data: {
                labels: labels,
                datasets: [dataset]
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

        // Створення та додавання графіка
        const ctx = document.createElement('canvas');
        containerSelector.appendChild(ctx);
        const myChart = new Chart(ctx, config);
        charts.push(myChart);
    }

    // Зміна ширини контейнера в разі, якщо довжина даних перевищує максимальну довжину
    if (data.length > maxDataLength) {
        const newWidth = 700 + 10000;
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