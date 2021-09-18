$(function() {
	var canadaMap = new Datamap({
		element: document.getElementById('canada'),
		geographyConfig: {
			dataUrl: '/static/geojson/canada.topo.json'
		},
		scope: 'canada',
		fills: {
			defaultFill: '#bada55'
		},
		setProjection: function(element) {
			var projection = d3.geo.mercator()
				.center([-95, 71])
				.scale(400)
				.translate([element.offsetWidth / 2, element.offsetHeight / 2]);
			var path = d3.geo.path().projection(projection);
			return {path: path, projection: projection};
		}
	});
	var USAmap = new Datamap({
		element: document.getElementById('usa'),
		geographyConfig: {
			dataUrl: '/static/geojson/usa.topo.json'
		},
		scope: 'usa',
		fills: {
			defaultFill: '#bada55'
		},
		setProjection: function(element) {
			var projection = d3.geo.mercator()
				.center([-120, 54])
				.scale(700)
				.translate([element.offsetWidth / 2, element.offsetHeight / 2]);
			var path = d3.geo.path().projection(projection);
			return {path: path, projection: projection};
		}
	});
});
