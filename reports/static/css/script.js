function createtable() {
	const cells = document.getElementsByTagName('td');
    for (i = 0; i < cells.length; i++) {
      if (cells[i].innerHTML == "Pass") {
        cells[i].className += 'greenclass';
      }
      if (cells[i].innerHTML == "Fail") {
        cells[i].className += 'redclass';
      }
    }
  }