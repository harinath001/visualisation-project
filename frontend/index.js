


var server_name = null;
var server_list = null;
var stats_interval = null;



function init(){
	show_servers();
	show_dashboard();
}


function fetch_server_list(){
	// this will make request to backend and bring all the existing servers available
	// for now we are hardcoding the values to ["server 1"]
	server_list = ["server 1"];
}


function show_servers(){
	// get the server list
	fetch_server_list();
	// fill the server list in the dropdown

}

function enable_stats(){
	// this function is to start hitting the server for data
	stats_interval = setInterval(refresh_stats_board, 3000);

}
function disable_stats(){

	// this function to stop the event of hitting the server for data
	if(stats_interval)clearInterval(stats_interval);
}


function show_dashboard(){
	// this function will show the dashboard
	dashboard = document.getElementById("dashboard");
	stats_board = document.getElementById("stats");
	logs_board = document.getElementById("logs");
	stats_board.style.display = "none";
	logs_board.style.display = "none";
	dashboard.style.display = "inline";
	disable_stats();
}




function show_stats(){
	// this function will show the stats board
	dashboard = document.getElementById("dashboard");
	stats_board = document.getElementById("stats");
	logs_board = document.getElementById("logs");
	stats_board.style.display = "inline";
	logs_board.style.display = "none";
	dashboard.style.display = "none";
	enable_stats();

}

function show_logs(){
	// this function will show the logs board
	dashboard = document.getElementById("dashboard");
	stats_board = document.getElementById("stats");
	logs_board = document.getElementById("logs");
	stats_board.style.display = "none";
	logs_board.style.display = "inline";
	dashboard.style.display = "none";
	disable_stats();
}


function refresh_stats_board(){
	// alert("stats data refreshed.");
	get_stats_data(server_name);
	var cpu_data;
	var network_data;
	var memory_data;
	var gpu_data;
	var disk_data;
	var processes_data;

	render_line_graph("cpu_board", cpu_data);
	render_line_graph("gpu_board", gpu_data);
	render_line_graph("network_board", network_data);
	render_line_graph("memory_board", memory_data);
	render_line_graph("disk_board", disk_data);
	render_line_graph("processes_board", processes_data);

}

function refresh_logs_board(){
	get_logs_data(server_name);
	alert("will refresh logs board");
}


function get_stats_data(given_server_name){

}


function get_logs_data(given_server_name){

}




function render_line_graph(div_id, data){
	// the data will be array of floating points.
	// access the width and height of the div using javascript

}

function render_bar_graph(div_id, dict){
	// keys will be on x-axis and corresponding values should be on y-axis
}

// EVENTS of dashboard
function server_selection_changed(){
	// this is triggered if dropdown is changed

}


//EVENTS of stats_board


// EVENTS of logs_board
function slider_changed(){
	// this will trigger if the slider to select the time range has been changed
}

window.onload = init;

