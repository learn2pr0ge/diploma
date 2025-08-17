document.getElementById("to_list").addEventListener("click", function(e) {
    e.preventDefault();

    const container = document.getElementById("search-result_memberzone");
    const cont_filter = document.getElementById("main_filter");
    const token = localStorage.getItem('authToken');
    container.innerHTML = "";
    cont_filter.innerHTML = "";
    const item = document.createElement('div');
    // Новая форма фильтров для ТО
    item.innerHTML = ` <form class="filter-form" id="filter-form1" method="get" action="/search/">
  <label for="field">Искать по:</label>
  <select id="field1" name="field" required>
    <option value="" disabled selected>Выберите поле</option>
      <option value="tm_car__factory_number">Зав. номер машины</option>
      <option value="tm_service_company__model_company_name">Сервисная компания</option>
      <option value="tm_type__model_tm_name">Тип ТО</option>
  </select>

  <label for="query" class="visually-hidden">Значение</label>
  <input id="query1" name="q" type="text" placeholder="Введите значение…" required>

  <button type="submit">Поиск</button>
        <button class="filter_reset" id="filter_reset1" type="reset">Сброс</button>
</form>`;
    cont_filter.appendChild(item);
    // Новая кнопка добавить ТО

    const add_car_btn = document.getElementById("add_car");
    if (add_car_btn) {
        add_car_btn.innerHTML = "";
        const item1 = document.createElement('div');
        item1.innerHTML = `<button id="add_to_button" class="add_to_button" type="submit"><a href="/memberzone/cars/createto/">Добавить ТО</a></button>`
        add_car_btn.appendChild(item1);
    }

    // обработчик фильтров

    document.getElementById("filter-form1").addEventListener("submit", function(z) {
    z.preventDefault();

    const value = document.getElementById("query1").value;
    const filter = document.getElementById("field1").value;
    const container = document.getElementById("search-result_memberzone");
    const token = localStorage.getItem('authToken');
    container.innerHTML = "";
    fetchFilter1(value, filter);

})

        // обработчик кнопки сброс

    document.getElementById("filter_reset1").addEventListener("click", function(x) {
        x.preventDefault();
        const token = localStorage.getItem('authToken');
        resetResult1(token);
    })

    const makeCarUrl = (factoryNumber) => `/memberzone/listcars/${encodeURIComponent(factoryNumber)}/`;
    const makeServiceUrl = (serviceNumber) => `/memberzone/listservice/${encodeURIComponent(serviceNumber)}/`;
    const makeToUrl = (toNumber) => `/memberzone/tolist/${encodeURIComponent(toNumber)}/`;

    if (!container) return;
    if (!token) {
        container.innerHTML = '<b>Нет токена авторизации</b>';
        return;
    }

    fetch("/api/cars/to/", {
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
                  btn.addEventListener("click", onHeaderClickTo);

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
                    else if (key === "Тип_ТО" && row[key]) {
                        const a = document.createElement("a");
                        a.href = makeToUrl(row[key]);
                        a.textContent = row[key];
                        a.className = "to-model-link";
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


//функция сортировки колонок таблицы
    let currentSort = {col: null, dir: 'desc'};

    function onHeaderClickTo(c) {
        const makeCarUrl = (factoryNumber) => `/memberzone/listcars/${encodeURIComponent(factoryNumber)}/`;
        const makeServiceUrl = (serviceNumber) => `/memberzone/listservice/${encodeURIComponent(serviceNumber)}/`;
        const makeToUrl = (toNumber) => `/memberzone/tolist/${encodeURIComponent(toNumber)}/`;
        const container = document.getElementById("search-result_memberzone");
        const token = localStorage.getItem('authToken');
        const col = +c.currentTarget.dataset.col;
        const dir = (currentSort.col === col && currentSort.dir === 'desc') ? 'asc' : 'desc';
        currentSort = {col, dir};
        //словарь индекс = название ячейки базы
        const base_dict_tm = {
            0: 'tm_type__model_tm_name',
            1: 'tm_date',
            2: 'tm_hours',
            3: 'tm_number',
            4: 'tm_number_date',
            5: 'tm_service_company__model_company_name',
            6: 'tm_car__factory_number',
            };

        // перерисовываем таблицу под новый запрос
    fetch("/api/cars/tosort/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": `Token ${token}`,
        },
        body: JSON.stringify({
            sort_by: base_dict_tm[col],
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
                  btn.addEventListener("click", onHeaderClickTo);

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



// функиця фетча фильтров

function fetchFilter1(value,  filter, sort='tm_date',direct='desc', d = undefined) {
    const container = document.getElementById("search-result_memberzone");
    const makeCarUrl = (factoryNumber) => `/memberzone/listcars/${encodeURIComponent(factoryNumber)}/`;
    const makeServiceUrl = (serviceNumber) => `/memberzone/listservice/${encodeURIComponent(serviceNumber)}/`;
    const makeToUrl = (toNumber) => `/memberzone/tolist/${encodeURIComponent(toNumber)}/`;
    const token = localStorage.getItem('authToken');
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
                  btn.addEventListener("click", (d) => onHeaderClickTo1(d,value, filter));

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
                    else if (key === "Тип_ТО" && row[key]) {
                        const a = document.createElement("a");
                        a.href = makeToUrl(row[key]);
                        a.textContent = row[key];
                        a.className = "to-model-link";
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

function resetResult1(token) {
    const container = document.getElementById("search-result_memberzone");
    const makeCarUrl = (factoryNumber) => `/memberzone/listcars/${encodeURIComponent(factoryNumber)}/`;
    const makeServiceUrl = (serviceNumber) => `/memberzone/listservice/${encodeURIComponent(serviceNumber)}/`;
    const makeToUrl = (toNumber) => `/memberzone/tolist/${encodeURIComponent(toNumber)}/`;

    fetch("/api/cars/to/", {
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
                  btn.addEventListener("click", onHeaderClickTo);

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


let currentSort2 = { col: null, dir: 'desc' };
function onHeaderClickTo1(d,value, filter) {

        const col = +d.currentTarget.dataset.col;
        const dir = (currentSort2.col === col && currentSort2.dir === 'desc') ? 'asc' : 'desc';
        currentSort2 = {col, dir};
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
        fetchFilter1(value, filter, sort , direct);
}