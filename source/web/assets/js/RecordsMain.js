
let QueryParams = new URLSearchParams(window.location.search);

let RecordsTable;

let PageNumInput;
let PageSizeInput;
let MaxPageNum;
let TotalNumRecords;

let ViewRecordButton;
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
		ViewRecordButton = document.getElementById("ViewRecord");
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
			if (RecordsTable.classList.contains("frozen-heading"))
			{
				if (RecordsTable.getBoundingClientRect().top >= 0)
				{
					RecordsTable.classList.remove("frozen-heading");
				}
			}
			else
			{
				if (RecordsTable.getBoundingClientRect().top <= 0)
				{
					RecordsTable.classList.add("frozen-heading");
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

		ViewRecordButton.addEventListener("click", (e) =>
		{
			let selected_record = document.getElementsByClassName("visit-record selected")[0];
			let visit_id = selected_record.dataset.visitId;
			viewRecord(visit_id);
		});

		document.addEventListener("keyup", (e) =>
		{
			if (e.isComposing) return;

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

	TotalNumRecords = parseInt(RecordsTable.firstElementChild.dataset.totalRecords, 10);
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

	let visit_records = document.getElementsByClassName("visit-record");
	for (let visit_record of visit_records)
	{
		(function()
		{
			let record_div = visit_record;
			record_div.addEventListener("click", (e) =>
			{
				let add_selected = !record_div.classList.contains("selected");

				let selected_records = document.getElementsByClassName("selected");
				for (let selected_record of selected_records)
				{
					selected_record.classList.remove("selected");
				}

				if (add_selected) record_div.classList.add("selected");

				if (document.getElementsByClassName("visit-record selected").length > 0)
				{
					ViewRecordButton.disabled = false;
				}
				else
				{
					ViewRecordButton.disabled = true;
				}
			});
		}());
	}
}


function viewRecord(id)
{
	document.body.classList.add("busy");

	let req_url =
		window.location.protocol+"//"+window.location.host+"/getVisitRecord";
	let query = new URLSearchParams();
	query.set("visitId", id);
	req_url += "?" + query.toString();

	let req = new XMLHttpRequest();
	req.addEventListener("load", () =>
	{
		if (req.status === 200)
		{
			document.body.insertAdjacentHTML("beforeend", req.responseText);
			new ViewVisitRecordOverlay(document.getElementById("ViewVisitRecords"));
		}

		document.body.classList.remove("busy");
	});
	req.open("GET", req_url);
	req.setRequestHeader("Cache-Control", "no-cache");
	req.send();
}
