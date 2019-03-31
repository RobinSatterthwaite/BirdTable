
let queryParams = new URLSearchParams(window.location.search);


function main()
{
	let date_from_input = document.getElementById("DateFrom");
	let date_to_input = document.getElementById("DateTo");
	let site_input = document.getElementById("SiteName");
	let include_feral_input = document.getElementById("IncludeFeral");

	let date_from = flatpickr(
		date_from_input,
		{
			dateFormat: "Y-m-d (D)"
		});
	let date_to = flatpickr(
		date_to_input,
		{
			dateFormat: "Y-m-d (D)"
		});

	let initial_from_date = queryParams.get("startDate");
	if (initial_from_date !== undefined && initial_from_date !== null)
	{
		date_from.setDate(moment(initial_from_date).toDate());
	}

	let initial_to_date = queryParams.get("endDate");
	if (initial_to_date !== undefined && initial_to_date !== null)
	{
		date_to.setDate(moment(initial_to_date).toDate());
	}

	let initial_site = queryParams.get("siteId");
	if (initial_site !== undefined && initial_site !== null)
	{
		site_input.dataset.value = initial_site;
		let selected_option = document.querySelector("#SiteList option[value='"+initial_site+"']")
		if (selected_option !== null)
		{
			let label = selected_option.label;
			site_input.value = label;
		}
	}

	if (queryParams.get("includeFeral"))
	{
		include_feral_input.checked = true;
	}

	site_input.addEventListener("input", (e) =>
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

	document.getElementById("ApplyFilters").addEventListener("click", (e) =>
	{
		if (date_from_input.value !== "")
		{
			queryParams.set("startDate", moment(date_from.selectedDates[0]).format("YYYY-MM-DD"));
		}
		else
		{
			queryParams.delete("startDate");
		}

		if (date_to_input.value !== "")
		{
			queryParams.set("endDate", moment(date_to.selectedDates[0]).format("YYYY-MM-DD"));
		}
		else
		{
			queryParams.delete("endDate");
		}

		if (site_input.dataset.value !== "")
		{
			queryParams.set("siteId", site_input.dataset.value);
		}
		else
		{
			queryParams.delete("siteId");
		}

		if (include_feral_input.checked)
		{
			queryParams.set("includeFeral", 1);
		}
		else
		{
			queryParams.delete("includeFeral");
		}

		updateList();
		updateQueryParams();
	});

	document.getElementById("ClearFilters").addEventListener("click", (e) =>
	{
		date_from.clear();
		date_to.clear();
		site_input.value = null;
		include_feral_input.checked = null;

		queryParams = new URLSearchParams();
		updateList();
		updateQueryParams();
	});
}


function updateQueryParams()
{
	let new_url =
		window.location.protocol+"//"+window.location.host+window.location.pathname;

	let query_url = queryParams.toString();
	if (query_url.length > 0) new_url += "?" + query_url;

	if (new_url !== window.location.href)
	{
		window.history.pushState({}, "", new_url);
	}
}


function updateList()
{
	let req_url =
		window.location.protocol+"//"+window.location.host+"/getList";
	let query_url = queryParams.toString();
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
	});
	req.open("GET", req_url);
	req.setRequestHeader("Cache-Control", "no-cache");
	req.send();
}
