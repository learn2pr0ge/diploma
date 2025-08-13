document.getElementById("filter-form").addEventListener("submit", function(e) {
    e.preventDefault();

    const value = document.getElementById("query").value;
    const filter = document.getElementById("field").value;
    const container = document.getElementById("search-result_memberzone");
    const token = localStorage.getItem('authToken');
    container.innerHTML = "";

    if (!container) return;
    if (!token) {
        container.innerHTML = '<b>Нет токена авторизации</b>';
        return;
    }

    const makeCarUrl = (factoryNumber) => `/memberzone/listcars/${encodeURIComponent(factoryNumber)}/`;
    const makeEngineUrl = (engineNumber) => `/memberzone/listengines/${encodeURIComponent(engineNumber)}/`;
    const makeModelUrl = (modelNumber) => `/memberzone/listmodels/${encodeURIComponent(modelNumber)}/`;
    const makeClutchUrl = (clutchNumber) => `/memberzone/listclutch/${encodeURIComponent(clutchNumber)}/`;
    const makeAxleUrl = (axleNumber) => `/memberzone/listaxle/${encodeURIComponent(axleNumber)}/`;
    const makeBridgeUrl = (bridgeNumber) => `/memberzone/listbridge/${encodeURIComponent(bridgeNumber)}/`;
    const makeServiceUrl = (serviceNumber) => `/memberzone/listservice/${encodeURIComponent(serviceNumber)}/`;

    fetch("/api/cars/filterto/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": `Token ${token}`,
        },
        body: JSON.stringify({
            filter: filter,
            value: value,
        }),
    })
        .then(async res => {
            if (!res.ok) {
                const txt = await res.text();
                throw new Error(txt || `HTTP ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            if (!Array.isArray(data) || data.length === 0) {
                container.innerHTML = "<b>Ничего не найдено</b>";
                return;
            }

            const table = document.createElement("table");
            table.className = "responsive-table";
            table.border = "1";
            table.cellPadding = "8";

            // Заголовки из первого объекта
            const headers = Object.keys(data[0]);

            // thead
            const thead = document.createElement("thead");
            const headerRow = document.createElement("tr");
            headers.forEach(key => {
                const th = document.createElement("th");
                th.textContent = key;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);

            // tbody
            const tbody = document.createElement("tbody");

            data.forEach(row => {
                const tr = document.createElement("tr");

                headers.forEach(key => {
                    const td = document.createElement("td");
                    td.setAttribute("data-label", key); // для мобильной вёрстки

                    if (key === "Зав_номер" && row[key]) {
                        const a = document.createElement("a");
                        a.href = makeCarUrl(row[key]);
                        a.textContent = row[key];
                        a.className = "car-link";
                        td.appendChild(a);
                    }
                    else if (key === "Модель_двигателя" && row[key]) {
                        const a = document.createElement("a");
                        a.href = makeEngineUrl(row[key]);
                        a.textContent = row[key];
                        a.className = "engine-model-link";
                        td.appendChild(a);
                    }
                    else if (key === "Модель_техники" && row[key]) {
                        const a = document.createElement("a");
                        a.href = makeModelUrl(row[key]);
                        a.textContent = row[key];
                        a.className = "technic-model-link";
                        td.appendChild(a);
                    }
                    else if (key === "Модель_транс" && row[key]) {
                        const a = document.createElement("a");
                        a.href = makeClutchUrl(row[key]);
                        a.textContent = row[key];
                        a.className = "model-link";
                        td.appendChild(a);
                    }
                    else if (key === "Ведущий_мост" && row[key]) {
                        const a = document.createElement("a");
                        a.href = makeAxleUrl(row[key]);
                        a.textContent = row[key];
                        a.className = "axle-model-link";
                        td.appendChild(a);
                    }
                    else if (key === "Управляемый_мост" && row[key]) {
                        const a = document.createElement("a");
                        a.href = makeBridgeUrl(row[key]);
                        a.textContent = row[key];
                        a.className = "bridge-model-link";
                        td.appendChild(a);
                    }
                    else if (key === "Серв_компания" && row[key]) {
                        const a = document.createElement("a");
                        a.href = makeServiceUrl(row[key]);
                        a.textContent = row[key];
                        a.className = "service-model-link";
                        td.appendChild(a);
                    }

                    else {
                        td.textContent = (row[key] ?? "");
                    }

                    tr.appendChild(td);
                });

                tbody.appendChild(tr);
            });

            table.appendChild(tbody);
            container.innerHTML = "";
            container.appendChild(table);
        })
        .catch(err => {
            console.error(err);
            container.innerHTML = `<b>Ошибка: ${err.message}</b>`;
        });
});


