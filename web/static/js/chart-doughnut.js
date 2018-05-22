		var randomScalingFactor = function() {
			return Math.round(Math.random() * 100);
		};
		var config = {
			type: 'doughnut',
			data: {
				datasets: [{
					data: $('#canvas-holder').attr("mc-data-set").split(','),
					backgroundColor: [
						window.chartColors.red,
						window.chartColors.orange,
						window.chartColors.yellow,
						window.chartColors.green,
						window.chartColors.blue,
                        window.chartColors.purple,
                        window.chartColors.grey,
					],
					label: 'Dataset 1'
				}],
				labels: [
					'Trojan-Ransom',
					'Virus',
					'Trojan',
					'Backdoor',
					'not-a-virus:Downloader',
                    'Worm',
                    'Rootkit'
				]
			},
			options: {
				responsive: true,
				legend: {
					position: 'right',
				},
				title: {
					display: false
				},
				animation: {
					animateScale: true,
					animateRotate: true
				}
			}
		};
		window.onload = function() {
			var ctx = document.getElementById('chart-area').getContext('2d');
			window.myDoughnut = new Chart(ctx, config);
		};
		
		var colorNames = Object.keys(window.chartColors);


