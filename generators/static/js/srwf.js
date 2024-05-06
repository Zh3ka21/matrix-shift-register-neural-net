// Функція для обробки події зміни вибору ступеня полінома
function handleDegreeChange() {
    const selectedNumber = numberSelect.value;
    if (selectedNumber) {
        fetch(`/get_polynomials/?degree=${selectedNumber}`)
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
            })
            .catch(error => {
                console.error('Помилка при отриманні списку поліномів:', error);
            });
    } else {
        elementSelect.innerHTML = '';
        elementSelect.disabled = true;
    }
}
function handlePolynomialOperations() {
    const selectedPolynomialId = elementSelect.value;
    if (selectedPolynomialId) {
        fetch(`/handle_matrix_operations/?polynomial_id=${selectedPolynomialId}`)
            .then(response => response.json())
            .then(data => {
                console.log(data)
                const matrixContainer = document.getElementById('matrix-container');
                matrixContainer.innerHTML = '';

                const matrixTable = document.createElement('table');
                matrixTable.classList.add('matrix-table');
                const tableBody = document.createElement('tbody');
                data.matrix.forEach((row, rowIndex) => {
                    const matrixRow = document.createElement('tr');
                    row.forEach((cell, cellIndex) => {
                        const matrixCell = document.createElement('td');
                        matrixCell.textContent = cell;
                        matrixRow.appendChild(matrixCell);
                    });
                    const indexCell = document.createElement('td');
                    indexCell.textContent = rowIndex + 1;
                    matrixRow.insertBefore(indexCell, matrixRow.firstChild);
                    tableBody.appendChild(matrixRow);
                });
                matrixTable.appendChild(tableBody);
                matrixContainer.appendChild(matrixTable);

                const resultContainer = document.getElementById('result-container');
                resultContainer.innerHTML = '';

                const resultTable = document.createElement('table');
                resultTable.classList.add('matrix-table');
                const resultTableBody = document.createElement('tbody');
                data.result_array.forEach((row, rowIndex) => {
                    const resultRow = document.createElement('tr');
                    row.forEach((cell, cellIndex) => {
                        const resultCell = document.createElement('td');
                        resultCell.textContent = cell;
                        resultRow.appendChild(resultCell);
                    });
                    const indexCell = document.createElement('td');
                    indexCell.textContent = rowIndex + 1;
                    resultRow.insertBefore(indexCell, resultRow.firstChild);
                    resultTableBody.appendChild(resultRow);
                });
                resultTable.appendChild(resultTableBody);
                resultContainer.appendChild(resultTable);

            })
            .catch(error => {
                console.error('Помилка при отриманні результатів операцій з матрицею:', error);
            });
    }
}

const buildMatrixButton = document.getElementById('buildMatrixButton');
buildMatrixButton.addEventListener('click', handlePolynomialOperations);

const numberSelect = document.getElementById('numberSelect');
const elementSelect = document.getElementById('elementSelect');
numberSelect.addEventListener('change', handleDegreeChange);