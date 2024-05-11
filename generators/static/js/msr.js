// Функція для обробки події зміни вибору ступеня полінома
function handleDegreeChange(selectorId, selectElement, numberSelectElement) {
  const selectedNumber = numberSelectElement.value;
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
    selectElement.disabled = true;
  }
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

let currentMatrixIndex = 0; // зберігаємо поточний індекс матриці
//функція для відображення елементів з сервера
function handlePolynomialOperations(elementSelectId1, elementSelectId2) {
  const selectedPolynomialId1 = document.getElementById(elementSelectId1).value;
  const selectedPolynomialId2 = document.getElementById(elementSelectId2).value;
  if (selectedPolynomialId1 && selectedPolynomialId2) {
    fetch(
      `/handle_matrix_operations_msr_view/?polynomial_idFirst=${selectedPolynomialId1}&polynomial_idSecond=${selectedPolynomialId2}`
    ) // передача параметрів на сервер
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        const matrixContainerFirst = document.getElementById(
          "matrix-container-first"
        );
        matrixContainerFirst.innerHTML = "";
        const matrixContainerSecond = document.getElementById(
          "matrix-container-second"
        );
        matrixContainerSecond.innerHTML = "";

        const TabContainer = document.getElementById("property-container");
        TabContainer.innerHTML = "";
        const HgContainer = document.getElementById("hg-container");
        HgContainer.innerHTML = "";
        const TContainer = document.getElementById("T-container");
        TContainer.innerHTML = "";

        const sequenceContainer = document.getElementById("sequence-container");
        sequenceContainer.innerHTML = "";
        const binarySequenceContainer = document.getElementById(
          "binary-sequence-container"
        );
        binarySequenceContainer.innerHTML = "";

        const polyContainerFirst = document.getElementById(
          "poly-container-first"
        );
        polyContainerFirst.innerHTML = "";
        const polyContainerSecond = document.getElementById(
          "poly-container-second"
        );
        polyContainerSecond.innerHTML = "";

        const matrixTableFirst = generateMatrixHTML(
          data.listResult["resultFirst"].structure_matrix
        );
        matrixContainerFirst.appendChild(matrixTableFirst);
        const matrixTableSecond = generateMatrixHTML(
          data.listResult["resultSecond"].structure_matrix
        );
        matrixContainerSecond.appendChild(matrixTableSecond);

        TabContainer.append(
          "T(A) " +
            data.listResult["resultSecond"].T +
            "; T(B) " +
            data.listResult["resultSecond"].T
        );
        HgContainer.append(
          "Вага(очікуване) " +
            data.listResult["hg_e"] +
            "; Вага(реальне) " +
            data.listResult["hg_r"]
        );
        TContainer.append(
          "T(очікуване) " +
            data.listResult["T_e"] +
            "; T(реальне) " +
            data.listResult["T_r"]
        );

        appendListToContainer(data.listResult["sequence"], sequenceContainer);
        appendListToContainer(
          data.listResult["binary_sequence"],
          binarySequenceContainer
        );

        polyContainerFirst.append(data.listResult["resultFirst"].poly);
        polyContainerSecond.append(data.listResult["resultSecond"].poly);

        const matrixContainerS = document.getElementById("matrix-container-S");
        matrixContainerS.innerHTML = "";
        const buttonContainerS = document.getElementById("button-container");
        buttonContainerS.innerHTML = "";
        const matrixTableS = generateMatrixHTML(
          data.listResult["matrixS"][currentMatrixIndex]
        );
        matrixContainerS.appendChild(matrixTableS);

        // Додавання кнопки для відображення наступної матриці S
        let nextMatrixButton = document.getElementById("nextMatrixButton");
        if (!nextMatrixButton) {
          // додавання кнопки лише якщо вона ще не існує
          nextMatrixButton = document.createElement("button");
          nextMatrixButton.id = "nextMatrixButton";
          nextMatrixButton.classList = "btn btn-primary container-button";
          nextMatrixButton.style = "display: block; margin: 0 auto";
          nextMatrixButton.textContent = "Наступна матриця S";

          nextMatrixButton.addEventListener("click", () => {
            currentMatrixIndex =
              (currentMatrixIndex + 1) % data.listResult["matrixS"].length; // збільшуємо індекс, перевіряємо, чи не перевищили довжину масиву
            matrixContainerS.innerHTML = "";
            const matrixTableNext = generateMatrixHTML(
              data.listResult["matrixS"][currentMatrixIndex]
            );
            matrixContainerS.appendChild(matrixTableNext);
          });
          buttonContainerS.appendChild(nextMatrixButton);
        }
      })
      .catch((error) => {
        console.error(
          "Помилка при отриманні результатів операцій з матрицею:",
          error
        );
      });
  }
}
