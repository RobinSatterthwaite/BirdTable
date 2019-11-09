
let QueryParams = new URLSearchParams(window.location.search);

let RecordsTable;

let PageNumInput;
let PageSizeInput;
let MaxPageNum;
let TotalNumRecords;

let FirstPageButton;
let PreviousPageButton;
let NextPageButton;
let LastPageButton;


function main()
{
	try
	{
		RecordsTable = document.getElementById("RecordsTable");
		PageNumInput = document.getElementById("PageNum");
		PageSizeInput = document.getElementById("PageSize");
		FirstPageButton = document.getElementById("FirstPage");
		PreviousPageButton = document.getElementById("PreviousPage");
		NextPageButton = document.getElementById("NextPage");
		LastPageButton = document.getElementById("LastPage");
		
		let new_visit_dialog = new NewVisitDialog(document.getElementById("NewVisitDialog"));
	
		document.getElementById("NewVisit").addEventListener("click", (e) =>
		{
			new_visit_dialog.show();
		});

		// transition between fixed and moving table header row
		document.getElementById("RecordsContainer").addEventListener("scroll", (e) =>
		{
			if (RecordsTable.children[0].classList.contains("frozen"))
			{
				if (RecordsTable.getBoundingClientRect().top >= 0)
				{
					RecordsTable.children[0].classList.remove("frozen");
					RecordsTable.children[1].style.display = "none";
				}
			}
			else
			{
				if (RecordsTable.getBoundingClientRect().top <= 0)
				{
					RecordsTable.children[0].classList.add("frozen");
					RecordsTable.children[1].style.display = "initial";
				}
			}
		});

		PageNumInput.addEventListener("change", (e) =>
		{
			updatePageOptions();
		});

		FirstPageButton.addEventListener("click", (e) =>
		{
			PageNumInput.value = 1;
			updatePageOptions();
		});

		PreviousPageButton.addEventListener("click", (e) =>
		{
			PageNumInput.value--;
			updatePageOptions();
		});

		NextPageButton.addEventListener("click", (e) =>
		{
			PageNumInput.value++;
			updatePageOptions();
		});

		LastPageButton.addEventListener("click", (e) =>
		{
			PageNumInput.value = MaxPageNum;
			updatePageOptions();
		});

		document.addEventListener("keyup", (e) =>
		{
			if (e.isComposing || e.keyCode === 229) return;

			switch (e.key)
			{
			case "ArrowLeft":
				if (e.ctrlKey) FirstPageButton.click();
				else           PreviousPageButton.click();
				break;
			case "ArrowRight":
				if (e.ctrlKey) LastPageButton.click();
				else           NextPageButton.click();
				break;
			default:
				break;
			}
		});

		// initial population of table
		updatePageOptions();
	}
	catch(e)
	{
		window.alert("A problem occured loading this page.");
		throw(e);
	}
}


function updatePageOptions()
{
	let page_num_value = parseInt(PageNumInput.value, 10);
	let page_size_value = parseInt(PageSizeInput.value, 10);

	if (!isNaN(page_num_value)  &&
	    !isNaN(page_size_value) &&
	    page_num_value < MaxPageNum)
	{
		let start_index = (MaxPageNum-page_num_value) * page_size_value;
		QueryParams.set("startIndex", start_index);
	}
	else
	{
		QueryParams.delete("startIndex");
	}

	let previous_page_size_value = QueryParams.get("numResults");
	if (!isNaN(page_size_value))
	{
		QueryParams.set("numResults", page_size_value);
	}
	else
	{
		QueryParams.delete("numResults");
	}

	updateTable();
}


function updateTable()
{
	RecordsTable.classList.add("busy");

	let req_url =
		window.location.protocol+"//"+window.location.host+"/getRecords";
	let query_url = QueryParams.toString();
	if (query_url.length > 0) req_url += "?" + query_url; 

	let req = new XMLHttpRequest();
	req.addEventListener("load", () =>
	{
		if (req.status === 200)
		{
			RecordsTable.innerHTML = req.responseText;
			processUpdatedTable();
		}

		RecordsTable.classList.remove("busy");
	});
	req.open("GET", req_url);
	req.setRequestHeader("Cache-Control", "no-cache");
	req.send();
}


function processUpdatedTable()
{
	let date_headers = document.getElementsByClassName("visit-date");
	for (let date_el of date_headers)
	{
		let date_string = moment(date_el.innerText).format("YYYY-MM-DD");
		date_el.innerText = date_string;
		date_el.style.display = "initial";
	}

	regenerateOddRows();

	TotalNumRecords = parseInt(document.getElementById("TotalNumRecords").textContent, 10);
	let page_size_value = parseInt(PageSizeInput.value, 10);

	let start_index = QueryParams.get("startIndex");
	if (start_index === null) start_index = 0;

	MaxPageNum = Math.ceil(TotalNumRecords/page_size_value);
	document.getElementById("MaxPageNum").textContent = MaxPageNum;
	PageNumInput.value = MaxPageNum-Math.ceil(start_index/page_size_value);

	if (start_index >= TotalNumRecords-page_size_value)
	{
		FirstPageButton.disabled = true;
		PreviousPageButton.disabled = true;
	}
	else
	{
		FirstPageButton.disabled = false;
		PreviousPageButton.disabled = false;
	}

	if (start_index <= 0)
	{
		NextPageButton.disabled = true;
		LastPageButton.disabled = true;
	}
	else
	{
		NextPageButton.disabled = false;
		LastPageButton.disabled = false;
	}

	document.getElementById("ToggleFilters").addEventListener(
		"dblclick", toggleFilters);

	let headings = RecordsTable.getElementsByClassName("visit-heading");
	let counter = 1;
	for (let heading of headings)
	{
		(function()
		{
			let column_num = counter;
			heading.addEventListener("dblclick", (e) =>
			{
				filterRowsForContentsOfColumn(column_num);
			});
		}());
		counter++;
	}

	let selected_species_id = QueryParams.get("speciesId");

	let species_names = RecordsTable.getElementsByClassName("species-name");
	for (let name of species_names)
	{
		name.addEventListener("dblclick", (e) =>
		{
			let species_id = e.target.dataset.id;
			let current_species_id = QueryParams.get("speciesId");
			if (current_species_id !== null &&
			    current_species_id === species_id)
			{
				QueryParams.delete("speciesId");
			}
			else
			{
				QueryParams.set("speciesId", species_id);
			}

			updateTable();
		});

		if (selected_species_id !== null &&
		    selected_species_id === name.dataset.id)
		{
			name.parentElement.classList.add("selected");
		}
	}
}


function toggleFilters()
{
	let filters_set = false;

	let filtered_rows = RecordsTable.getElementsByClassName("filtered");
	if (filtered_rows.length > 0)
	{
		filters_set = true;
		while (filtered_rows.length > 0)
		{
			filtered_rows[0].classList.remove("filtered");
		}

		RecordsTable.className = "";
	}

	if (QueryParams.get("speciesId") !== null)
	{
		filters_set = true;
		QueryParams.delete("speciesId");
		updateTable();
	}
	
	if (!filters_set)
	{
		let rows = RecordsTable.getElementsByClassName("species-records");	
		for (let row of rows)
		{
			let row_is_empty = true;
			
			let row_children = Array.prototype.slice.call(row.children, 1);
			for (let child of row_children)
			{
				if (child.textContent.trim() !== "")
				{
					row_is_empty = false;
					break;
				}
			}

			if (row_is_empty) row.classList.add("filtered");
		}
	}

	regenerateOddRows();
}


function filterRowsForContentsOfColumn(column_num)
{
	let rows = RecordsTable.getElementsByClassName("species-records");
	for (let row of rows)
	{
		if (row.children[column_num].textContent.trim() === "")
		{
			row.classList.add("filtered");
		}
		else
		{
			row.classList.remove("filtered");
		}
	}

	RecordsTable.className = `select-column-${column_num}`;

	regenerateOddRows();
}


function regenerateOddRows()
{
	let rows = RecordsTable.getElementsByClassName("species-records");
	let counter = 1;
	let last_visible_row;
	for (let row of rows)
	{
		if (row.classList.contains("filtered")) continue;

		if (counter%2 === 0) row.classList.remove("odd");
		else                 row.classList.add("odd");
		counter++;

		row.classList.remove("last-visible");
		last_visible_row = row;
	}

	if (last_visible_row !== undefined)
	{
		last_visible_row.classList.add("last-visible");
	}
}
