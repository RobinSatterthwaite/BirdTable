
function main()
{
	try
	{
		let new_visit_dialog = new NewVisitDialog(document.getElementById("NewVisitDialog"));
	
		document.getElementById("NewVisit").addEventListener("click", (e) =>
		{
			new_visit_dialog.show();
		});
	
		let date_headers = document.getElementsByClassName("visit-date");
		for (let date_el of date_headers)
		{
			let date_string = moment(date_el.innerText).format("YYYY-MM-DD");
			date_el.innerText = date_string;
		}
	}
	catch(e)
	{
		window.alert("A problem occured loading this page.");
		throw(e);
	}
}
