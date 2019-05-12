
class ContextMenu
{
	constructor(menu, parent)
	{
		this.menu = menu;
		
		parent.addEventListener("contextmenu", (e) =>
		{
			e.stopPropagation();
			e.preventDefault();

			this.open(e.pageX, e.pageY);
		});

		document.body.addEventListener("keyup", (e) =>
		{
			if (!this.menu.classList.contains("hidden"))
			{
				e.stopPropagation();
				e.preventDefault();

				this.handleKey(e.key);
			}
		});

		this.menu.addEventListener("mousemove", (e) =>
		{
			this.clearSelection();
		});

		document.body.addEventListener("click", (e) =>
		{
			this.close();
		});

		this.menu.addEventListener("click", (e) =>
		{
			e.stopPropagation();
		});

		for (let menu_option of this.menu.children)
		{
			let method = menu_option.dataset.method;
			if (method !== undefined && method !== null && method !== "")
			{
				ContextMenu.prototype[method] = (e) => {};

				menu_option.addEventListener("click", (e) => { this[method](); });
			}
		}
	}


	open(x, y)
	{
		let menu_width = this.menu.offsetWidth;
		let menu_height = this.menu.offsetHeight;
		let page_width = document.body.offsetWidth;
		let page_height = document.body.offsetHeight;

		if (x > page_width-menu_width) x = page_width-menu_width-1;
		if (y > page_height-menu_height) y = page_height-menu_height-1;

		this.menu.style.left = x+'px';
		this.menu.style.top = y+'px';
		this.menu.classList.remove("hidden");
	}


	close()
	{
		this.clearSelection();
		this.menu.classList.add("hidden");
	}


	handleKey(key)
	{
		switch (key)
		{
		case "ArrowUp":
			{
				let selected = this.menu.querySelector(".selected");
				if (selected === null)
				{
					if (this.menu.lastElementChild !== null)
					{
						this.menu.lastElementChild.classList.add("selected");
					}
				}
				else
				{
					selected.classList.remove("selected");
					if (selected.previousElementSibling !== null)
					{
						selected.previousElementSibling.classList.add("selected");
					}
				}
			}
			break;

		case "ArrowDown":
			{
				let selected = this.menu.querySelector(".selected");
				if (selected === null)
				{
					if (this.menu.firstElementChild !== null)
					{
						this.menu.firstElementChild.classList.add("selected");
					}
				}
				else
				{
					selected.classList.remove("selected");
					if (selected.nextElementSibling !== null)
					{
						selected.nextElementSibling.classList.add("selected");
					}
				}
			}
			break;

		case "PageUp":
			this.clearSelection();
			if (this.menu.firstElementChild !== null)
			{
				this.menu.firstElementChild.classList.add("selected");
			}
			break;

		case "PageDown":
			this.clearSelection();
			if (this.menu.lastElementChild !== null)
			{
				this.menu.lastElementChild.classList.add("selected");
			}
			break;

		case "Enter":
			{
				let selected = this.menu.querySelector(".selected");
				if (selected !== null)
				{
					let method = selected.dataset.method;
					this[method]();
				}
				this.close();
			}
			break;

		case "Escape":
			this.close();
			break;

		default:
			/* do nothing */
			break;
		}
	}


	clearSelection()
	{
		for (let opt of this.menu.children)
		{
			opt.classList.remove("selected");
		}
	}
}
