<script lang="ts">
	import { Area, Axis, Chart, Highlight, Pie, Svg } from "layerchart";
	import { scaleLinear, scaleOrdinal } from "d3-scale";
	import * as d3shapes from "d3-shape";

	interface EnergyData {
		date: number; // Seconds
		value: number; // Energy level
	}

	let inCamera = {
		in: 0,
		out: 0,
	}

	let pieData = [
		{ date: 1, value: inCamera.in },
		{ date: 2, value: inCamera.out },
	];

	let energyData: EnergyData[] = [];
	let seconds = 0;
	let socket = new WebSocket("ws://192.168.1.103:80/stats");
	socket.onmessage = (data) => {
		const parsed = JSON.parse(data.data);
		energyData.push({ date: seconds++, value: parsed.energy });
		energyData = energyData.slice(-60);
		if (parsed.in_camera) {
			inCamera.in++;
		} else {
			inCamera.out++;
		}
		pieData = [
			{ date: 1, value: inCamera.in },
			{ date: 2, value: inCamera.out },
		];
	};

	const keyColors = [
		'hsl(var(--color-success))',
		'hsl(var(--color-danger))',
	];
</script>

<main class="p-4">
	<h1 class="text-2xl font-bold mt-8 mb-4">Energy Levels</h1>
	<div class="h-[300px] p-4 border rounded">
		<Chart
			data={energyData}
			x="date"
			xScale={scaleLinear()}
			y="value"
			yDomain={[0, null]}
			yNice
			padding={{ left: 16, bottom: 24 }}
			tooltip
		>
			<Svg>
				<Axis placement="left" grid rule />
				<Axis placement="bottom" format={(d) => d} rule />
				<Area line={{ class: 'stroke-2 stroke-primary' }} class="fill-primary/30"
					  curve={d3shapes['curveBasis']} />
				<Highlight points lines />
			</Svg>
		</Chart>
	</div>
	<h1 class="text-2xl font-bold mt-8 mb-4">In Camera</h1>
	<div class="h-[300px] p-4 border rounded">
		<Chart
			data={pieData}
			x="value"
			r="date"
			rScale={scaleOrdinal()}
			rRange={keyColors}
		>
			<Svg>
				<Pie tweened />
			</Svg>
		</Chart>
	</div>z
</main>
