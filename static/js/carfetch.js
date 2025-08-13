function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

document.getElementById("search-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const query = document.getElementById("factory_number").value;
    const container = document.getElementById("search-result");
    container.innerHTML = "";

    try {
        const res = await fetch("/api/cars/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({
                factory_number: query
            }),
        });

        if (!res.ok) {
            const errorText = await res.text();
            throw new Error(errorText);
        }

        const data = await res.json();

        if (data.length>0) {
            const container = document.getElementById('search-result');
            const notificationElement = document.createElement('div1');
            notificationElement.innerHTML = `<span style="font-size: 20px; margin-bottom: 10px; padding-bottom: 10px;">Таблица с данными</span>`;
            container.appendChild(notificationElement);
        // Рисуем таблицу
        const table = document.createElement("table");
        table.className = "responsive-table";
        table.border = "1";
        table.cellPadding = "8";

            const headers = Object.keys(data[0]);
            const thead = document.createElement("thead");
            const headerRow = document.createElement("tr");

            headers.forEach(key => {
                const th = document.createElement("th");
                th.textContent = key;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);

            const tbody = document.createElement("tbody");
            data.forEach(row => {
                const tr = document.createElement("tr");
                headers.forEach(key => {
                    const td = document.createElement("td");
                    td.textContent = row[key];
                    td.setAttribute("data-label", key);
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });
            table.appendChild(tbody);

            container.appendChild(table);
        }
        else {
                const container = document.getElementById('search-result');
                const notificationElement = document.createElement('div');
                notificationElement.innerHTML = `<span style="color: #D20A11; font-weight: bold;">Ничего не найдено ⚠</span>`;
                container.appendChild(notificationElement);
        }
    } catch (error) {
        console.error("Ошибка:", error);
        container.innerHTML = `<b>Ничего не найдено ❗</b>`;
    }
});
