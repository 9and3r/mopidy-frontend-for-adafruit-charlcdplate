//Use this method in https://www.quinapalus.com/hd44780udg.html

function generateArrayString(){
	var string = "[";
	for (var i=0; i<7; i++){
		string += "[";
		for (var z=0; z<5; z++){
			if (px[z][i] || px[z][i] == 1){
				value = 1;
			}else{
				value = 0;
			}
			string += value + ",";
		}
		string = string.substring(0, string.length - 1);
		string += "], ";
	}
	string = string.substring(0, string.length - 2);
	string += "]";
	console.log(string);
	window.prompt("Copy to clipboard: Ctrl+C, Enter", string);
}
