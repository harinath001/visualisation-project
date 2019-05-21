


var server_name = "server 1";
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
	stats_interval = setInterval(refresh_stats_board, 2000);
    refresh_stats_board();
}
function disable_stats(){

	//alert("dis");

	// this function to stop the event of hitting the server for data
	if(stats_interval)clearInterval(stats_interval);
	//if(stats_interval)clearTimeout(stats_interval);
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

}

function refresh_logs_board(){
	get_logs_data(server_name);
	alert("will refresh logs board");
}


function get_stats_data(given_server_name){
	//alert("asfsf");
    console.log("Getting stats data from server ", given_server_name);
    $.ajax({
        url: 'http://172.24.16.228/stats/get?server_name='+given_server_name,
        success: function(data) {
            console.log(data);
            handle_stats_data(data);
        }
        //complete: 
    });
}

function handle_stats_data(data){
	var res = JSON.parse(data)['results'];
	console.log(res)
	var cpu_data=[];
	var network_data=[];
	var memory_data=[];
	var gpu_data=[];
	var disk_data=[];
	var processes_data=[];
	var i;
	//console.log(res.length)
	for (i = 0; i < res.length; i++) { 
	 	cpu_data.push({'cpu':res[i].cpu});
	 	network_data.push({'network':res[i].network/10000000});
	 	memory_data.push({'memory':res[i].memory});
	 	gpu_data.push({'gpu':res[i].gpu});
	 	disk_data.push({'disk':res[i].disk});
	 	processes_data.push({'processes':res[i].processes});
	}
	render_line_graph("cpu_board", cpu_data);
	//render_line_graph("gpu_board", gpu_data);
	render_line_graph("network_board", network_data);
	render_line_graph("memory_board", memory_data);
	render_line_graph("disk_board", disk_data);
	render_line_graph("processes_board", processes_data);
	//console.log(cpu_data)
}

function get_logs_data(given_server_name){

}

function calc_min(data){
	var m = 1000000;
	var i;
	for (i=0;i<data.length;i++){
		var k = data[i][Object.keys(data[i])[0]];
		if (k!=="null"){
			if (m>k){
				m=k;
			}
		}
	}
	console.log(m);
	return m
}
function render_line_graph(div_id, data){
	// the data will be array of floating points.
	// access the width and height of the div using javascript
	d3.select("#"+div_id).selectAll("*").remove();
	console.log("render_line_graph")
	var box = document.getElementById(div_id);
	var margin = {top: box.clientHeight*0.1, right: box.clientWidth*0.1,
	 bottom: box.clientHeight*0.1, left: box.clientWidth*0.1}
	var width = box.clientWidth - margin.left - margin.right
	var height = box.clientHeight - margin.top - margin.bottom
	//var rect = box.getBoundingClientRect();
	var svg = d3.select("#"+div_id)
				.append("svg:svg")
				.attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.bottom)
				.append("g")
				.attr("transform",
				"translate(" + margin.left + "," + margin.top + ")");
	//var keys = d3.keys(data);
	console.log(data)
	// console.log(keys)
	// console.log(rect)
	var x = d3.scaleLinear().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);
	// define the line
	var valueline = d3.line()
					  .defined(function(d) { return d; })
					  .x(function(d,i) { return x(i); })
				   	  .y(function(d) { return y(d[d3.keys(d)[0]]); });
	
	var m = calc_min(data)
	x.domain(d3.extent(data, function(d,i) { return i; }));
	y.domain([m, d3.max(data, function(d) { return d[d3.keys(d)[0]]; })]);
	//d3.min(data, function(d) { return d[d3.keys(d)[0]]; })
	function make_y_gridlines() {		
	    return d3.axisLeft(y)
	        .ticks(3)
	}
	svg.append("g")			
      .attr("class", "grid")
      .call(make_y_gridlines()
          .tickSize(-width)
          .tickFormat("")
      )
	svg.append("path")
		.data([data])
		.attr("class", "line")
		.attr("d", valueline);

	// Add the X Axis
	svg.append("g")
		.attr("transform", "translate(0," + height + ")")
		.attr("class", "axisWhite")
		.call(d3.axisBottom(x));

	// Add the Y Axis
	svg.append("g")
		.attr("class", "axisWhite")
		.call(d3.axisLeft(y));

	// svg.selectAll(".dot")
	// 	.data(data)
	// 	.data(data.filter(function(d) { return d; }))
	// 	.enter().append("circle") // Uses the enter().append() method
	// 	.attr("class", "dot") // Assign a class for styling
	// 	.attr("cx", function(d, i) { return x(i) })
	// 	.attr("cy", function(d) { return y(d[d3.keys(d)[0]]) })
	// 	.attr("r", 5);

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

