
let QueryParams = new URLSearchParams(window.location.search);

let DateFromInput;
let DateToInput;
let AreaInput;
let SiteInput;
let IncludeFeralInput;

let DateFrom;
let DateTo;


class SpeciesListContextMenu extends ContextMenu
{
	copyTable(e)
	{
		let table = getListAsTable();
		document.body.appendChild(table);

		let range = document.createRange();
		range.selectNodeContents(table);
	
		let selection = window.getSelection();
		selection.removeAllRanges();
		selection.addRange(range);
	
		document.execCommand("copy");

		document.body.removeChild(table);

		this.close();
	}
}


function main()
{
	DateFromInput = document.getElementById("DateFrom");
	DateToInput = document.getElementById("DateTo");
	AreaInput = document.getElementById("AreaName")
	SiteInput = document.getElementById("SiteName");
	IncludeFeralInput = document.getElementById("IncludeFeral");

	new SpeciesListContextMenu(document.getElementById("SpeciesListContextMenu"),
	                           document.getElementById("SpeciesListContent"));

	DateFrom = flatpickr(
		DateFromInput, {
			dateFormat: "Y-m-d (D)"
		});
	DateTo = flatpickr(
		DateToInput, {
			dateFormat: "Y-m-d (D)"
		});

	let initial_from_date = QueryParams.get("startDate");
	if (initial_from_date !== undefined && initial_from_date !== null)
	{
		DateFrom.setDate(moment(initial_from_date).toDate());
	}

	let initial_to_date = QueryParams.get("endDate");
	if (initial_to_date !== undefined && initial_to_date !== null)
	{
		DateTo.setDate(moment(initial_to_date).toDate());
	}

	let initial_area = QueryParams.get("areaId");
	if (initial_area !== undefined && initial_area !== null)
	{
		AreaInput.dataset.value = initial_area;
		let selected_option = document.querySelector("#AreaList option[value='"+initial_area+"']")
		if (selected_option !== null)
		{
			let label = selected_option.label;
			AreaInput.value = label;
		}
	}

	let initial_site = QueryParams.get("siteId");
	if (initial_site !== undefined && initial_site !== null)
	{
		SiteInput.dataset.value = initial_site;
		let selected_option = document.querySelector("#SiteList option[value='"+initial_site+"']")
		if (selected_option !== null)
		{
			let label = selected_option.label;
			SiteInput.value = label;
		}
	}

	if (QueryParams.get("includeFeral"))
	{
		IncludeFeralInput.checked = true;
	}

	AreaInput.addEventListener("input", (e) =>
	{
		let value = e.target.value;
		e.target.dataset.value = value;
		let selected_option = document.querySelector("#AreaList option[value='"+value+"']")
		if (selected_option !== null)
		{
			let label = selected_option.label;
			e.target.value = label;

			updateAreaSelection(value);
		}
	});

	SiteInput.addEventListener("input", (e) =>
	{
		let value = e.target.value;
		e.target.dataset.value = value;
		let selected_option = document.querySelector("#SiteList option[value='"+value+"']")
		if (selected_option !== null)
		{
			let label = selected_option.label;
			e.target.value = label;
		}
	});

	document.getElementById("ApplyFilters").addEventListener("click", applyFilters);
	document.getElementById("ClearFilters").addEventListener("click", clearFilters);
}


function applyFilters()
{
	if (DateFromInput.value !== "")
	{
		QueryParams.set("startDate", moment(DateFrom.selectedDates[0]).format("YYYY-MM-DD"));
	}
	else
	{
		QueryParams.delete("startDate");
	}

	if (DateToInput.value !== "")
	{
		QueryParams.set("endDate", moment(DateTo.selectedDates[0]).format("YYYY-MM-DD"));
	}
	else
	{
		QueryParams.delete("endDate");
	}

	if (SiteInput.dataset.value !== "" &&
	    SiteInput.dataset.value !== undefined)
	{
		QueryParams.delete("areaId");
		QueryParams.set("siteId", SiteInput.dataset.value);
	}
	else
	{
		QueryParams.delete("siteId");

		if (AreaInput.dataset.value !== "" &&
				AreaInput.dataset.value !== undefined)
		{
			QueryParams.set("areaId", AreaInput.dataset.value);
		}
		else
		{
			QueryParams.delete("areaId");
		}
	}

	if (IncludeFeralInput.checked)
	{
		QueryParams.set("includeFeral", 1);
	}
	else
	{
		QueryParams.delete("includeFeral");
	}

	updateList();
	updateQueryParams();
}


function clearFilters()
{
	DateFrom.clear();
	DateTo.clear();
	AreaInput.value = null
	AreaInput.dataset.value = "";
	SiteInput.value = null;
	SiteInput.dataset.value = "";
	IncludeFeralInput.checked = null;
	
	QueryParams = new URLSearchParams();
	updateList();
	updateQueryParams();
}


function updateQueryParams()
{
	let new_url =
		window.location.protocol+"//"+window.location.host+window.location.pathname;

	let query_url = QueryParams.toString();
	if (query_url.length > 0) new_url += "?" + query_url;

	if (new_url !== window.location.href)
	{
		window.history.pushState({}, "", new_url);
	}
}


function updateList()
{
	let species_list = document.getElementById("SpeciesList");
	species_list.classList.add("busy");

	let req_url =
		window.location.protocol+"//"+window.location.host+"/getList";
	let query_url = QueryParams.toString();
	if (query_url.length > 0) req_url += "?" + query_url; 

	let req = new XMLHttpRequest();
	req.addEventListener("load", () =>
	{
		if (req.status === 200)
		{
			let species_list_content = document.getElementById("SpeciesListContent");
			species_list_content.innerHTML = req.responseText;
			document.getElementById("SpeciesCount").textContent = species_list_content.childElementCount.toString()
		}

		species_list.classList.remove("busy");
	});
	req.open("GET", req_url);
	req.setRequestHeader("Cache-Control", "no-cache");
	req.send();
}


function updateAreaSelection(area_id)
{
	let req_url =
		window.location.protocol+"//"+window.location.host+"/getSiteOptions";
	let site_query = new URLSearchParams();
	site_query.set("areaId", area_id);
	let query_url = site_query.toString();
	if (query_url.length > 0) req_url += "?" + query_url; 

	let req = new XMLHttpRequest();
	req.addEventListener("load", () =>
	{
		if (req.status === 200)
		{
			let site_list = document.getElementById("SiteList");
			site_list.innerHTML = req.responseText;
			SiteInput.focus();
		}
	});
	req.open("GET", req_url);
	req.setRequestHeader("Cache-Control", "no-cache");
	req.send();
}


function getListAsTable()
{
	let thead = document.createElement("thead");
	let tr = document.createElement("tr")
	let th = document.createElement("th");
	th.innerHTML = "Name";
	tr.appendChild(th);
	th = document.createElement("th");
	th.innerHTML = "Binomial name";
	tr.appendChild(th);
	th = document.createElement("th");
	th.innerHTML = "Count";
	tr.appendChild(th);
	th = document.createElement("th");
	th.innerHTML = "Seen";
	tr.appendChild(th);
	th = document.createElement("th");
	th.innerHTML = "Heard";
	tr.appendChild(th);
	thead.appendChild(tr);

	let tbody = document.createElement("tbody");
	let list = document.getElementById("SpeciesListContent").children;

	for (let el of list)
	{
		let common_name = el.getElementsByClassName("species-name")[0].textContent;
		let binomial_name = el.getElementsByClassName("species-binomial-name")[0].textContent;
		let count = el.getElementsByClassName("count")[0].children[0].textContent;
		let seen = el.getElementsByClassName("species-seen")[0].textContent;
		let heard = el.getElementsByClassName("species-heard")[0].textContent;

		let tr = document.createElement("tr");
		let td = document.createElement("td");
		td.innerHTML = common_name;
		tr.appendChild(td);
		td = document.createElement("td");
		td.innerHTML = binomial_name;
		tr.appendChild(td);
		td = document.createElement("td");
		td.innerHTML = count;
		tr.appendChild(td);
		td = document.createElement("td");
		td.innerHTML = seen;
		tr.appendChild(td);
		td = document.createElement("td");
		td.innerHTML = heard;
		tr.appendChild(td);
		tbody.appendChild(tr);
	}

	let table = document.createElement("table");
	table.appendChild(thead);
	table.appendChild(tbody);

	return table;
}
