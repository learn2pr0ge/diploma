document.getElementById("claims_list").addEventListener("click", function(e) {
    e.preventDefault();
    const token = localStorage.getItem('authToken');
    const container = document.getElementById("search-result_memberzone");
    container.innerHTML = "";

    if (!container) return;
    if (!token) {
        container.innerHTML = '<b>Нет токена авторизации</b>';
        return;
    }
    fetchClaimData();

    });
    function fetchClaimData(sort='claim_date', direct='desc', d = undefined) {
    const container = document.getElementById("search-result_memberzone");
    const token = localStorage.getItem('authToken');
    const makeCarUrl = (factoryNumber) => `/memberzone/listcars/${encodeURIComponent(factoryNumber)}/`;
    const makeServiceUrl = (serviceNumber) => `/memberzone/listservice/${encodeURIComponent(serviceNumber)}/`;
    const makeClaimUrl = (claimNumber) => `/memberzone/claimpart/${encodeURIComponent(claimNumber)}/`;
    const makeClaimRecoverUrl = (claimRecoverNumber) => `/memberzone/claimrecover/${encodeURIComponent(claimRecoverNumber)}/`;
    const FACTORY_NUMBER = JSON.parse(document.getElementById('car-fn').textContent);


    fetch("/api/cars/filterclaims/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": `Token ${token}`,
        },
        body: JSON.stringify({
            filter: 'claim_car__factory_number',
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
                  btn.addEventListener("click", (y) => onHeaderClickClaimsData(y));

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
                    }
                    else if (key === "Модель_двигателя" && row[key]) {
                        const a = document.createElement("a");
                        a.href = makeEngineUrl(row[key]);
                        a.textContent = row[key];
                        a.className = "engine-model-link";
                        td.appendChild(a);
                    }
                    else if (key === "Сервисная_комп" && row[key]) {
                        const a = document.createElement("a");
                        a.href = makeServiceUrl(row[key]);
                        a.textContent = row[key];
                        a.className = "service-model-link";
                        td.appendChild(a);
                    }
                    else if (key === "Узел_отк" && row[key]) {
                        const a = document.createElement("a");
                        a.href = makeClaimUrl(row[key]);
                        a.textContent = row[key];
                        a.className = "claim-model-link";
                        td.appendChild(a);
                    }
                     else if (key === "Способ_вост" && row[key]) {
                        const a = document.createElement("a");
                        a.href = makeClaimRecoverUrl(row[key]);
                        a.textContent = row[key];
                        a.className = "claimrecover-model-link";
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
let currentSort6 = {col: null, dir: 'desc'};
function onHeaderClickClaimsData(y) {
    const col = +y.currentTarget.dataset.col;
    const dir = (currentSort6.col === col && currentSort6.dir === 'desc') ? 'asc' : 'desc';
    currentSort6 = {col, dir};
    //словарь индекс = название ячейки базы
    const base_dict_claims = {
        0: 'claim_date',
        1: 'claim_hours',
        2: 'claim_part__model_claimpart_name',
        3: 'claim_description',
        4: 'claim_recover__model_claimrecover_name',
        5: 'claim_used_parts',
        6: 'claim_finish_date',
        7: 'claim_downtime',
        8: 'claim_service_company__model_company_name',
        9: 'claim_car__factory_number',

    };
    const sort = base_dict_claims[col];
    const direct = dir;
    fetchClaimData(sort, direct);

}
