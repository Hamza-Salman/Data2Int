(function() {
    var margin = {top: 50, left: 50, right: 50, bottom: 50},
    height = 1000 - margin.top - margin.bottom,
    width = 1000 - margin.left - margin.right;
    

    var svg = d3.select("#map")
        .append("svg")
        .attr("height", height + margin.top + margin.bottom)
        .attr("width", width*1.5 + margin.left + margin.right)
        .append("g")
        .attr("transform", "translate(" + width/1.5 + "," + height/2.5 + ")");

    d3.queue()
      .defer(d3.json, "/static/geojson/canada_divisions.json")
      .defer(d3.json, "/donorschoose/mapdata")
      .await(ready)

    var projection = d3.geoMercator()
        .translate([ width, height])
        .scale(600)

    var path = d3.geoPath()
        .projection(projection)

    function ready (error, data, mapData) {

        const g = svg.append('g')

        var divisions = topojson.feature(data, data.objects.canada_divisions).features

        console.log(divisions)
        console.log(mapData)

        g.selectAll(".division")
            .data(divisions)
            .enter().append("path")
            .attr("class", "division")
            .attr("d", path)
            .attr("id", function(d) {
                return d.properties.CDUID; 
            })
            .attr("colorClass", "test")
            .classed("low", function(d) {
                var thisDivision = divisions.find(x => x.properties.CDUID === this.id)
                var divisionId = thisDivision.properties.CDUID
                var thisData = mapData.find(x => x["GEO_CODE (POR)"] === divisionId)
                var population = thisData["Dim: Sex (3): Member ID: [1]: Total - Sex"]
                if (population < 10000) {
                    this.setAttribute("colorClass", "low")
                    return true
                }else {
                    return false
                }
            })
            .classed("lowmid", function(d) {
                var thisDivision = divisions.find(x => x.properties.CDUID === this.id)
                var divisionId = thisDivision.properties.CDUID
                var thisData = mapData.find(x => x["GEO_CODE (POR)"] === divisionId)
                var population = thisData["Dim: Sex (3): Member ID: [1]: Total - Sex"]
                if (population < 50000 && population >= 10000) {
                    this.setAttribute("colorClass", "lowmid")
                    return true
                }else {
                    return false
                }
            })
            .classed("mid", function(d) {
                var thisDivision = divisions.find(x => x.properties.CDUID === this.id)
                var divisionId = thisDivision.properties.CDUID
                var thisData = mapData.find(x => x["GEO_CODE (POR)"] === divisionId)
                var population = thisData["Dim: Sex (3): Member ID: [1]: Total - Sex"]
                if (population < 100000 && population >= 50000) {
                    this.setAttribute("colorClass", "mid")
                    return true
                }else {
                    return false
                }
            })
            .classed("midhigh", function(d) {
                var thisDivision = divisions.find(x => x.properties.CDUID === this.id)
                var divisionId = thisDivision.properties.CDUID
                var thisData = mapData.find(x => x["GEO_CODE (POR)"] === divisionId)
                var population = thisData["Dim: Sex (3): Member ID: [1]: Total - Sex"]
                if (population < 500000 && population >= 100000) {
                    this.setAttribute("colorClass", "midhigh")
                    return true
                }else {
                    return false
                }
            })
            .classed("high", function(d) {
                var thisDivision = divisions.find(x => x.properties.CDUID === this.id)
                var divisionId = thisDivision.properties.CDUID
                var thisData = mapData.find(x => x["GEO_CODE (POR)"] === divisionId)
                var population = thisData["Dim: Sex (3): Member ID: [1]: Total - Sex"]
                if (population < 1000000 && population >= 500000) {
                    this.setAttribute("colorClass", "high")
                    return true
                }else {
                    return false
                }
            })
            .classed("extreme", function(d) {
                var thisDivision = divisions.find(x => x.properties.CDUID === this.id)
                var divisionId = thisDivision.properties.CDUID
                var thisData = mapData.find(x => x["GEO_CODE (POR)"] === divisionId)
                var population = thisData["Dim: Sex (3): Member ID: [1]: Total - Sex"]
                if (population >= 1000000) {
                    this.setAttribute("colorClass", "extreme")
                    return true
                }else {
                    return false
                }
            })
            .on('mouseenter', function(d){
                d3.select(this).classed("low", false)
                d3.select(this).classed("lowmid", false)
                d3.select(this).classed("mid", false)
                d3.select(this).classed("midhigh", false)
                d3.select(this).classed("high", false)
                d3.select(this).classed("extreme", false)
                d3.select(this).classed("selected", true)
            })
            .on('mouseout', function(d){
                d3.select(this).classed(this.getAttribute("colorClass"), true)
                d3.select(this).classed("selected", false)
            })
            .on('click', function(d) {
                var thisDivision = divisions.find(x => x.properties.CDUID === this.id)
                var divisionId = thisDivision.properties.CDUID
                var thisData = mapData.find(x => x["GEO_CODE (POR)"] === divisionId) //THIS IS NEEDED
                var divisonName = thisData.GEO_NAME//THIS IS NEEDED
                var totalPopulation = thisData["Dim: Sex (3): Member ID: [1]: Total - Sex"]//THIS IS NEEDED
                alert(divisonName + "\nTotal Population: " + totalPopulation)

        svg.selectAll(".division")
            .append('title')
            .text(d => d.properties.CDNAME)

        svg.call(d3.zoom().on('zoom', () => {
            g.attr('transform', d3.event.transform)
        }))

    })
    }
})();