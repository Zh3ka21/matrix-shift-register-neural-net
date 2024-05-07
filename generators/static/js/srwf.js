// Функція для обробки події зміни вибору ступеня полінома
function handleDegreeChange() {
    const selectedNumber = numberSelect.value;
    if (selectedNumber) {
        fetch(`/get_polynomials_view/?degree=${selectedNumber}`)
            .then(response => response.json())
            .then(data => {
                elementSelect.innerHTML = '';
                data.forEach(polynomial => {
                    const option = document.createElement('option');
                    option.value = polynomial.id;
                    option.textContent = `${polynomial.first_number} ${polynomial.second_number} ${polynomial.letter}`;
                    elementSelect.appendChild(option);
                });
                elementSelect.disabled = false;
                // Оновлення третього селектора зі списком чисел
                const thirdSelect = document.getElementById('initialStateSelect');
                thirdSelect.innerHTML = '';
                for (let i = 1; i <= Math.pow(2, selectedNumber) - 1; i++) {
                    const option = document.createElement('option');
                    option.value = `${i}`;
                    option.textContent = i;
                    thirdSelect.appendChild(option);
                }
                console.log(thirdSelect)
                thirdSelect.disabled = false;

            })
            .catch(error => {
                console.error('Помилка при отриманні списку поліномів:', error);
            });
    } else {
        elementSelect.innerHTML = '';
        elementSelect.disabled = true;
    }
}

// Універсальна функція для побудови таблиць
function generateMatrixHTML(matrixData) {
    const table = document.createElement('table');
    table.classList.add('matrix-table');
    const tableBody = document.createElement('tbody');
    matrixData.forEach((row, rowIndex) => {
        const tableRow = document.createElement('tr');
        row.forEach((cell, cellIndex) => {
            const tableCell = document.createElement('td');
            tableCell.textContent = cell;
            tableRow.appendChild(tableCell);
        });
        const indexCell = document.createElement('td');
        indexCell.textContent = rowIndex + 1;
        tableRow.insertBefore(indexCell, tableRow.firstChild);
        tableBody.appendChild(tableRow);
    });

    table.appendChild(tableBody);
    return table;
}

//функція для додавання до контейнера
function appendListToContainer(list, container) {
    list.forEach(number => {
        const span = document.createElement('span');
        span.textContent = number + ' ';
        container.appendChild(span);
    });
}

//функція для відображення елементів з сервера
function handlePolynomialOperations() {
    // зчитування елементів
    const selectedPolynomialId = elementSelect.value;
    const selectedNumber = initialStateSelect.value;
    if (selectedPolynomialId && selectedNumber) {
        fetch(`/handle_matrix_operations_view/?polynomial_id=${selectedPolynomialId}&select=${selectedNumber}`)// передача параметрів на сервер
            .then(response => response.json())
            .then(data => {
                console.log(data);
                const matrixContainer = document.getElementById('matrix-container');
                matrixContainer.innerHTML = '';
                const resultContainer = document.getElementById('result-container');
                resultContainer.innerHTML = '';
                const sequenceContainer = document.getElementById('sequence-container');
                sequenceContainer.innerHTML = '';
                const binarySequenceContainer = document.getElementById('binary-sequence-container');
                binarySequenceContainer.innerHTML = '';
                const propertyContainer = document.getElementById('property-container');
                propertyContainer.innerHTML = '';
                const polyContainer = document.getElementById('poly-container');
                polyContainer.innerHTML = '';

                const matrixTable = generateMatrixHTML(data.result['structure_matrix']);
                matrixContainer.appendChild(matrixTable);

                const resultTable = generateMatrixHTML(data.result['state']);
                resultContainer.appendChild(resultTable);

                appendListToContainer(data.result['sequence'], sequenceContainer);
                appendListToContainer(data.result['binary_sequence'], binarySequenceContainer);

                propertyContainer.append('Вага Хемінгу ' + data.result['hg'] + '; T(очікуване) ' + data.result['T_e'] + '; T(реальне) ' + data.result['T_r']);
                polyContainer.append(data.result['poly'])
            })
            .catch(error => {
                console.error('Помилка при отриманні результатів операцій з матрицею:', error);
            });
    }
}



