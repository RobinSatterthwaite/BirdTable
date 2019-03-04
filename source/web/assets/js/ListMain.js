
var queryParams = {};


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

	document.getElementById("ApplyFilters").addEventListener("click", (e) =>
	{
		if (date_from_input.value !== "")
		{
			queryParams.startDate = date_from.getMoment().format("YYYY-MM-DD");
		}
		else
		{
			delete queryParams.startDate;
		}

		if (date_to_input.value !== "")
		{
			queryParams.endDate = date_to.getMoment().format("YYYY-MM-DD");
		}
		else
		{
			delete queryParams.endDate;
		}

		if (include_feral_input.checked)
		{
			queryParams.includeFeral = "1";
		}
		else
		{
			delete queryParams.includeFeral;
		}

		updateQueryParams();
	});

	document.getElementById("ClearFilters").addEventListener("click", (e) =>
	{
		date_from_input.value = "";
		date_to_input.value = "";
		include_feral_input.checked = false;

		queryParams = {};
		updateQueryParams();
	});
}


function updateQueryParams()
{
	var new_url =
		window.location.protocol+"//"+window.location.host+window.location.pathname;

	var first_param = true;
	for (var p in queryParams)
	{
		if (first_param)
		{
			new_url += "?";
			first_param = false;
		}
		else
		{
			new_url += "&";
		}

		new_url += p + "=" + queryParams[p];
	}

	if (new_url !== window.location.href)
	{
		window.history.pushState({}, "", new_url);
	}
}
