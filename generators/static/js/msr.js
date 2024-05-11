// Функція для обробки події зміни вибору ступеня полінома
function handleDegreeChange(selectorId, numberSelectElement) {
    const selectedNumber = document.getElementById(numberSelectElement).value;
    const selectElement = document.getElementById(selectorId);
    if (selectedNumber) {
        fetch(`/get_polynomials_view/?degree=${selectedNumber}`)
            .then((response) => response.json())
            .then((data) => {
                populateSelectOptions(data, selectorId, "id", [
                    "first_number",
                    "second_number",
                    "letter",
                ]);
            })
            .catch((error) => {
                console.error("Помилка при отриманні списку поліномів:", error);
            });
    } else {
        selectElement.innerHTML = "";
        selectElement.disabled = false;
    }
}

let currentMatrixIndex = 0;

function handlePolynomialOperations(elementSelectId1, elementSelectId2, numberSelect1, numberSelect2) {
    const selectedPolynomialId1 = document.getElementById(elementSelectId1).value;
    const selectedPolynomialId2 = document.getElementById(elementSelectId2).value;
    const degree1 = document.getElementById(numberSelect1).value;
    const degree2 = document.getElementById(numberSelect2).value;
    if (selectedPolynomialId1 && selectedPolynomialId2 && degree1 && degree2) {
        fetch(`/handle_matrix_operations_msr_view/?polynomial_idFirst=${selectedPolynomialId1}&polynomial_idSecond=${selectedPolynomialId2}&degreeFirst=${degree1}&degreeSecond=${degree2}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error vlidation');
                }
                return response.json();
            })
            .then((data) => {
                const containerBody = document.querySelector('.containerBody');
                const acfData = data.listResult['acf'];
                createCharts(acfData, containerBody);

                // Очистка контейнерів перед оновленням даних
                document.getElementById("matrix-container-first").innerHTML = "";
                document.getElementById("matrix-container-second").innerHTML = "";
                document.getElementById("property-container").innerHTML = "";
                document.getElementById("hg-container").innerHTML = "";
                document.getElementById("T-container").innerHTML = "";
                document.getElementById("sequence-container").innerHTML = "";
                document.getElementById("binary-sequence-container").innerHTML = "";
                document.getElementById("poly-container-first").innerHTML = "";
                document.getElementById("poly-container-second").innerHTML = "";
                document.getElementById("matrix-container-S").innerHTML = "";
                document.getElementById("button-container").innerHTML = "";

                // Генерування та додавання нових елементів до контейнерів
                document.getElementById("matrix-container-first").appendChild(generateMatrixHTML(data.listResult["resultFirst"].structure_matrix));
                document.getElementById("matrix-container-second").appendChild(generateMatrixHTML(data.listResult["resultSecond"].structure_matrix));

                document.getElementById("property-container").innerText = "T(A) " +
                    data.listResult["resultSecond"].T +
                    "; T(B) " +
                    data.listResult["resultSecond"].T;
                document.getElementById("hg-container").innerText = "Вага(очікуване) " +
                    data.listResult["hg_e"] +
                    "; Вага(реальне) " +
                    data.listResult["hg_r"];
                document.getElementById("T-container").innerText = "T(очікуване) " +
                    data.listResult["T_e"] +
                    "; T(реальне) " +
                    data.listResult["T_r"];

                appendListToContainer(data.listResult["sequence"], document.getElementById("sequence-container"));
                appendListToContainer(data.listResult["binary_sequence"], document.getElementById("binary-sequence-container"));

                document.getElementById("poly-container-first").innerText = data.listResult["resultFirst"].poly;
                document.getElementById("poly-container-second").innerText = data.listResult["resultSecond"].poly;

                const matrixContainerS = document.getElementById("matrix-container-S");
                matrixContainerS.innerHTML = "";
                const buttonContainerS = document.getElementById("button-container");
                buttonContainerS.innerHTML = "";
                const matrixTableS = generateMatrixHTML(data.listResult["matrixS"][currentMatrixIndex]);
                matrixContainerS.appendChild(matrixTableS);

                let nextMatrixButton = document.getElementById("nextMatrixButton");
                if (!nextMatrixButton) {
                    nextMatrixButton = document.createElement("button");
                    nextMatrixButton.id = "nextMatrixButton";
                    nextMatrixButton.classList = "btn btn-primary container-button";
                    nextMatrixButton.style = "display: block; margin: 0 auto";
                    nextMatrixButton.textContent = "Наступна матриця S";

                    nextMatrixButton.addEventListener("click", () => {
                        currentMatrixIndex = (currentMatrixIndex + 1) % data.listResult["matrixS"].length;
                        matrixContainerS.innerHTML = "";
                        const matrixTableNext = generateMatrixHTML(data.listResult["matrixS"][currentMatrixIndex]);
                        matrixContainerS.appendChild(matrixTableNext);
                    });
                    buttonContainerS.appendChild(nextMatrixButton);
                }
            })
            .catch(error => {
                alert('Помилка: ' + error.message);
            });
    }
}

//функція відображення другого полінома
function iventSelectSecond() {
    const elementSelect = document.getElementById("numberSelectSecond");
    const selectedDegreeFirst = parseInt(numberSelectFirst.value);

    elementSelect.innerHTML = '';
    for (let i = selectedDegreeFirst + 1; i < 14; i++) {
        const option = document.createElement('option');
        option.value = `${i}`;
        option.textContent = i;
        elementSelect.appendChild(option);
    }
    handleDegreeChange('elementSelectSecond', 'numberSelectSecond');
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