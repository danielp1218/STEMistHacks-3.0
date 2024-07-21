<script lang="ts">
	import { Button, Progress } from "svelte-ux";
	import { browser } from "$app/environment";
	import { Confetti } from "svelte-confetti";

	let cameraFrame: string;
	let stats: {energy: number, hunger: number, mood: string, in_camera:boolean} = {energy: 0, hunger: 0, mood: "happy", in_camera: false};


	const serverAddress = "192.168.1.103:80"; //LAN IP used for testing, would use ngrok/other services for production

	if (browser) {
		let socket = new WebSocket(`ws://${serverAddress}/camera`);
		socket.onmessage = (data) => {
			// Convert blob to bas64
			let reader = new FileReader();
			reader.onload = () => {
				cameraFrame = (reader.result as string).replace("application/octet-stream", "image/png");
			};
			reader.readAsDataURL(data.data);
		};

		let socket = new WebSocket(`ws://${serverAddress}/stats`);
		statSocket.onmessage = (data) => {
			stats = JSON.parse(data.data);
		};
	}

	const takePhotoAndDownload = () => {
		let a = document.createElement("a");
		a.href = cameraFrame;
		a.download = "photo.png";
		a.click();
	};

	let showHearts = false;
	let timeout: NodeJS.Timeout;

	const pet = () => {
		showHearts = true;
		clearTimeout(timeout);
		timeout = setTimeout(() => {
			showHearts = false;
		}, 5000);
	};

	const feed = () => {
		const response = await fetch(`${serverAddress}/feed`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ amount: 10 }),
		});
	}
</script>

<main class="p-4">
	{#if showHearts}
		<div style="
		 position: fixed;
		 top: -50px;
		 left: 0;
		 height: 100vh;
		 width: 100vw;
		 display: flex;
		 justify-content: center;
		 overflow: hidden;
		 pointer-events: none;">R
			<Confetti size=40 x={[-5, 5]} y={[0, 0.1]} delay={[500, 2000]} infinite duration=5000 amount=200
					  fallDistance="100vh"
					  colorArray={["url(https://static-00.iconduck.com/assets.00/red-heart-emoji-2048x1879-8wl1z711.png)"]} />
		</div>
	{/if}
	<h1 class="font-bold text-4xl pt-2">Camera View</h1>
	<img class="rounded-2xl border-4 border-primary-200 my-4"
		 src="{cameraFrame}" alt="Camera" />
	<div class="py-2" />
	<div class="flex">
		<Button class="w-32 text-2xl mr-3" variant="fill" color="secondary" on:click={feed}>Feed</Button>
		<div class="rounded border-2 p-3">
			<div class="flex">
				<h3 style="line-height:.4rem; margin-right: 5px">Energy: </h3>
				<Progress class="ml-3" value={stats.energy} max={100} color="primary">Energy</Progress>
			</div>
			<div class="flex mt-5">
				<h3 style="line-height:.4rem">Hunger: </h3>
				<Progress class="ml-3" value={stats.hunger} max={100} color="red">Hunger</Progress>
			</div>
		</div>
	</div>
	<Button class="w-full text-2xl my-4" variant="fill" color="accent" on:click={pet}>Pet ❤️</Button>
	<Button class="w-full text-2xl" variant="fill" color="primary" on:click={takePhotoAndDownload}>Take Photo
	</Button>
</main>
