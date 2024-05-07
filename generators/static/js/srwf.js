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

function handlePolynomialOperations() {
    const selectedPolynomialId = elementSelect.value;
    if (selectedPolynomialId) {
        fetch(`/handle_matrix_operations/?polynomial_id=${selectedPolynomialId}`)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                const matrixContainer = document.getElementById('matrix-container');
                matrixContainer.innerHTML = '';
                const resultContainer = document.getElementById('result-container');
                resultContainer.innerHTML = '';
                const sequenceContainer = document.getElementById('sequence-container');
                sequenceContainer.innerHTML = ''; // Очищаємо контейнер для послідовності

                const matrixTable = generateMatrixHTML(data.matrix);
                matrixContainer.appendChild(matrixTable);

                const resultTable = generateMatrixHTML(data.result_array);
                resultContainer.appendChild(resultTable);


                data.sequence.forEach(number => {
                    const span = document.createElement('span');
                    span.textContent = number + ' '; // Додаємо пробіл після кожного числа
                    sequenceContainer.appendChild(span);
                });
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