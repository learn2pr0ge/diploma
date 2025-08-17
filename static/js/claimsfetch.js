let currentSort1 = { col: -1, dir: 'asc' };

// вынеси словарь наружу, чтобы не создавать каждый клик
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

function onHeaderClickClaimsFilter(d, value, filter) {
  const token = localStorage.getItem('authToken');
  const col = Number(d.currentTarget.dataset.col);
  if (!Number.isFinite(col)) return;

  const dir = (currentSort1.col === col && currentSort1.dir === 'desc') ? 'asc' : 'desc';
  currentSort1 = { col, dir };

  const sortField = base_dict_claims[col];
  if (!sortField) return;

  fetchFilter(value, filter, token, sortField, dir);
}

function onHeaderClickClaims(c){

    const makeCarUrl = (factoryNumber) => `/memberzone/listcars/${encodeURIComponent(factoryNumber)}/`;
    const makeServiceUrl = (serviceNumber) => `/memberzone/listservice/${encodeURIComponent(serviceNumber)}/`;
    const makeClaimUrl = (claimNumber) => `/memberzone/claimpart/${encodeURIComponent(claimNumber)}/`;
    const makeClaimRecoverUrl = (claimRecoverNumber) => `/memberzone/claimrecover/${encodeURIComponent(claimRecoverNumber)}/`;
    const container = document.getElementById("search-result_memberzone");
    const token = localStorage.getItem('authToken');
    const col = +c.currentTarget.dataset.col;
    const dir = (currentSort.col === col && currentSort.dir === 'desc') ? 'asc' : 'desc';
    currentSort = { col, dir };
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

    // перерисовываем таблицу под новый запрос
    fetch("/api/cars/claimssort/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": `Token ${token}`,
        },
        body: JSON.stringify({
            sort_by: base_dict_claims[col],
            direction: dir,
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
                  btn.addEventListener("click", onHeaderClickClaims);

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

document.getElementById("claims_list").addEventListener("click", function(e) {
    e.preventDefault();

    const container = document.getElementById("search-result_memberzone");
    const cont_filter = document.getElementById("main_filter");
    const token = localStorage.getItem('authToken');
    container.innerHTML = "";
    cont_filter.innerHTML = "";
    const item = document.createElement('div');
    // Новая форма фильтров для ТО
    item.innerHTML = ` <form class="filter-form" id="filter-form" method="get" action="/search/">
  <label for="field">Искать по:</label>
  <select id="field" name="field" required>
    <option value="" disabled selected>Выберите поле</option>
      <option value="claim_car__factory_number">Зав. номер машины</option>
      <option value="claim_part__model_claimpart_name">Узел отказа</option>
      <option value="claim_recover__model_claimrecover_name">Способ восстановления</option>
      <option value="claim_service_company__model_company_name">Сервисная компания</option>
  </select>

  <label for="query" class="visually-hidden">Значение</label>
  <input id="query" name="q" type="text" placeholder="Введите значение…" required>

  <button type="submit">Поиск</button>
        <button class="filter_reset" id="filter_reset" type="reset">Сброс</button>
</form>`;
    cont_filter.appendChild(item);

    // меняем кнопку добавить рекламацию

    const add_car_btn = document.getElementById("add_car");
    if (add_car_btn) {
        add_car_btn.innerHTML = "";
        const item1 = document.createElement('div');
        item1.innerHTML = `<button id="add_claim_button" class="add_claim_button" type="submit"><a href="/memberzone/cars/createclaim/">Добавить рекламацию</a></button>`
        add_car_btn.appendChild(item1);
    }

    // обработчик фильтров

    document.getElementById("filter-form").addEventListener("submit", function(z) {
    z.preventDefault();

    const value = document.getElementById("query").value;
    const filter = document.getElementById("field").value;
    const container = document.getElementById("search-result_memberzone");
    const token = localStorage.getItem('authToken');
    container.innerHTML = "";
    fetchFilter(value, filter,token);

})

        // обработчик кнопки сброс

    document.getElementById("filter_reset").addEventListener("click", function(x) {
        x.preventDefault();
        const token = localStorage.getItem('authToken');
        resetResult(token);
    })

    const makeCarUrl = (factoryNumber) => `/memberzone/listcars/${encodeURIComponent(factoryNumber)}/`;
    const makeServiceUrl = (serviceNumber) => `/memberzone/listservice/${encodeURIComponent(serviceNumber)}/`;
    const makeClaimUrl = (claimNumber) => `/memberzone/claimpart/${encodeURIComponent(claimNumber)}/`;
    const makeClaimRecoverUrl = (claimRecoverNumber) => `/memberzone/claimrecover/${encodeURIComponent(claimRecoverNumber)}/`;

    if (!container) return;
    if (!token) {
        container.innerHTML = '<b>Нет токена авторизации</b>';
        return;
    }

    fetch("/api/cars/claims/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": `Token ${token}`,
        },
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
                  btn.addEventListener("click", onHeaderClickClaims); // <-- обработчик здесь

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

});



// функиця фетча фильтров

function fetchFilter(value, filter,token,sort='claim_date', direct='desc') {
    const container = document.getElementById("search-result_memberzone");
    const makeCarUrl = (factoryNumber) => `/memberzone/listcars/${encodeURIComponent(factoryNumber)}/`;
    const makeServiceUrl = (serviceNumber) => `/memberzone/listservice/${encodeURIComponent(serviceNumber)}/`;
    const makeClaimUrl = (claimNumber) => `/memberzone/claimpart/${encodeURIComponent(claimNumber)}/`;
    const makeClaimRecoverUrl = (claimRecoverNumber) => `/memberzone/claimrecover/${encodeURIComponent(claimRecoverNumber)}/`;

    fetch("/api/cars/filterclaims/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": `Token ${token}`,
        },
        body: JSON.stringify({
            filter: filter,
            value: value,
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
                  btn.addEventListener("click", (d) => onHeaderClickClaimsFilter(d,value, filter));

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

// функция сброса

function resetResult(token) {
    const container = document.getElementById("search-result_memberzone");
    const makeCarUrl = (factoryNumber) => `/memberzone/listcars/${encodeURIComponent(factoryNumber)}/`;
    const makeServiceUrl = (serviceNumber) => `/memberzone/listservice/${encodeURIComponent(serviceNumber)}/`;
    const makeClaimUrl = (claimNumber) => `/memberzone/claimpart/${encodeURIComponent(claimNumber)}/`;
    const makeClaimRecoverUrl = (claimRecoverNumber) => `/memberzone/claimrecover/${encodeURIComponent(claimRecoverNumber)}/`;

     fetch("cars/claims/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": `Token ${token}`,
        },
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
                  btn.addEventListener("click", onHeaderClickClaims); // <-- обработчик здесь

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