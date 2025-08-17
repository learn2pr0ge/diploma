document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('search-result_memberzone');
    container.innerHTML = "";
    const token = localStorage.getItem('authToken');
    const FACTORY_NUMBER = JSON.parse(document.getElementById('car-fn').textContent);
    const makeCarUrl = (factoryNumber) => `/memberzone/listcars/${encodeURIComponent(factoryNumber)}/`;
    const makeServiceUrl = (serviceNumber) => `/memberzone/listservice/${encodeURIComponent(serviceNumber)}/`;
    const makeToUrl = (toNumber) => `/memberzone/tolist/${encodeURIComponent(toNumber)}/`;

    if (!container) return;
    if (!token) {
        container.innerHTML = '<b>Нет токена авторизации</b>';
        return;
    }
    getTO(token, FACTORY_NUMBER, makeCarUrl, makeServiceUrl, makeToUrl);
    document.getElementById("to_list").addEventListener("click", function (e) {
        e.preventDefault();
        getTO(token, FACTORY_NUMBER, makeCarUrl, makeServiceUrl, makeToUrl);


    })

});

    function getTO(token, FACTORY_NUMBER, makeCarUrl, makeServiceUrl, makeToUrl, sort = 'tm_date', direct = 'desc') {
        const container = document.getElementById('search-result_memberzone');
        fetch("/api/cars/filterto/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": `Token ${token}`,
            },
            body: JSON.stringify({
                filter: 'tm_car__factory_number',
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
                    btn.addEventListener("click", (d) => onHeaderClickTOList(d));

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

                        if (key === "Авто" && row[key]) {
                            const a = document.createElement("a");
                            a.href = makeCarUrl(row[key]);
                            a.textContent = row[key];
                            a.className = "car-link";
                            td.appendChild(a);
                        } else if (key === "Модель_двигателя" && row[key]) {
                            const a = document.createElement("a");
                            a.href = makeEngineUrl(row[key]);
                            a.textContent = row[key];
                            a.className = "engine-model-link";
                            td.appendChild(a);
                        } else if (key === "Сервисная_комп" && row[key]) {
                            const a = document.createElement("a");
                            a.href = makeServiceUrl(row[key]);
                            a.textContent = row[key];
                            a.className = "service-model-link";
                            td.appendChild(a);
                        } else if (key === "Тип_ТО" && row[key]) {
                            const a = document.createElement("a");
                            a.href = makeToUrl(row[key]);
                            a.textContent = row[key];
                            a.className = "to-model-link";
                            td.appendChild(a);
                        } else {
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

    let currentSort3 = {col: null, dir: 'desc'};

    function onHeaderClickTOList(d) {

        const col = +d.currentTarget.dataset.col;
        const dir = (currentSort3.col === col && currentSort3.dir === 'desc') ? 'asc' : 'desc';
        currentSort3 = {col, dir};
        //словарь индекс = название ячейки базы
        const base_dict1 = {
            0: 'tm_type__model_tm_name',
            1: 'tm_date',
            2: 'tm_hours',
            3: 'tm_number',
            4: 'tm_number_date',
            5: 'tm_service_company__model_company_name',
            6: 'tm_car__factory_number',
        };
        const sort = base_dict1[col];
        const direct = dir;
        const token = localStorage.getItem('authToken');
        const FACTORY_NUMBER = JSON.parse(document.getElementById('car-fn').textContent);
        const makeCarUrl = (factoryNumber) => `/memberzone/listcars/${encodeURIComponent(factoryNumber)}/`;
        const makeServiceUrl = (serviceNumber) => `/memberzone/listservice/${encodeURIComponent(serviceNumber)}/`;
        const makeToUrl = (toNumber) => `/memberzone/tolist/${encodeURIComponent(toNumber)}/`;
        getTO(token, FACTORY_NUMBER, makeCarUrl, makeServiceUrl, makeToUrl,sort,direct);
    }


// используем
