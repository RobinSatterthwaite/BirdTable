
class ViewVisitRecordOverlay
{
	constructor(element)
	{
		this.element = element;

		this.element.addEventListener("scroll", (e) =>
		{
			e.stopPropagation();
		});

		document.getElementById("CloseVisitRecord").addEventListener("click", (e) =>
		{
			document.body.removeChild(this.element);
		});

		this.element.addEventListener("keyup", (e) =>
		{
			if (e.key == "Escape")
			{
				document.body.removeChild(this.element);
			}
		});

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
}
