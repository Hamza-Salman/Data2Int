// set the dimensions and margins of the graph
var margin1 = {top: 10, right: 30, bottom: 90, left: 40},
    width1 = 1000 - margin1.left - margin1.right,
    height1 = 450 - margin1.top - margin1.bottom;

d3.queue()
    .defer(d3.json, "/donorschoose/manualcharts")
    .defer(d3.json, "/donorschoose/scatterplotdimensions")
    .defer(d3.json, "/donorschoose/scatterplot")
    .await(drawChart)

// append the svg object to the body of the page
var svg1 = d3.select("#barchart")
  .append("svg")
    .attr("width", width1 + margin1.left + margin1.right)
    .attr("height", height1 + margin1.top + margin1.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin1.left + "," + (margin1.top) + ")");

// Parse the Data
function drawChart(error, data2, data3, data) {
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

    // X axis
    var x = d3.scaleBand()
    .range([ 0, width1 ])
    .domain(data.map(function(d) { return d[xVar]; }))
    .padding(0.2);
    svg1.append("g")
    .attr("transform", "translate(0," + height1 + ")")
    .call(d3.axisBottom(x))
    .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

    // Add Y axis
    var y = d3.scaleLinear()
    .domain([0, yMax])
    .range([ height1, 0]);
    svg1.append("g")
    .call(d3.axisLeft(y));

    var tooltip1 = d3.select("#barchart")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "black")
    .style("border-radius", "5px")
    .style("padding", "10px")
    .style("color", "white")

    var showTooltip = function(d) {
        tooltip1
        .transition()
        .duration(200)
        tooltip1
        .style("opacity", 1)
        .html(dimensions[0] + " " + d[dimensions[0]] + " " + zVar + ": " + d[zVar])
        .style("left", (d3.mouse(this)[0]+60) + "px")
        .style("top", (d3.mouse(this)[1]+60) + "px")
    }
    var moveTooltip = function(d) {
        tooltip1
        .style("left", (d3.mouse(this)[0]+250) + "px")
        .style("top", (d3.mouse(this)[1]+670) + "px")
    }
    var hideTooltip = function(d) {
        tooltip1
        .transition()
        .duration(200)
        .style("opacity", 0)
    }

    // Bars
    svg1.selectAll("mybar")
    .data(data)
    .enter()
    .append("rect")
        .attr("x", function(d) { return x(d[xVar]); })
        .attr("width", x.bandwidth())
        .attr("fill", "#69b3a2")
        // no bar at the beginning thus:
        .attr("height", function(d) { return height1 - y(0); }) // always equal to 0
        .attr("y", function(d) { return y(0); })
        .on("mouseover", showTooltip )
        .on("mousemove", moveTooltip )
        .on("mouseleave", hideTooltip )
    
    // Animation
    svg1.selectAll("rect")
    .transition()
    .attr("y", function(d) { return y(d[yVar]); })
    .attr("height", function(d) { return height1 - y(d[yVar]); })
    .delay(function(d,i){console.log(i) ; return(i*100)})

}