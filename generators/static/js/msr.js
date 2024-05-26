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


function handlePolynomialOperations(elementSelectId1, elementSelectId2,
                                    numberSelect1, numberSelect2,
                                    iSelect, jSelect, rSelect) {
    const selectedPolynomialId1 = document.getElementById(elementSelectId1).value;
    const selectedPolynomialId2 = document.getElementById(elementSelectId2).value;
    const degree1 = document.getElementById(numberSelect1).value;
    const degree2 = document.getElementById(numberSelect2).value;
    const i = document.getElementById(iSelect).value;
    const j = document.getElementById(jSelect).value;
    const r = document.getElementById(rSelect).value;
    if (selectedPolynomialId1 && selectedPolynomialId2 && degree1 && degree2) {
        fetch(`/handle_matrix_operations_msr_view/?polynomial_idFirst=${selectedPolynomialId1}
                                                        &polynomial_idSecond=${selectedPolynomialId2}
                                                        &degreeFirst=${degree1}
                                                        &degreeSecond=${degree2}
                                                        &i=${i}
                                                        &j=${j}
                                                        &r=${r}`)
            .then(response => response.json())
            .then((data) => {
                if (data.error) {
                    console.log(data.error);
                    showError(data.error);
                    return;
                } else {
                    // Обрабатываем успешный ответ
                    console.log(data.listResult);
                    display();
                }

                const containerBody = document.querySelector('.containerBody');
                const acfData = data.listResult['acf'];
                createCharts(acfData, containerBody);
                let currentMatrixIndex = 0;
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
                    data.listResult["resultFirst"].T +
                    "; T(B) " +
                    data.listResult["resultSecond"].T;
                let str = "Вага(очікуване) " + data.listResult["hg_e"] + "; Вага(реальне) " + data.listResult["hg_r"];
                if (degree1 == degree2) {
                    str = "Вага(реальне) " + data.listResult["hg_r"];
                }

                document.getElementById("hg-container").innerText = str;
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
            .catch(error => console.error('Error:', error));
    }
}

//функція відображення другого полінома
function iventSelectSecond() {
    const elementSelect = document.getElementById("numberSelectSecond");
    const selectedDegreeFirst = parseInt(numberSelectFirst.value);

    elementSelect.innerHTML = '';
    for (let i = selectedDegreeFirst; i < 14; i++) {
        const option = document.createElement('option');
        option.value = `${i}`;
        option.textContent = i;
        elementSelect.appendChild(option);
    }
    handleDegreeChange('elementSelectSecond', 'numberSelectSecond');
}

function updateSelector(selector, maxDegree) {
    selector.innerHTML = '';
    for (let i = 0; i < maxDegree; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        selector.appendChild(option);
    }
}

function updateR(maxDegree) {
    const selector = document.getElementById("rSelect")

    selector.innerHTML = '';
    for (let i = 1; i <= maxDegree; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i;
        selector.appendChild(option);
    }
}