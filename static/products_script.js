const table = document.querySelector("#productTable");
const th = table.querySelectorAll("th");
let tbody = table.querySelector("tbody");
let rows = [...tbody.rows];

th.forEach((header) => {
  header.addEventListener("click", function () {
    let columnIndex = header.cellIndex;
    let sortDirection =
      header.getAttribute("data-sort-direction") === "asc" ? "desc" : "asc";
    header.setAttribute("data-sort-direction", sortDirection);

    rows.sort((a, b) => {
      let aValue = a.cells[columnIndex].textContent;
      let bValue = b.cells[columnIndex].textContent;

      if (sortDirection === "asc") {
        return aValue > bValue ? 1 : -1;
      } else {
        return bValue > aValue ? 1 : -1;
      }
    });

    tbody.remove();
    tbody = document.createElement("tbody");
    rows.forEach((row) => tbody.appendChild(row));
    table.appendChild(tbody);
  });
});