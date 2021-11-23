var margin = {top: 10, right: 20, bottom: 30, left: 50},
width = 1000 - margin.left - margin.right,
height = 420 - margin.top - margin.bottom;

let xVar;
let xMin;
let xMax;
let yVar;
let yMin;
let yMax;
let zVar;
let zMin;
let zMax;
let dimensions;

d3.queue()
    .defer(d3.json, "/donorschoose/manualcharts")
    .defer(d3.json, "/donorschoose/scatterplotdimensions")
    .await(drawChart)

// append the svg object to the body of the page
var svg = d3.select("#scatterplot")
.append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
.append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");



function drawChart(error, data2, data3) {

    console.log(data2)
    console.log(data3)
    xVar = data2.x;
    xMin = data2.xMin;
    xMax = data2.xMax;
    yVar = data2.y;
    yMin = data2.yMin;
    yMax = data2.yMax;
    zVar = data2.z;
    zMin = data2.zMin;
    zMax = data2.zMax;
    //bool1 = true;

    dimensions = data3;
    //bool2 = true;

    console.log("x: " + xVar);
    console.log("y: " + yVar);
    console.log("z: " + zVar);

    d3.json("/donorschoose/scatterplot", function(data) {

        // Add X axis
        var x = d3.scaleLinear()
            .domain([xMin, xMax])
            .range([ 0, width ]);
        svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x));
        
        // Add Y axis
        var y = d3.scaleLinear()
            .domain([yMin, yMax])
            .range([ height, 0]);
        svg.append("g")
            .call(d3.axisLeft(y));
        
        // Add a scale for bubble size
        var z = d3.scaleLinear()
            .domain([zMin, zMax])
            .range([ 4, 15]);
        
        //Add a scale for bubble color
        var myColor = d3.scaleOrdinal()
            .domain([zMin, zMax])
            .range(d3.schemeSet2);
        
        // -1- Create a tooltip div that is hidden by default:
        var tooltip = d3.select("#scatterplot")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip")
            .style("background-color", "black")
            .style("border-radius", "5px")
            .style("padding", "10px")
            .style("color", "white")
        
        // -2- Create 3 functions to show / update (when mouse move but stay on same circle) / hide the tooltip
        var showTooltip = function(d) {
            tooltip
            .transition()
            .duration(200)
            tooltip
            .style("opacity", 1)
            .html(dimensions[0] + " " + d[dimensions[0]] + " " + zVar + ": " + d[zVar])
            .style("left", (d3.mouse(this)[0]+60) + "px")
            .style("top", (d3.mouse(this)[1]+60) + "px")
        }
        var moveTooltip = function(d) {
            tooltip
            .style("left", (d3.mouse(this)[0]+200) + "px")
            .style("top", (d3.mouse(this)[1]+200) + "px")
        }
        var hideTooltip = function(d) {
            tooltip
            .transition()
            .duration(200)
            .style("opacity", 0)
        }
        
        // Add dots
        svg.append('g')
            .selectAll("dot")
            .data(data)
            .enter()
            .append("circle")
            .attr("class", "bubbles")
            .attr("cx", function (d) { return x(d[xVar]); } )
            .attr("cy", function (d) { return y(d[yVar]); } )
            .attr("r", function (d) { return z(d[zVar]); } )
            .style("fill", function (d) { return myColor(d[zVar]); } )
            // -3- Trigger the functions
            .on("mouseover", showTooltip )
            .on("mousemove", moveTooltip )
            .on("mouseleave", hideTooltip )
        
    })
}