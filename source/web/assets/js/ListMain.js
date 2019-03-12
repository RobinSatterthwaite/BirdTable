
var queryParams = new URLSearchParams(window.location.search);


function main()
{
	var date_from_input = document.getElementById("DateFrom");
	var date_to_input = document.getElementById("DateTo");
	var include_feral_input = document.getElementById("IncludeFeral");

	var date_from = new Pikaday({
		field: date_from_input,
		format: "YYYY-MM-DD (ddd)"
	});
	var date_to = new Pikaday({
		field: date_to_input,
		format: "YYYY-MM-DD (ddd)"
	});

	var initial_from_date = queryParams.get("startDate");
	if (initial_from_date !== undefined)
	{
		date_from.setDate(moment(initial_from_date).toDate());
	}

	var initial_to_date = queryParams.get("endDate");
	if (initial_to_date !== undefined)
	{
		date_to.setDate(moment(initial_to_date).toDate());
	}

	if (queryParams.get("includeFeral"))
	{
		include_feral_input.checked = true;
	}

	document.getElementById("ApplyFilters").addEventListener("click", (e) =>
	{
		if (date_from_input.value !== "")
		{
			queryParams.set("startDate", date_from.getMoment().format("YYYY-MM-DD"));
		}
		else
		{
			queryParams.delete("startDate");
		}

		if (date_to_input.value !== "")
		{
			queryParams.set("endDate", date_to.getMoment().format("YYYY-MM-DD"));
		}
		else
		{
			queryParams.delete("endDate");
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
		date_from_input.value = "";
		date_to_input.value = "";
		include_feral_input.checked = false;

		queryParams = new URLSearchParams();
		updateList();
		updateQueryParams();
	});
}


function updateQueryParams()
{
	var new_url =
		window.location.protocol+"//"+window.location.host+window.location.pathname;

	var query_url = queryParams.toString();
	if (query_url.length > 0) new_url += "?" + query_url;

	if (new_url !== window.location.href)
	{
		window.history.pushState({}, "", new_url);
	}
}


function updateList()
{
	var req_url =
		window.location.protocol+"//"+window.location.host+"/getList";
	var query_url = queryParams.toString();
	if (query_url.length > 0) req_url += "?" + query_url; 

	var req = new XMLHttpRequest();
	req.addEventListener("load", () =>
	{
		if (req.status === 200)
		{
			var species_list_content = document.getElementById("SpeciesListContent");
			species_list_content.innerHTML = req.responseText;
			document.getElementById("SpeciesCount").textContent = species_list_content.childElementCount.toString()
		}
	});
	req.open("GET", req_url);
	req.setRequestHeader("Cache-Control", "no-cache")
	req.send();
}
