
class NewEditVisitRecordOverlay
{
	constructor(element)
	{
		this.element = element;

		this.startDateTime = flatpickr(
			document.getElementById("StartDateTime"),	{
				enableTime: true,
				dateFormat: "Y-m-d  H:i"
			});
		this.endDateTime = flatpickr(
			document.getElementById("EndDateTime"), {
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

		this.visitNotes = document.getElementById("VisitNotes");
		this.visitNotes.addEventListener("keyup", (e) =>
		{
			if (e.isComposing) return;

			if (e.key == "\\")
			{
				let cursor_pos = e.target.selectionStart-1;
				let pos = e.target.value.lastIndexOf(' ', cursor_pos)+1;
				if (pos > 0 && cursor_pos > pos)
				{
					let pre_word = e.target.value.substring(0, pos);
					let word = e.target.value.substring(pos, cursor_pos);
					let post_word = e.target.value.substring(cursor_pos+1);
					
					switch (word)
					{
					case "deg":
					case "degrees":
						e.target.value = pre_word + '\u00b0' + post_word;
						break;
					default:
						break;
					}
				}
			}
		});

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

		document.getElementById("AddNewVisit").addEventListener("click", (e) =>
		{
			if (window.confirm("Submit records?")) this.submit();
		});

		document.getElementById("CancelNewVisit").addEventListener("click", (e) =>
		{
			if (document.querySelector(".species-entry:not(.inactive)") == null ||
					window.confirm("Discard changes?"))
			{
				this.close();
			}
		});
	}


	setVisitData(visit_data)
	{
		this.element.dataset.visitId = visit_data.Id;
		this.startDateTime.setDate(visit_data.StartTime.format("YYYY-MM-DD  HH:mm"));
		this.endDateTime.setDate(visit_data.EndTime.format("YYYY-MM-DD  HH:mm"));
		this.siteName.value = visit_data.Site;
		this.siteName.dispatchEvent(new Event("input"));
		this.visitNotes.value = visit_data.Notes;

		let sightings = this.element.getElementsByClassName("species-entry");
		for (let sighting_inputs of sightings)
		{
			let species_id = sighting_inputs.dataset.speciesId;
			if (visit_data.Sightings.hasOwnProperty(species_id))
			{
				let sighting_data = visit_data.Sightings[species_id];
				sighting_inputs.getElementsByClassName("count")[0].value = sighting_data.Count;
				sighting_inputs.getElementsByClassName("uncertainty")[0].value = sighting_data.Uncertainty;
				sighting_inputs.getElementsByClassName("seen")[0].checked = sighting_data.Seen;
				sighting_inputs.getElementsByClassName("heard")[0].checked = sighting_data.Heard;
				sighting_inputs.getElementsByClassName("notes")[0].value = sighting_data.Notes;
				sighting_inputs.getElementsByClassName("feral")[0].checked = sighting_data.Feral;
				sighting_inputs.classList.remove("inactive");
			}
		}
	}


	getVisitData()
	{
		let visit = {};

		visit.StartTime = moment(this.startDateTime.selectedDates[0]).toISOString();
		visit.EndTime = moment(this.endDateTime.selectedDates[0]).toISOString();
		visit.Site = Number(this.siteName.dataset.value);
		visit.Notes = this.visitNotes.value;
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
		delete this.element.dataset.visitId;
		delete this.siteName.dataset.value;
		this.startDateTime.clear();
		this.endDateTime.clear();
		this.visitNotes.value = null;
		this.visitNotes.dispatchEvent(new Event("change"));

		let inputs = this.element.getElementsByTagName("input");
		for (let input of inputs)
		{
			input.value = null;
			input.checked = null;
			input.dispatchEvent(new Event("change"));
		}

		document.getElementById("NewVisitContainer").scrollTop = 0;
	}


	submit()
	{
		let visit = this.getVisitData();;
		let req_url =	window.location.protocol+"//"+window.location.host
		if (this.element.dataset.visitId === undefined)
		{
			req_url += "/newVisit";
		}
		else
		{
			let query = new URLSearchParams();
			query.set("visitId", this.element.dataset.visitId);
			req_url += "/editVisit?" + query.toString();
		}

		let req = new XMLHttpRequest();
		req.addEventListener("load", () =>
		{
			if ((req.status === 201 && this.element.dataset.visitId === undefined) ||
					req.status === 200)
			{
				this.close();
			}
		});
		req.open("PUT", req_url);

		req.setRequestHeader("Cache-Control", "no-cache");
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		req.send(JSON.stringify(visit));
	}


	show()
	{
		//this.element.classList.remove("slide-out-up");
		//this.element.classList.add("slide-in");
		this.element.classList.remove("hidden");
	}


	hide()
	{
		//this.element.classList.remove("slide-in");
		//this.element.classList.add("slide-out-up");
		this.element.classList.add("hidden");
	}


	close()
	{
		this.hide();
		this.clear();
	}
}
