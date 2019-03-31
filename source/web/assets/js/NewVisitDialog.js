
class NewVisitDialog
{
	constructor(element)
	{
		this.element = element;

		let input_counts = this.element.getElementsByClassName("count");
		for (let input of input_counts)
		{
			input.addEventListener("change", (e) =>
			{
				let species_entry = e.target.closest(".species-entry");
				if (species_entry !== null)
				{
					let value = e.target.value;
					if (value === undefined || value === null || value === "" || value === "0")
					{
						species_entry.classList.add("inactive");
					}
					else
					{
						species_entry.classList.remove("inactive");
					}
				}
			});
		}

		this.startDateTime = flatpickr(
			document.getElementById("StartDateTime"),
			{
				enableTime: true,
				dateFormat: "Y-m-d  H:i"
			});
		this.endDateTime = flatpickr(
			document.getElementById("EndDateTime"),
			{
				enableTime: true,
				dateFormat: "Y-m-d  H:i"
			});

		this.siteName = document.getElementById("SiteName");
		this.siteName.addEventListener("input", (e) =>
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

		document.getElementById("AddNewVisit").addEventListener("click", (e) =>
		{
			if (window.confirm("Submit records?")) this.submit();
		});

		document.getElementById("CancelNewVisit").addEventListener("click", (e) =>
		{
			if (window.confirm("Discard changes?")) this.clear();
		});
	}


	submit()
	{
		let visit = this.getVisitData();

		let req_url =
			window.location.protocol+"//"+window.location.host+"/newVisit";

		let req = new XMLHttpRequest();
		req.addEventListener("load", () =>
		{
			if (req.status === 201) this.clear();
		});
		req.open("PUT", req_url);

		req.setRequestHeader("Cache-Control", "no-cache");
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		req.send(JSON.stringify(visit));
	}


	getVisitData()
	{
		let visit = {};

		visit.StartTime = moment(this.startDateTime.selectedDates[0]).toISOString();
		visit.EndTime = moment(this.endDateTime.selectedDates[0]).toISOString();
		visit.Site = Number(this.siteName.dataset.value);
		visit.Sightings = [];

		let sightings = this.element.getElementsByClassName("species-entry");
		for (let sighting_inputs of sightings)
		{
			let count = sighting_inputs.getElementsByClassName("count")[0].value;

			if (count > 0)
			{
				let species_id = sighting_inputs.dataset.speciesId;
				let uncertainty = sighting_inputs.getElementsByClassName("uncertainty")[0].value;
				let seen = sighting_inputs.getElementsByClassName("seen")[0].checked;
				let heard = sighting_inputs.getElementsByClassName("heard")[0].checked;
				let notes = sighting_inputs.getElementsByClassName("notes")[0].value;
				let feral = sighting_inputs.getElementsByClassName("feral")[0].checked;

				visit.Sightings.push({
					Species:     Number(species_id),
					Count:       Number(count),
					Uncertainty: Number(uncertainty),
					Seen:        seen,
					Heard:       heard,
					Notes:       notes,
					Feral:       feral
				});
			}
		}

		return visit;
	}


	clear()
	{
		this.startDateTime.clear();
		this.endDateTime.clear();

		let inputs = this.element.getElementsByTagName("input");
		for (let input of inputs)
		{
			input.value = null;
			input.checked = null;
			input.dispatchEvent(new Event("change"));
		}
	}
}
