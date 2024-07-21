<script lang="ts">
	import { Button } from "svelte-ux";
	import { browser } from "$app/environment";
	import { Confetti } from "svelte-confetti";

	let cameraFrame: string;
	if (browser) {
		let socket = new WebSocket("ws://192.168.1.103:80/camera");
		socket.onmessage = (data) => {
			// Convert blob to bas64
			let reader = new FileReader();
			reader.onload = () => {
				cameraFrame = (reader.result as string).replace("application/octet-stream", "image/png");
			};
			reader.readAsDataURL(data.data);
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

	let socket = new WebSocket("ws://192.168.1.103:80/stats");
	let stats: Object;
	socket.onmessage = (data) => {
		stats = JSON.parse(data.data);
	};

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
	<h1 class="font-bold text-4xl pt-8">Camera Name</h1>
	<img class="rounded-2xl border-4 border-primary-200 my-4"
		 src="{cameraFrame}" alt="Camera" />
	<div class="py-2" />
	<Button class="w-full text-2xl my-4" variant="fill" color="secondary">Feed</Button>
	<Button class="w-full text-2xl my-4" variant="fill" color="accent" on:click={pet}>Pet ❤️</Button>
	<Button class="w-full text-2xl my-4" variant="fill" color="primary" on:click={takePhotoAndDownload}>Take Photo
	</Button>
</main>
