const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const tableWrapper = document.querySelector(".tableWrapper");
const pagination = document.querySelector(".pagination");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    pagination.style.display = "none";
    tbody.innerHTML = "";

    fetch("/warehouse/search-products", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        tableWrapper.style.display = "none";
        tableOutput.style.display = "block";

        if (data.length === 0) {
          noResults.style.display = "block";
          tableOutput.style.display = "none";
        } else {
          noResults.style.display = "none";
          data.forEach((item) => {
            tbody.innerHTML += `
            
            <tr>
            <td>${item.id}</td>
            <td>${item.code}</td>
            <td>${item.name}</td>
            <td>${item.quantity}</td>
            <td>${item.description}</td>
            <td>${item.location_in_aislemap}</td>
            <td>${item.packaging_instruction}</td>
          </td>`;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    tableWrapper.style.display = "block";
    pagination.style.display = "block";
  }
});
