// Set the dimensions of the canvas / graph
var	margin = {top: 30, right: 20, bottom: 30, left: 70},
	width = 800 - margin.left - margin.right,
	height = 440 - margin.top - margin.bottom;

// Parse the date / time
var	parseDate = d3.time.format("%Y-%m-%d").parse;

var parseDateTime = d3.time.format("%Y-%m-%dT%H:%M:%S").parse;

// Set the ranges
var	x = d3.time.scale().range([0, width]);
var	y = d3.scale.linear().range([height, 0]);

// Define the axes
var	xAxis = d3.svg.axis().scale(x)
	.orient("bottom").ticks(5);

var	yAxis = d3.svg.axis().scale(y)
	.orient("left").ticks(8);

// Define the line
var	valueline = d3.svg.line()
	.x(function(d) { return x(d.Reported_Date); })
	.y(function(d) { return y(d.Total_ICU_Covid_19); });

var valueline2 = d3.svg.line()
	.x(function(d) { return x(d.Reported_Date); })
	.y(function(d) { return y(d.Total_Cases); })

var valueline3 = d3.svg.line()
	.x(function(d) { return x(d.date); })
	.y(function(d) { return y(d.numconf); })

var oneDoseVaccinatedLine = d3.svg.line()
	.x(function(d) { return x(d.report_date); })
	.y(function(d) { return y(d.total_individuals_at_least_one); })

var twoDosesVaccinatedLine = d3.svg.line()
	.x(function(d) { return x(d.report_date); })
	.y(function(d) { return y(d.total_individuals_fully_vaccinated); })

// Adds the svg canvas
var	chart1 = d3.select("#charts")
	.append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Get the data
d3.csv("/static/js/datasources/ontarioicucovid.csv", function(error, data) {
	data.forEach(function(d) {
		d.Reported_Date = parseDate(d.Reported_Date);
		d.Total_ICU_Covid_19 = +d.Total_ICU_Covid_19;
	});

	// Scale the range of the data
	x.domain(d3.extent(data, function(d) { return d.Reported_Date; }));
	y.domain([0, d3.max(data, function(d) { return d.Total_ICU_Covid_19; })]);

	// Add the valueline path.
	chart1.append("path")
		.attr("class", "line")
		.attr("d", valueline(data));

	// Add the X Axis
	chart1.append("g")
		.attr("class", "x axis")
		.attr("transform", "translate(0," + height + ")")
		.call(xAxis);

	// Add the Y Axis
	chart1.append("g")
		.attr("class", "y axis")
		.call(yAxis);

	chart1.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .text("Figure 1: Ontario ICU Admissions Due to Covid-19");

	  // text label for the y axis
  	chart1.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - margin.left)
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("ICU Count");

});

// Adds the svg canvas
var	chart2 = d3.select("#charts")
	.append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	.append("g")
		.attr("transform", "translate(" + (margin.left + 50) + "," + margin.top + ")");


// Get the data
d3.csv("/static/js/datasources/totalcases.csv", function(error, data) {
	data.forEach(function(d) {
		d.Reported_Date= parseDate(d.Reported_Date);
		d.Total_Cases = +d.Total_Cases;
	});

	// Scale the range of the data
	x.domain(d3.extent(data, function(d) { return d.Reported_Date; }));
	y.domain([0, d3.max(data, function(d) { return d.Total_Cases; })]);

	// Add the valueline path.
	chart2.append("path")
		.attr("class", "line")
		.attr("d", valueline2(data));

	// Add the X Axis
	chart2.append("g")
		.attr("class", "x axis")
		.attr("transform", "translate(0," + height + ")")
		.call(xAxis);

	// Add the Y Axis
	chart2.append("g")
		.attr("class", "y axis")
		.call(yAxis);

	chart2.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .text("Figure 2: Total Covid-19 Cases in Ontario");

	// text label for the y axis
  	chart2.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - (margin.left+30))
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Case Count");
});

// Set the dimensions of the canvas / graph
var	chart3margin = {top: 30, right: 120, bottom: 30, left: 70},
	chart3width = 800 - chart3margin.left - chart3margin.right,
	chart3height = 440 - chart3margin.top - chart3margin.bottom;

// Set the ranges
x = d3.time.scale().range([0, chart3width]);
y = d3.scale.linear().range([chart3height, 0]);

// Define the axes
var xAxis = d3.svg.axis().scale(x)
    .orient("bottom").ticks(5);

var yAxis = d3.svg.axis().scale(y)
    .orient("left").ticks(8);

// Define the line
var caseline = d3.svg.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.numconf); });

// Adds the svg canvas
var chart3 = d3.select("#charts")
    .append("svg")
        .attr("width", chart3width + chart3margin.left + chart3margin.right + 100 )
        .attr("height", chart3height + chart3margin.top + chart3margin.bottom)
    .append("g")
        .attr("transform",
              "translate(" + (chart3margin.left + 30) +"," + chart3margin.top + ")");

chart3.selectAll("svg").attr("id", function(d,i) { return i; });

// Get the data
d3.csv("/static/js/datasources/canadaconfirmedcases.csv", function(error, data) {
    data.forEach(function(d) {
		d.date = parseDate(d.date);
		d.numconf = +d.numconf;
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, d3.max(data, function(d) { return d.numconf; })]);

    // Nest the entries by symbol
    var dataNest = d3.nest()
        .key(function(d) {return d.prname;})
        .entries(data);

    var color = d3.scale.category20b();   // set the colour scale

    var legendSpace = chart3width / dataNest.length; // spacing for legend

    // Loop through each symbol / key
    dataNest.forEach(function(d,i) {

        chart3.append("path")
            .attr("class", "line")
            .style("stroke", function() { // Add the colours dynamically
                return d.color = color(d.key); })
            .attr("d", caseline(d.values));

        // Add the Legend
        chart3.append("text")
            .attr("x", 700) // spacing
            .attr("y", i*(legendSpace/2))
            .attr("class", "legend")    // style the legend
            .style("fill", function() { // dynamic colours
                return d.color = color(d.key); })
            .text(d.key);

    });

    // Add the X Axis
    chart3.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + chart3height + ")")
        .call(xAxis);

    // Add the Y Axis
    chart3.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    chart3.append("text")
        .attr("x", (chart3width / 2))
        .attr("y", 0 - (chart3margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .text("Figure 3: Covid-19 Cases Across Canada and All Provinces");


	  // text label for the y axis
  	chart3.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - (chart3margin.left + 30))
      .attr("x",0 - (chart3height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Covid-19 Case Counts");

});
// Define the axes
var	xAxis = d3.svg.axis().scale(x)
	.orient("bottom").ticks(5);

var	yAxis = d3.svg.axis().scale(y)
	.orient("left").ticks(8);

// Adds the svg canvas
var	chart4 = d3.select("#charts")
	.append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
	.append("g")
		.attr("transform", "translate(" + (margin.left + 50) + "," + margin.top + ")");


// Get the data
d3.csv("/static/js/datasources/covid_vaccine_doses_stats.csv", function(error, data) {
	data.forEach(function(d) {
		d.report_date = parseDateTime(d.report_date);
		d.total_individuals_at_least_one = +d.total_individuals_at_least_one;
		d.total_individuals_fully_vaccinated = +d.total_individuals_fully_vaccinated;
	});

	// Scale the range of the data
	x.domain(d3.extent(data, function(d) { return d.report_date; }));
	y.domain([0, d3.max(data, function(d) { return d.total_individuals_at_least_one; })],
		[0, d3.max(data, function(d) { return d.total_individuals_fully_vaccinated; })]);

	// Add the valueline path.
	chart4.append("path")
		.attr("class", "line")
		.attr("d", oneDoseVaccinatedLine(data));

	chart4.append("path")
		.attr("class", "line")
		.style("stroke", "red")
		.attr("d", twoDosesVaccinatedLine(data))

	// Add the Legend
	chart4.append("text")
            .attr("x", 240) // spacing
            .attr("y", 100)
            .attr("class", "legend")    // style the legend
            .style("fill", "steelblue")
            .text("First Doses");

	// Add the Legend
	chart4.append("text")
            .attr("x", 410) // spacing
            .attr("y", 200)
            .attr("class", "legend")    // style the legend
            .style("fill", "red")
            .text("Second Doses");

	// Add the X Axis
	chart4.append("g")
		.attr("class", "x axis")
		.attr("transform", "translate(0," + height + ")")
		.call(xAxis);

	// Add the Y Axis
	chart4.append("g")
		.attr("class", "y axis")
		.call(yAxis);

	chart4.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .text("Figure 4: Vaccination Rates in Ontario");

	// text label for the y axis
  	chart4.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - (margin.left+50))
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Doses administered");
});