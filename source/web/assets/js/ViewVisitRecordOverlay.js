
class ViewVisitRecordOverlay
{
	constructor(element, visit_id, edit_visit_overlay)
	{
		this.element = element;
		this.visitId = visit_id;
		this.editVisit = edit_visit_overlay;

		this.element.addEventListener("scroll", (e) =>
		{
			e.stopPropagation();
		});

		document.getElementById("EditVisitRecord").addEventListener("click", (e) =>
		{
			this.edit();
		});

		document.getElementById("CloseVisitRecord").addEventListener("click", (e) =>
		{
			this.close();
		});

		this.element.addEventListener("keyup", (e) =>
		{
			if (e.key == "Escape")
			{
				this.close();
			}
		});

		this.element.focus();

		this.dateTimeElement = document.getElementById("VisitDateTime");
		let start_time = moment(this.dateTimeElement.dataset.startTime);
		let end_time = moment(this.dateTimeElement.dataset.endTime);

		this.dateTimeElement.innerText = start_time.format("dddd, D MMM YYYY — hh:mm a");
		if (start_time.isSame(end_time, 'day'))
		{
			this.dateTimeElement.innerText += " - " + end_time.format("hh:mm a");
		}
		else
		{
			this.dateTimeElement.innerText += " - " + end_time.format("dddd, D MMM YYYY  hh:mm a");
		}
	}

	edit()
	{
		let visit_data = {};

		visit_data.Id = this.visitId;
		visit_data.StartTime = moment(this.dateTimeElement.dataset.startTime);
		visit_data.EndTime = moment(this.dateTimeElement.dataset.endTime);
		visit_data.Site = document.getElementById("VisitSiteName").dataset.id;
		visit_data.Notes = document.getElementById("ViewVisitNotes").textContent.trim();
		visit_data.Sightings = {};

		let sightings = this.element.getElementsByClassName("species-entry");
		for (let sighting of sightings)
		{
			let species_id = Number(sighting.dataset.speciesId);
			visit_data.Sightings[species_id] = {
				Count:       Number(sighting.dataset.count),
				Uncertainty: Number(sighting.dataset.uncertainty),
				Seen:        (sighting.dataset.seen == "True"),
				Heard:       (sighting.dataset.heard == "True"),
				Notes:       sighting.getElementsByClassName("sighting-notes")[0].textContent.trim(),
				Feral:       (sighting.dataset.feral == "True")
			};
		}

		this.editVisit.setVisitData(visit_data);
		this.editVisit.show();
		this.close();
	}

	close()
	{
		document.body.removeChild(this.element);
	}
}
