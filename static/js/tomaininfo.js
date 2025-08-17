document.getElementById("carlist_button").addEventListener("click", function(e) {
    e.preventDefault();
    const container = document.getElementById("search-result_memberzone");
    const token = localStorage.getItem('authToken');
    container.innerHTML = "";

    if (!container) return;
    if (!token) {
        container.innerHTML = '<b>Нет токена авторизации</b>';
        return;
    }
    fetchCarData();

    });


    function fetchCarData(sort='agreement_date',direct='desc', d = undefined) {
        const makeCarUrl = (factoryNumber) => `/memberzone/listcars/${encodeURIComponent(factoryNumber)}/`;
        const makeEngineUrl = (engineNumber) => `/memberzone/listengines/${encodeURIComponent(engineNumber)}/`;
        const makeModelUrl = (modelNumber) => `/memberzone/listmodels/${encodeURIComponent(modelNumber)}/`;
        const makeClutchUrl = (clutchNumber) => `/memberzone/listclutch/${encodeURIComponent(clutchNumber)}/`;
        const makeAxleUrl = (axleNumber) => `/memberzone/listaxle/${encodeURIComponent(axleNumber)}/`;
        const makeBridgeUrl = (bridgeNumber) => `/memberzone/listbridge/${encodeURIComponent(bridgeNumber)}/`;
        const makeServiceUrl = (serviceNumber) => `/memberzone/listservice/${encodeURIComponent(serviceNumber)}/`;
        const FACTORY_NUMBER = JSON.parse(document.getElementById('car-fn').textContent);
        const container = document.getElementById("search-result_memberzone");
        const token = localStorage.getItem('authToken');

    fetch("/api/cars/filter/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": `Token ${token}`,
        },
        body: JSON.stringify({
            filter: 'factory_number',
            value: FACTORY_NUMBER,
            sort_by: sort,
            direction: direct,
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
            headers.forEach((key, idx) => {
                const th = document.createElement("th");
                headerRow.appendChild(th);
                th.setAttribute("aria-sort", "none");

                  const btn = document.createElement("button");
                  btn.type = "button";
                  btn.className = "th-btn";
                  btn.dataset.col = idx;     // номер колонки
                  btn.textContent = key;     // надпись
                  btn.addEventListener("click", (z) => onHeaderClickCarList(z));

                  th.appendChild(btn);
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

}
let currentSort5 = {col: null, dir: 'desc'};
function onHeaderClickCarList(z) {
        const col = +z.currentTarget.dataset.col;
        const dir = (currentSort5.col === col && currentSort5.dir === 'desc') ? 'asc' : 'desc';
        currentSort5 = {col, dir};
        //словарь индекс = название ячейки базы
        const base_dict = {
            0: 'factory_number',
            1: 'model_technic__model_technic_name',
            2: 'model_engine__model_engine_name',
            3: 'engine_factory_number',
            4: 'model_clutch__model_clutch_name',
            5: 'clutch_factory_number',
            6: 'driven_axle_model__model_axle_name',
            7: 'driven_axle_factory_number',
            8: 'managed_bridge_model__model_bridge_name',
            9: 'managed_bridge_factory_number',
            10: 'agreement_number',
            11: 'agreement_date',
            12: 'receiver',
            13: 'receiver_address',
            14: 'configuration',
            15: 'client_name',
            16: 'service_company__model_company_name',
        };
        const sort = base_dict[col];
        const direct = dir;
        fetchCarData(sort , direct);
}