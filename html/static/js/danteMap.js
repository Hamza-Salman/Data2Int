(function() {
    var margin = {top: 50, left: 50, right: 50, bottom: 50},
    height = 1010 - margin.top - margin.bottom,
    width = 1500 - margin.left - margin.right;
    

    var svg = d3.select("#map")
        .append("svg")
        .attr("height", height)
        .attr("width", width)//*1.8
        .attr("style", "background-color:rgb(202, 223, 230)")
        .append("g")
        .attr("transform", "translate(" + (width-2100) + "," + (height-1200) + ")");

    d3.queue()
      .defer(d3.json, "/static/geojson/worldGeo.topojson")
      .defer(d3.json, "/donorschoose/covid_genome_data")
      .await(ready)

    var projection = d3.geoMercator()
        .translate([ width, height])
        .scale(180)

    var path = d3.geoPath()
        .projection(projection)


    var tabulate = function (data,columns) {
        var table = d3.select('#tableData').append('table')
            var thead = table.append('thead')
            var tbody = table.append('tbody')
        
            thead.append('tr')
            .selectAll('th')
                .data(columns)
                .enter()
            .append('th')
                .text(function (d) { return d })
        
            var rows = tbody.selectAll('tr')
                .data(data)
                .enter()
            .append('tr')
        
            var cells = rows.selectAll('td')
                .data(function(row) {
                    return columns.map(function (column) {
                        return { column: column, value: row[column] }
                })
            })
            .enter()
            .append('td')
            .text(function (d) { return d.value })
        
        return table;
    }

    function ready (error, data, mapData) {
        console.log(data)
        const g = svg.append('g')

        var countries = topojson.feature(data, data.objects.worldGeo).features
        
        console.log(countries)
        console.log(mapData)
        
        g.selectAll(".country")
            .data(countries)
            .enter().append("path")
            .attr("class", "country")
            .attr("d", path)
            .attr("Country", function(d) {
                return d.properties.sovereignt; 
            })
            .attr("colorClass", "test")
            .classed("low", function(d) {
                var thisCountry = countries.find(x => x.properties.sovereignt == this.getAttribute("Country"))
                var countryId = thisCountry.properties.sovereignt
                console.log(thisCountry)
                console.log(countryId)
                console.log(mapData.Country)
                try {
                var thisData = mapData.filter(x => x["Country"] === countryId).length

                console.log(thisData)
                if (thisData < 1) {
                    this.setAttribute("colorClass", "low")
                    return true
                }else {
                    return false
                }
                } catch {
                        console.log("not found")
                        return true;
                }
                
            })
            .classed("lowmid", function(d) {
                var thisCountry = countries.find(x => x.properties.sovereignt == this.getAttribute("Country"))
               // console.log(mapData.filter(x => x == thisCountry).length)
                var countryId = thisCountry.properties.sovereignt
                try {
                   // var data = mapData.filter(x => x == thisCountry).length
                   var thisData = mapData.filter(x => x["Country"]  === countryId).length

                    if (thisData > 1 && thisData < 500) {
                        this.setAttribute("colorClass", "lowmid")
                        return true
                    }else {
                        return false
                    }
                    } catch {
                            console.log("not found")
                            return true;
                    }
                    
            })
            .classed("mid", function(d) {
                var thisCountry = countries.find(x => x.properties.sovereignt == this.getAttribute("Country"))
                var countryId = thisCountry.properties.sovereignt
                try {
                    var thisData = mapData.filter(x => x["Country"]  === countryId).length
                    if (thisData > 500 && thisData < 1000) {
                        this.setAttribute("colorClass", "mid")
                        return true
                    }else {
                        return false
                    }
                    } catch {
                            console.log("not found")
                            return true;
                    }
                    
            })
            .classed("midhigh", function(d) {
                var thisCountry = countries.find(x => x.properties.sovereignt == this.getAttribute("Country"))
                var countryId = thisCountry.properties.sovereignt
                try {
                    var thisData = mapData.filter(x => x["Country"]  === countryId).length
                    if (thisData > 1000 && thisData < 2000) {
                        this.setAttribute("colorClass", "midhigh")
                        return true
                    }else {
                        return false
                    }
                    } catch {
                            console.log("not found")
                            return true;
                    }
                    
            })
            .classed("high", function(d) {
                var thisCountry = countries.find(x => x.properties.sovereignt == this.getAttribute("Country"))
                var countryId = thisCountry.properties.sovereignt
                try {
                    var thisData = mapData.filter(x => x["Country"]  === countryId).length
                    if (thisData > 2000 && thisData < 5000) {
                        this.setAttribute("colorClass", "high")
                        return true
                    }else {
                        return false
                    }
                    } catch {
                            console.log("not found")
                            return true;
                    }
                    
            })
            .classed("extreme", function(d) {
                var thisCountry = countries.find(x => x.properties.sovereignt == this.getAttribute("Country"))
                var countryId = thisCountry.properties.sovereignt
                try {
                   var thisData = mapData.filter(x => x["Country"]  === countryId).length
                   
                    if (thisData > 5000) {
                        this.setAttribute("colorClass", "extreme")
                        return true
                    }else {
                        return false
                    }
                    } catch {
                            console.log("not found")
                            return true;
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
                var thisCountry = countries.find(x => x.properties.sovereignt == this.getAttribute("Country"))
                var countryId = thisCountry.properties.sovereignt
               
                    console.log(mapData.filter(x => x["Country"] === countryId))
                //var thisData = mapData.find(x => x["Country"] === countryId) //THIS IS NEEDED
                 $("#tableData").html("");
                 var columns = ['Nucleotide_Accession', 'Species_Taxonomy_Id','Species_Name','Virus_Genus','Virus_Family', 'Isolate_Name','Nucleotide_Length', 'Sequence_Type','Nuc_Completeness', 'Continent', 'Country', 'City', 'Host_Taxonomy_ID']
                 var country_data = mapData.filter(x => x["Country"] === countryId)
                 tabulate(country_data,columns)


        svg.selectAll(".country")
            .append('title')
            .text(d => d.properties.sovereignt)
        svg.call(d3.zoom().on('zoom', () => {
            g.attr('transform', d3.event.transform)
        }))

    })
    }
})();