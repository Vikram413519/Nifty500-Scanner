function searchStock() {

    let input = document.getElementById("search").value.toUpperCase();
    let table = document.getElementById("stockTable");
    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) {

        let td = tr[i].getElementsByTagName("td")[0];

        if (td) {

            let txt = td.textContent || td.innerText;

            tr[i].style.display =
                txt.toUpperCase().indexOf(input) > -1 ? "" : "none";
        }
    }
}

function filterTable(signal) {

    let table = document.getElementById("stockTable");
    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) {

        let td = tr[i].getElementsByTagName("td")[8];

        if (td) {

            let value = td.innerText.trim();

            if (signal === "ALL") {

                tr[i].style.display = "";

            } else {

                tr[i].style.display =
                    (value === signal) ? "" : "none";
            }
        }
    }
}